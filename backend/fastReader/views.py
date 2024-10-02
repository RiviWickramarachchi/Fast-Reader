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

             # Get the file from the request data (without saving it to the database)
            
            file = request.data.get('file')
            common_methods = CommonMethods()
            content, isReadable = common_methods.process_file(file)

            #Save the file if it is in a readable format
            if(isReadable):
                file_instance = file_serializer.save()
                id = file_instance.id
                return Response({"message": "File uploaded successfully", "content": id}, status=status.HTTP_201_CREATED)
            else:
                return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(file_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SingleDocumentView(APIView):
    def get(self, request, id, *args, **kwargs):

        #GET request to return a single Document object by its ID.
        try:
            document = Document.objects.get(pk=id)  # Get the document by ID
            file = document.file #get the file data from the object
            common_methods = CommonMethods()
            words, isReadable = common_methods.process_file(file) #convert the file to readable format
            return Response( {"data": words} , status=status.HTTP_200_OK)
        except Document.DoesNotExist:
            return Response({"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND)
    def delete(self, request, id=None, *args, **kwargs):
        try:
            document = Document.objects.get(pk=id)
            document.delete()
            return Response({"message": "Document deleted successfully!"}, status=status.HTTP_204_NO_CONTENT)
        except Document.DoesNotExist:
            return Response({"error": "Document not found!"}, status=status.HTTP_404_NOT_FOUND)

class CommonMethods():
     def process_file(self, file):
        # Determine if the file is Word or PDF and process accordingly
        file_name = file.name.lower()

        if file_name.endswith('.docx'):
            return self.read_docx(file), True
        elif file_name.endswith('.pdf'):
            return self.read_pdf(file), True

        return "Unsupported file format", False
     def read_docx(self, file):

        single_text_arr = []
        # Extract text from Word (.docx) file
        doc = docx.Document(file)
        full_text = [paragraph.text for paragraph in doc.paragraphs]
        #formatted_text.extend(full_text.splitlines())
        for element in full_text:
            single_text_arr.extend(element.split())
        #print(single_text_arr)
        return single_text_arr

     def read_pdf(self, file):
        # Extract text from PDF file using pdfplumber
        full_text = ""
        formatted_text = []
        single_text_arr =[]
        with pdfplumber.open(file) as pdf:
            for page in pdf.pages:
                #full_text += page.extract_text() + "\n"
                full_text += page.extract_text()
                formatted_text.extend(full_text.splitlines())
            for element in formatted_text:
                single_text_arr.extend(element.split())
            print(single_text_arr)
        return single_text_arr

     #write a function to support text files
