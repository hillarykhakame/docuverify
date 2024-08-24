from PIL import Image
import pytesseract
from .models import DocumentVerification

# Set the path to the Tesseract-OCR executable
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(image_path):
    """
    Extracts text, name, and certificate number from the provided image path.
    """
    try:
        image = Image.open(image_path)
        extracted_text = pytesseract.image_to_string(image)
        
        # Initialize variables for name and certificate number
        name = 'Not Found'
        cert_no = 'Not Found'
        
        # Split the text into lines for easier processing
        lines = extracted_text.splitlines()
        lines = [line.strip() for line in lines if line.strip()]  # Clean up any empty lines
        
        # Detect and extract name and certificate number based on pattern
        for i, line in enumerate(lines):
            # Look for "This is to certify that" or similar phrases
            if "This is to certify that" in line:
                # Check the next line for the name
                if i + 1 < len(lines):
                    name_candidate = lines[i + 1].strip()
                    # Simple validation: Ensure it's not another sentence or too short
                    if len(name_candidate.split()) >= 2:  # Expecting at least a first and last name
                        name = name_candidate
            # Extract the certificate number
            if "Cert No:" in line:
                cert_no = line.split("Cert No:")[1].strip()

        # Return the extracted data in a dictionary
        return {
            
            'certificate_name': name,
            'certificate_number': cert_no
        }

    except Exception as e:
        print(f"Error extracting text from image: {e}")
        return {
            'extracted_text': '',
            'certificate_name': 'Not Found',
            'certificate_number': 'Not Found'
        }

def verify_document(owner_name, cert_number):
    """
    Verify if the document with the given owner name and certificate number exists in the DocumentVerification model.
    """
    try:
        # Query the DocumentVerification model to find a matching record
        verification_record = DocumentVerification.objects.get(owner_name=owner_name, cert_number=cert_number)
        return "Verified", verification_record
    except DocumentVerification.DoesNotExist:
        # If no record is found, return 'Not Verified'
        return "Not Verified", None