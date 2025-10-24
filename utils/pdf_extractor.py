"""
PDF Extractor - Extract text from PDF files
Uses PyMuPDF (fitz) for text extraction
"""

import logging
import fitz  # PyMuPDF

logger = logging.getLogger("pdf_extractor")


def extract_text_from_pdf(pdf_path: str) -> str:
    """
    Extract text content from a PDF file
    
    Args:
        pdf_path: Path to the PDF file
    
    Returns:
        Extracted text content
    
    Raises:
        Exception: If extraction fails
    """
    try:
        logger.info(f"Extracting text from PDF: {pdf_path}")
        
        # Open PDF
        doc = fitz.open(pdf_path)
        
        # Extract text from all pages
        text_content = []
        for page_num in range(len(doc)):
            page = doc[page_num]
            text = page.get_text()
            text_content.append(text)
        
        doc.close()
        
        # Combine all pages
        full_text = "\n".join(text_content)
        
        logger.info(f"Successfully extracted {len(full_text)} characters from PDF")
        return full_text
        
    except Exception as e:
        error_msg = f"Failed to extract text from PDF: {str(e)}"
        logger.error(error_msg)
        return f"[Error extracting text: {str(e)}]"


def validate_pdf(pdf_path: str) -> bool:
    """
    Validate if a file is a valid PDF
    
    Args:
        pdf_path: Path to the PDF file
    
    Returns:
        True if valid PDF, False otherwise
    """
    try:
        doc = fitz.open(pdf_path)
        doc.close()
        return True
    except Exception:
        return False
