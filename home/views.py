from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from .models import Document
from django.http import HttpResponse
from .utils import extract_text_from_image
from .models import Document, DocumentVerification
from django.shortcuts import render, get_object_or_404, redirect
from .utils import verify_document


def home (request):
    return render (request, 'index.html')

def about (request):
    return render (request, 'about.html')

def upload(request):
    if request.method == 'POST':
        document_name = request.POST.get('document_name')
        document_type = request.POST.get('document_type')
        uploaded_file = request.FILES['document']

        document = Document.objects.create(
            document_name=document_name,
            document_type=document_type,
            uploaded_file=uploaded_file,
        )
        document.save()
        
        return redirect('text_extraction', document_name=document_name)  # Redirect to text extraction page

    return render(request, 'upload.html')


def verify (request):
    documents = Document.objects.all()
   
    return render (request, 'verification.html', {'documents': documents})


def text_extraction(request, document_name):
    document = Document.objects.get(document_name=document_name)

    if request.method == 'POST':
        # Perform OCR and save extracted text
        text = extract_text_from_image(document.uploaded_file.path)
        
        if text:
            document.extracted_text = text
            document.save()
            
            # Extract specific fields from the text
            name = text.get('certificate_name', '')
            cert_number = text.get('certificate_number', '')
            
            # Pass the extracted fields to the template
            context = {
                'document_name': document_name,
                'name': name,
                'cert_number': cert_number
            }

            return render(request, 'extraction_result.html', context)

    return render(request, 'text_extraction.html', {'document': document})



def verify_document_view(request):
    if request.method == 'POST':
        print("POST request received.")

        document_id = request.POST.get('document_id')
        print(f"Document ID received: {document_id}")

        document = get_object_or_404(Document, id=document_id)
        print(f"Document retrieved: {document}")

        # Extract details from the document
        extracted_text = eval(document.extracted_text)  # Convert string to dictionary
        print(f"Extracted text: {extracted_text}")

        owner_name = extracted_text.get('certificate_name', '').strip()
        cert_number = extracted_text.get('certificate_number', '').strip()
        print(f"Owner Name: {owner_name}, Certificate Number: {cert_number}")

        # Verify the document
        status, verification_record = verify_document(owner_name, cert_number)
        print(f"Verification status: {status}, Verification record: {verification_record}")

        # Update document verification status
        document.is_verified = (status == "Verified")
        document.save()
        print(f"Document verification status updated: {document.is_verified}")

        # Redirect to the page that shows the updated list of documents
        return redirect('verify')  # Adjust URL name if needed
    
    print("Request method is not POST. Redirecting to home.")
    return redirect('home')  # Redirect if the request method is not POST



def compare_document_details():
    # Fetch details from the Document model
    documents = Document.objects.all()  # Adjust query as needed

    results = []
    for doc in documents:
        # Assuming extracted_text is a dictionary
        extracted_text = eval(doc.extracted_text)  # Convert string to dictionary if stored as string
        owner_name = extracted_text.get('certificate_name', '').strip()
        cert_number = extracted_text.get('certificate_number', '').strip()

        # Verify the extracted details
        status, verification_record = verify_document(owner_name, cert_number)
        results.append({
            'document_name': doc.document_name,
            'owner_name': owner_name,
            'cert_number': cert_number,
            'status': status,
            'verification_record': verification_record
        })
    
    return results


def view_verification_results(request):
    results = compare_document_details()
    return render(request, 'verification_results.html', {'results': results})


