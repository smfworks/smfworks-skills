# PDF Toolkit — Quick Reference

## Install
```bash
smfw install pdf-toolkit
```

## Commands
```bash
python main.py merge output.pdf input1.pdf input2.pdf         # Merge PDFs
python main.py split input.pdf ./output/                       # Split into pages
python main.py extract input.pdf 1 5 output.pdf              # Extract pages 1-5
python main.py info document.pdf                              # Show PDF info
python main.py compress input.pdf output.pdf                   # Compress PDF
python main.py rotate input.pdf output.pdf 90                 # Rotate 90°
```

## Common Examples
```bash
# Merge two PDFs
python main.py merge combined.pdf chapter1.pdf chapter2.pdf

# Split PDF into individual pages
python main.py split big.pdf ./pages/

# Extract pages 1-5
python main.py extract report.pdf 1 5 extracted.pdf

# Get PDF info
python main.py info document.pdf
```

## Help
```bash
python main.py --help
python main.py merge --help
```
