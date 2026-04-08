from django.urls import path
from document.views.documentCategoriesView import DocumentCategoriesView
from document.views.hrDocumentView import HRDocumentView
from document.views.acknowledgementView import AcknowledgementView
from document.views.documentTemplateView import documentTemplateView

urlpatterns = [
    path('document-categories', DocumentCategoriesView.as_view(), name='document-categories'),
    path('document-categories/<int:pk>', DocumentCategoriesView.as_view(), name='document-categories-update'),
    path('hr-document', HRDocumentView.as_view(), name='hr-document'),
    path('hr-document/<int:pk>', HRDocumentView.as_view(), name='hr-document-update'),
    path('acknowledgement', AcknowledgementView.as_view(), name='acknowledgement'),
    path('acknowledgement/<int:pk>', AcknowledgementView.as_view(), name='acknowledgement-update'),
    path('document-template', documentTemplateView.as_view(), name='document-template'),
    path('document-template/<int:pk>', documentTemplateView.as_view(), name='document-template-update'),
]