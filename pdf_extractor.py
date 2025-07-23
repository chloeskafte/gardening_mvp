import fitz  # PyMuPDF
import os
import sys

def extract_text_from_pdf(pdf_path):
    """
    Extract text from a PDF file using PyMuPDF (fitz).
    
    Args:
        pdf_path (str): Path to the PDF file
        
    Returns:
        str: Extracted text from the PDF
    """
    try:
        # Open the PDF document
        doc = fitz.open(pdf_path)
        
        # Initialize text variable
        full_text = ""
        
        # Iterate through each page
        for page_num in range(len(doc)):
            page = doc.load_page(page_num)
            
            # Extract text from the page
            page_text = page.get_text()
            full_text += f"\n--- Page {page_num + 1} ---\n"
            full_text += page_text
            
        # Close the document
        doc.close()
        
        return full_text
        
    except Exception as e:
        print(f"Error extracting text from PDF: {e}")
        return None

def save_text_to_file(text, output_path):
    """
    Save extracted text to a file.
    
    Args:
        text (str): Text to save
        output_path (str): Path where to save the text file
    """
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(text)
        print(f"Text saved to: {output_path}")
    except Exception as e:
        print(f"Error saving text to file: {e}")

def main():
    """
    Main function to run the PDF text extraction.
    """
    # Check if PDF path is provided as command line argument
    if len(sys.argv) < 2:
        print("Usage: python pdf_extractor.py <path_to_pdf>")
        print("Example: python pdf_extractor.py gardening_guide.pdf")
        return
    
    pdf_path = sys.argv[1]
    
    # Check if file exists
    if not os.path.exists(pdf_path):
        print(f"Error: File '{pdf_path}' not found.")
        return
    
    print(f"Extracting text from: {pdf_path}")
    
    # Extract text from PDF
    extracted_text = extract_text_from_pdf(pdf_path)
    
    if extracted_text:
        # Create output filename
        base_name = os.path.splitext(os.path.basename(pdf_path))[0]
        output_path = f"{base_name}_extracted.txt"
        
        # Save extracted text to file
        save_text_to_file(extracted_text, output_path)
        
        # Print first 500 characters as preview
        print("\n--- Text Preview (first 500 characters) ---")
        print(extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text)
        
    else:
        print("Failed to extract text from PDF.")

if __name__ == "__main__":
    main() 