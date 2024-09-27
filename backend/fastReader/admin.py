from django.contrib import admin
from .models import Document


class DocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'file', 'uploaded_at')


# Register your models here.
admin.site.register(Document, DocumentAdmin)