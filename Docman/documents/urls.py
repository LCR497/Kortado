from django.urls import path
from . import views

urlpatterns = [
    path('', views.document_list, name='document_list'),
    path('create/', views.document_create, name='document_create'),
    path('document/<int:pk>/', views.document_detail, name='document_detail'),
    path('document/<int:pk>/edit/', views.document_edit, name='document_edit'),
    path('document/<int:pk>/delete/', views.document_delete, name='document_delete'),
    path('document/<int:pk>/download/', views.download_document, name='download_document'),
    path('document/<int:document_id>/download/', views.download_document_files, name='download_document_files'), 
    path('search/', views.search_documents, name='search_documents'),
]
