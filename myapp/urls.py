from django.urls import path
from .views import download_pdf, download_pdf_drive

urlpatterns = [
    path("url/<path:url>/", download_pdf, name="download_pdf"),
    path("drive/<str:id>/", download_pdf_drive, name="download_pdf_drive"),
]
