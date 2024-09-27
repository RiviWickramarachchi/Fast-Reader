from django.shortcuts import render

# Create your views here.
# documents/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Document
from .serializer import DocumentSerializer
import docx
import pdfplumber

class DocumentUploadView(APIView):

    def get(self,request):
        queryset = Document.objects.all()  # Get all Document objects
        serializer = DocumentSerializer(queryset, many=True)  # Serialize the data
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        # Deserialize the incoming request data
        file_serializer = DocumentSerializer(data=request.data)
        if file_serializer.is_valid():
            file_serializer.save()

            # Process the file after saving it
            file_instance = file_serializer.instance
            content = self.process_file(file_instance.file)

            return Response({"message": "File uploaded successfully", "content": content}, status=status.HTTP_201_CREATED)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def process_file(self, file):
        # Determine if the file is Word or PDF and process accordingly
        file_name = file.name.lower()

        if file_name.endswith('.docx'):
            return self.read_docx(file)
        elif file_name.endswith('.pdf'):
            return self.read_pdf(file)

        return "Unsupported file format"

    def read_docx(self, file):
        # Extract text from Word (.docx) file
        doc = docx.Document(file)
        full_text = [paragraph.text for paragraph in doc.paragraphs]
        return "\n".join(full_text)

    def read_pdf(self, file):
        # Extract text from PDF file using pdfplumber
        full_text = ""
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                full_text += page.extract_text() + "\n"
        return full_text