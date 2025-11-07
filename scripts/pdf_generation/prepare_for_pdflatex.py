#!/usr/bin/env python3
"""
預處理 Markdown 檔案，將 Unicode 字元轉換為 LaTeX 命令
以便 pdflatex 可以正確處理
"""
import re
import sys

def convert_unicode_to_latex(text):
    """將常見的 Unicode 字元轉換為 LaTeX 命令"""

    # 首先處理科學記號格式（在單字符替換之前）

    # 格式 1: 數字×10^數字^ (使用 ^...^ 作為上標)
    # 例如: 2.3×10^-68^ -> $2.3\times10^{-68}$
    sci_notation_caret = r'(\d+\.?\d*)\s*×\s*10\^([^$\^]+)\^'
    text = re.sub(sci_notation_caret, r'$\1\\times10^{\2}$', text)

    # 格式 2: 數字×10<sup>數字</sup> (使用 HTML sup 標籤)
    # 例如: 2.3×10<sup>-68</sup> -> $2.3\times10^{-68}$
    sci_notation_html = r'(\d+\.?\d*)\s*×\s*10<sup>([^<]+)</sup>'
    text = re.sub(sci_notation_html, r'$\1\\times10^{\2}$', text)

    # 格式 3: 數字×10上標數字 (使用 Unicode 上標字符)
    # 例如: 2.3×10⁻⁶⁸ -> $2.3\times10^{-68}$
    sci_notation_unicode = r'(\d+\.?\d*)\s*×\s*10([⁻⁰¹²³⁴⁵⁶⁷⁸⁹]+)'

    def convert_superscript(match):
        """將 Unicode 上標數字轉換為普通數字"""
        superscript_map = {
            '⁻': '-', '⁰': '0', '¹': '1', '²': '2', '³': '3',
            '⁴': '4', '⁵': '5', '⁶': '6', '⁷': '7', '⁸': '8', '⁹': '9'
        }
        coefficient = match.group(1)
        exponent = match.group(2)
        # 轉換上標為普通數字
        normal_exp = ''.join(superscript_map.get(c, c) for c in exponent)
        return f'${coefficient}\\times10^{{{normal_exp}}}$'

    text = re.sub(sci_notation_unicode, convert_superscript, text)

    # 希臘字母 - 使用 \ensuremath 確保在任何環境下都可以正確渲染
    replacements = {
        'ρ': r'\ensuremath{\rho}',
        'α': r'$\alpha$',
        'β': r'$\beta$',
        'γ': r'$\gamma$',
        'δ': r'$\delta$',
        'ε': r'$\varepsilon$',
        'θ': r'$\theta$',
        'κ': r'$\kappa$',  # 添加 kappa
        'λ': r'$\lambda$',
        'μ': r'$\mu$',
        'π': r'$\pi$',
        'σ': r'$\sigma$',
        'τ': r'$\tau$',
        'φ': r'$\phi$',
        'χ': r'$\chi$',
        'ψ': r'$\psi$',
        'ω': r'$\omega$',

        # 上標數字 (剩餘的單獨上標，不在科學記號中)
        '⁻': r'$^{-}$',
        '⁰': r'$^{0}$',
        '¹': r'$^{1}$',
        '²': r'$^{2}$',
        '³': r'$^{3}$',
        '⁴': r'$^{4}$',
        '⁵': r'$^{5}$',
        '⁶': r'$^{6}$',
        '⁷': r'$^{7}$',
        '⁸': r'$^{8}$',
        '⁹': r'$^{9}$',

        # 其他符號（剩餘的 × 符號，不在科學記號中）
        '×': r'$\times$',
        '±': r'$\pm$',
        '≤': r'$\leq$',
        '≥': r'$\geq$',
        '≠': r'$\neq$',
        '≈': r'$\approx$',
        '∼': r'$\sim$',
        '→': r'$\rightarrow$',
        '←': r'$\leftarrow$',
        '↔': r'$\leftrightarrow$',
        '∞': r'$\infty$',

        # 特殊字元
        '°': r'$^\circ$',
        '′': r'$^\prime$',
        '″': r'$^{\prime\prime}$',

        # 分數和其他
        '½': r'$\frac{1}{2}$',
        '¼': r'$\frac{1}{4}$',
        '¾': r'$\frac{3}{4}$',
    }

    for unicode_char, latex_cmd in replacements.items():
        text = text.replace(unicode_char, latex_cmd)

    # 處理 <sup> HTML 標籤（轉為 LaTeX 上標）
    text = re.sub(r'<sup>([^<]+)</sup>', r'$^{\1}$', text)

    return text

def main():
    input_file = 'paper/MANUSCRIPT_bioRxiv_FIXED.md'
    output_file = 'paper/MANUSCRIPT_bioRxiv_FOR_PDFLATEX.md'

    print(f"讀取: {input_file}")
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()

    print("轉換 Unicode 字元為 LaTeX 命令...")
    converted = convert_unicode_to_latex(content)

    print(f"寫入: {output_file}")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(converted)

    print("✓ 轉換完成！")

    # 統計
    original_unicode = len([c for c in content if ord(c) > 127])
    converted_unicode = len([c for c in converted if ord(c) > 127])
    print(f"  原始 Unicode 字元: {original_unicode}")
    print(f"  轉換後剩餘: {converted_unicode}")
    print(f"  已轉換: {original_unicode - converted_unicode}")

if __name__ == '__main__':
    main()
