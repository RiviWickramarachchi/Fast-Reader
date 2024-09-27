from django.urls import path, include
from rest_framework import routers
from .views import DocumentUploadView


# router = routers.DefaultRouter()
# router.register(r'docs', DocumentUploadView, 'doc')

urlpatterns = [
   path('documents/', DocumentUploadView.as_view(), name='upload-document')
    #path('', include(router.urls)),
]

