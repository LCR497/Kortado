from django import forms
from .models import Document,DocumentFile
from django.forms import inlineformset_factory
class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'description', 'attached_file', 'document_type']
        labels = {
            'title': 'Название документа',
            'description': 'Описание',
            'attached_file': 'Прикрепленный файл',
            'document_type': 'Тип документа',
        }

class DocumentFileForm(forms.ModelForm):
    class Meta:
        model = DocumentFile
        fields = ['file']

DocumentFileFormSet = inlineformset_factory(Document, DocumentFile, form=DocumentFileForm, extra=1)