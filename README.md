# Gardening MVP - PDF Text Extraction

Extract text from gardening guide PDFs using PyMuPDF (fitz) library.

## Features
- PDF text extraction using PyMuPDF (fitz)
- Extract text from all pages or specific pages
- Save extracted text to files
- Simple command-line interface

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Method 1: Command Line Interface
```bash
python pdf_extractor.py your_gardening_guide.pdf
```

This will:
- Extract text from all pages
- Save the text to `your_gardening_guide_extracted.txt`
- Show a preview of the first 500 characters

### Method 2: Using the Example Script
1. Place your PDF file in the project directory
2. Update the filename in `example_usage.py`:
   ```python
   pdf_file = "your_actual_file.pdf"
   ```
3. Run the example:
   ```bash
   python example_usage.py
   ```

### Method 3: Direct fitz Usage
```python
import fitz

# Open PDF
doc = fitz.open("your_gardening_guide.pdf")

# Extract text from first page
first_page = doc.load_page(0)
text = first_page.get_text()
print(text)

# Extract from all pages
all_text = ""
for page_num in range(len(doc)):
    page = doc.load_page(page_num)
    all_text += page.get_text()

doc.close()
```

## Key fitz Functions Used

- `fitz.open(pdf_path)` - Open a PDF document
- `doc.load_page(page_num)` - Load a specific page
- `page.get_text()` - Extract text from a page
- `len(doc)` - Get total number of pages
- `doc.close()` - Close the document

## Output

The extracted text will be saved as a `.txt` file with page separators:
```
--- Page 1 ---
[Page 1 content]

--- Page 2 ---
[Page 2 content]
...
```
