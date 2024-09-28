from django.urls import path, include
from rest_framework import routers
from .views import DocumentUploadView, SingleDocumentView


# router = routers.DefaultRouter()
# router.register(r'docs', DocumentUploadView, 'doc')

urlpatterns = [
   path('documents/', DocumentUploadView.as_view(), name='upload-document'),
   path('documents/<int:id>/', SingleDocumentView.as_view(), name='document-detail'),
    #path('', include(router.urls)),
]

