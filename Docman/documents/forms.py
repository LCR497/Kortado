from django import forms
from .models import Document, DocumentFile

class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ['title', 'description', 'document_type', 'attached_file']

class DocumentFileForm(forms.ModelForm):
    class Meta:
        model = DocumentFile
        fields = ['file']

DocumentFileFormSet = forms.inlineformset_factory(
    Document, DocumentFile, form=DocumentFileForm, extra=1, can_delete=True
)