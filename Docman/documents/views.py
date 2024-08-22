from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .models import Document, DocumentType
from django.utils.html import mark_safe
from .forms import DocumentForm,DocumentFileFormSet
from django.contrib.admin.views.decorators import staff_member_required
from whoosh import index
from whoosh.qparser import QueryParser
from django.http import FileResponse, Http404
import os
import logging
from datetime import datetime
import zipfile
import io

logger = logging.getLogger('django')

@login_required
def document_create(request):
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        formset = DocumentFileFormSet(request.POST, request.FILES)

        if form.is_valid() and formset.is_valid():
            document = form.save(commit=False)
            document.user = request.user
            document.save()

            files = formset.save(commit=False)
            for file in files:
                file.document = document
                file.save()

            return redirect('document_list')
        else:
            print("Form errors:", form.errors)
            print("Formset errors:", formset.errors)

    else:
        form = DocumentForm()
        formset = DocumentFileFormSet()

    return render(request, 'documents/document_form.html', {'form': form, 'formset': formset})


@login_required
def document_list(request):
    documents = Document.objects.all()
    return render(request, 'documents/document_list.html', {'documents': documents})

@login_required
def document_detail(request, pk):
    document = get_object_or_404(Document, pk=pk)
    return render(request, 'documents/document_detail.html', {'document': document})

@staff_member_required
def document_delete(request, pk):
    document = get_object_or_404(Document, pk=pk)
    document.delete()
    return redirect('document_list')

@login_required
def document_edit(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if request.method == "POST":
        form = DocumentForm(request.POST, request.FILES, instance=document)
        if form.is_valid():
            form.save()
            return redirect('document_detail', pk=document.pk)
    else:
        form = DocumentForm(instance=document)
    return render(request, 'documents/document_edit.html', {'form': form})


@login_required
def search_documents(request):
    query = None
    results = []

    if 'query' in request.GET:
        query = request.GET.get('query')
        results = Document.objects.filter(
                Q(description__icontains=query))
    return render(request, 'documents/search_results.html', {'results': results, 'query': query})


@login_required
def download_document(request, pk):
    document = get_object_or_404(Document, pk=pk)
    if document.attached_file:
        current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        logger.info(f"{current_time} - Document downloaded: {document.title} by user {request.user.username}")
        response = FileResponse(document.attached_file.open(), as_attachment=True)
        return response
    else:
        raise Http404("Document does not have an attached file")

def download_document_files(request, document_id):
    document = get_object_or_404(Document, id=document_id)
    files = document.files.all()  # Получение всех файлов, связанных с документом

    # Создание zip-архива в памяти
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, 'w') as zip_file:
        for file_obj in files:
            file_path = file_obj.file.path
            file_name = file_obj.file.name.split('/')[-1]
            zip_file.write(file_path, file_name)
    
    buffer.seek(0)

    # Отправка архива как ответа
    response = HttpResponse(buffer, content_type='application/zip')
    response['Content-Disposition'] = f'attachment; filename={document.title}.zip'

    return response
