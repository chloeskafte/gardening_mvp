#!/usr/bin/env python3
"""
Example usage of the PDF text extractor for gardening guides.
This script demonstrates how to use the fitz library to extract text from PDFs.
"""

import fitz
import os

def simple_extract_example(pdf_path):
    """
    Simple example of extracting text from a PDF using fitz.
    
    Args:
        pdf_path (str): Path to the PDF file
    """
    print(f"Opening PDF: {pdf_path}")
    
    # Open the PDF document
    doc = fitz.open(pdf_path)
    
    print(f"PDF has {len(doc)} pages")
    
    # Extract text from first page as an example
    if len(doc) > 0:
        first_page = doc.load_page(0)
        text = first_page.get_text()
        
        print("\n--- First Page Text ---")
        print(text[:300] + "..." if len(text) > 300 else text)
    
    # Close the document
    doc.close()

def extract_all_pages(pdf_path):
    """
    Extract text from all pages of a PDF.
    
    Args:
        pdf_path (str): Path to the PDF file
    """
    doc = fitz.open(pdf_path)
    
    all_text = ""
    for page_num in range(len(doc)):
        page = doc.load_page(page_num)
        page_text = page.get_text()
        all_text += f"\n--- Page {page_num + 1} ---\n"
        all_text += page_text
    
    doc.close()
    
    # Save to file
    output_file = f"{os.path.splitext(os.path.basename(pdf_path))[0]}_full_text.txt"
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(all_text)
    
    print(f"Full text saved to: {output_file}")
    return all_text

if __name__ == "__main__":
    # Example usage - replace with your actual PDF path
    pdf_file = "indolent_kitchen_gardening.pdf"  # Replace with your PDF file
    
    if os.path.exists(pdf_file):
        print("=== Simple Extraction Example ===")
        simple_extract_example(pdf_file)
        
        print("\n=== Full Extraction Example ===")
        extract_all_pages(pdf_file)
    else:
        print(f"PDF file '{pdf_file}' not found.")
        print("Please place your gardening guide PDF in the same directory and update the filename in this script.") 