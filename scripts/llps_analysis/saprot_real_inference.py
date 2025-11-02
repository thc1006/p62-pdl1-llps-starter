#!/usr/bin/env python3
"""
Real SaProt Inference for LLPS Prediction
Using pre-trained transformer model from HuggingFace
"""
import sys
import torch
from transformers import EsmTokenizer, EsmForMaskedLM
from pathlib import Path
import json
import numpy as np

# Check GPU
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
print(f"[Device] Using: {device}")
if torch.cuda.is_available():
    print(f"[GPU] {torch.cuda.get_device_name(0)}")
    print(f"[GPU] Memory: {torch.cuda.get_device_properties(0).total_memory / 1e9:.2f} GB")

# Model configuration
MODEL_NAME = "westlake-repl/SaProt_650M_AF2"  # 650M parameters, fits in 4GB VRAM

def download_model():
    """Download SaProt model from HuggingFace"""
    print(f"\n[Download] Loading tokenizer and model from HuggingFace...")
    print(f"[Download] Model: {MODEL_NAME}")
    print(f"[Download] This may take a few minutes on first run...")

    try:
        tokenizer = EsmTokenizer.from_pretrained(MODEL_NAME)
        model = EsmForMaskedLM.from_pretrained(MODEL_NAME)
        model.to(device)
        model.eval()

        print(f"[Download] Success!")
        print(f"[Model] Parameters: {sum(p.numel() for p in model.parameters()) / 1e6:.1f}M")
        print(f"[Model] Device: {next(model.parameters()).device}")

        return tokenizer, model

    except Exception as e:
        print(f"\n[ERROR] Failed to download model: {e}")
        print(f"\n[SOLUTION] Try:")
        print(f"  1. Install transformers: pip install transformers")
        print(f"  2. Check internet connection")
        print(f"  3. Use smaller model if OOM: SaProt_35M_AF2")
        return None, None

def get_protein_embeddings(tokenizer, model, sequence, protein_name="unknown"):
    """
    Get protein embeddings from SaProt model

    Args:
        tokenizer: HuggingFace tokenizer
        model: SaProt model
        sequence: Amino acid sequence (single-letter codes)
        protein_name: Protein identifier

    Returns:
        embedding: Mean-pooled embedding vector (shape: [hidden_dim])
        per_residue_features: Per-residue features for disorder analysis
    """
    print(f"\n[Inference] {protein_name} ({len(sequence)} aa)...")

    # Tokenize sequence
    inputs = tokenizer(sequence, return_tensors="pt", padding=True, truncation=True, max_length=1024)
    inputs = {k: v.to(device) for k, v in inputs.items()}

    # Get hidden states (forward pass)
    with torch.no_grad():
        outputs = model(**inputs, output_hidden_states=True)
        hidden_states = outputs.hidden_states[-1]  # Last layer: [batch, seq_len, hidden_dim]

    # Mean pooling (excluding special tokens)
    attention_mask = inputs['attention_mask']
    mask_expanded = attention_mask.unsqueeze(-1).expand(hidden_states.size()).float()
    sum_hidden = torch.sum(hidden_states * mask_expanded, dim=1)
    sum_mask = torch.clamp(mask_expanded.sum(dim=1), min=1e-9)
    mean_embedding = sum_hidden / sum_mask  # [batch, hidden_dim]

    # Per-residue features (for disorder analysis)
    # Extract all tokens (full sequence length)
    seq_len = hidden_states.shape[1]
    per_residue = hidden_states[0, :, :].cpu().numpy()  # Full sequence including special tokens

    # LLPS propensity heuristic from embeddings
    # Use variance across ALL positions (more robust)
    if seq_len > 2:
        embedding_variance = torch.var(hidden_states[0, :, :]).item()  # Variance across all positions
    else:
        embedding_variance = 0.0  # Fallback for very short sequences

    print(f"  Embedding shape: {mean_embedding.shape}")
    print(f"  Per-residue shape: {per_residue.shape}")
    print(f"  Embedding variance (disorder proxy): {embedding_variance:.3f}")

    return mean_embedding.cpu().numpy(), per_residue, embedding_variance

def predict_llps_from_embedding(embedding, per_residue_features, variance):
    """
    Predict LLPS propensity from SaProt embeddings

    This is a heuristic-based prediction. For production, train a classifier on:
    - CD-CODE database (positive examples: known condensate proteins)
    - Negative examples: non-condensing proteins
    """

    # Heuristic 1: Embedding variance (higher = more disordered)
    # Threshold based on typical IDR proteins
    disorder_score = min(1.0, variance / 0.01)  # Normalize

    # Heuristic 2: Per-residue feature heterogeneity
    # LLPS proteins often have patchy/heterogeneous features
    if per_residue_features.shape[0] > 10:
        local_stds = []
        window = 10
        for i in range(0, len(per_residue_features) - window, window//2):
            window_feats = per_residue_features[i:i+window]
            local_std = np.std(window_feats, axis=0).mean()
            local_stds.append(local_std)

        heterogeneity_score = np.mean(local_stds) if local_stds else 0.0
        heterogeneity_score = min(1.0, heterogeneity_score / 50.0)  # Normalize
    else:
        heterogeneity_score = 0.0

    # Combined LLPS score
    llps_score = 0.6 * disorder_score + 0.4 * heterogeneity_score

    verdict = "HIGH" if llps_score > 0.6 else "MEDIUM" if llps_score > 0.4 else "LOW"

    result = {
        "llps_score": round(llps_score, 3),
        "disorder_score": round(disorder_score, 3),
        "heterogeneity_score": round(heterogeneity_score, 3),
        "embedding_variance": round(variance, 3),
        "verdict": verdict
    }

    print(f"  LLPS score: {llps_score:.3f} ({verdict})")
    print(f"    - Disorder: {disorder_score:.3f}")
    print(f"    - Heterogeneity: {heterogeneity_score:.3f}")

    return result

def main():
    """Main execution"""

    print("=" * 80)
    print("SaProt Real Inference for LLPS Prediction")
    print("=" * 80)

    # Download model (cached after first run)
    tokenizer, model = download_model()

    if tokenizer is None or model is None:
        print("\n[FAILED] Could not load model. Exiting.")
        return 1

    # Test proteins
    proteins = {
        "p62_PB1": "MEELTLEEVAREVSQEPGTESTQTPDQVAEQLCAMFGGTQAQFIMKIFENVPKQVSVVVRCPHCHSVCTKDCVCLSQEVVEMCGDCVATQENLCDCFDDLPG",
        "p62_UBA": "DELQWLKEHLELTTAASQQGHFPMSGTLQGDEDMQWAHQDLLAGTGAEVG",
        "PDL1_tail": "RMKPRSYSVSKGVVGDLAELLPQQLSIFFDNKSQSDVEAVDQDTSTKSIGSLPSSLNSSGNKSQSSTQDRH",
        "HIP1R_ANTH": "MSSKGDLDNLEARLNSLEKACRKMWEEVKQLQLDAAEFQLLCQEAFDQARFRGQKVENLQKDKEQQLEVQKKQLEELKKKLLEAEKEGKQEMKDDQRKVKELQEQVRELEKELQKLQQELQQQEKEQKLKQEKEKLKDDQLAELKEQVSKLEEELQVLQQDLEGQRQDLKEKQAELQKQKEQLEKDQEQLKEEQKEKEKDKEKLQEELQKLQQDLASQRQDLKEKQAELEKQKEQLEKDQEQLKEEQKEKLNVKSNSGTSYVRCQ"
    }

    results = {}

    # Run predictions
    for name, sequence in proteins.items():
        embedding, per_residue, variance = get_protein_embeddings(
            tokenizer, model, sequence, name
        )
        result = predict_llps_from_embedding(embedding, per_residue, variance)
        results[name] = result

    # Save results
    output_dir = Path("outputs/llps_predictions")
    output_dir.mkdir(parents=True, exist_ok=True)

    json_path = output_dir / "saprot_real_predictions.json"
    with open(json_path, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"\n[SAVE] Results saved: {json_path}")

    # Summary table
    print("\n" + "=" * 80)
    print("SUMMARY TABLE (Real SaProt Transformer)")
    print("=" * 80)
    print(f"{'Protein':<20} {'LLPS Score':>12} {'Disorder':>10} {'Heterogen':>12} {'Verdict':>10}")
    print("-" * 80)

    for name, res in results.items():
        print(f"{name:<20} {res['llps_score']:>12.3f} {res['disorder_score']:>10.3f} {res['heterogeneity_score']:>12.3f} {res['verdict']:>10}")

    print("=" * 80)

    print("\n[SUCCESS] Real SaProt inference complete!")
    print("\nNext steps:")
    print("  [ ] Compare with simplified predictions (saprot_llps_scores.json)")
    print("  [ ] Validate with experimental data (CD-CODE database)")
    print("  [ ] Train supervised classifier on known LLPS proteins")

    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except KeyboardInterrupt:
        print("\n\n[INTERRUPTED] Stopping...")
        sys.exit(1)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
