from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from .utils import (
    download_pdf_from_url,
    process_pdf_file,
    download_pdf_from_drive,
)
import os


def download_pdf(request, url):
    file_name = download_pdf_from_url(url)

    if file_name:
        # Do something with the downloaded file, like serving it as a response or further processing
        metadata = process_pdf_file(file_name)
        try:
            os.remove(file_name)
        except OSError as e:
            print(f"Error deleting file: {e}")

        if metadata:
            # You can customize the response format as needed
            response_data = {
                "title": metadata["title"],
                "authors": metadata["authors"],
                "institutions": metadata["institutions"],
                "keywords": metadata["keywords"],
                "abstract": metadata["abstract"],
                "text": metadata["text"],
                "references": metadata["references"],
            }

            # Return the metadata as a JSON response
            return JsonResponse(response_data)
        else:
            return HttpResponse("Failed to extract metadata.", status=500)

    else:
        return HttpResponse("Failed to download the file.", status=500)


def download_pdf_drive(request, id):
    full_url = f"https://drive.google.com/uc?export=download&id={id}"
    file_name = download_pdf_from_drive(full_url)
    if file_name:
        # Do something with the downloaded file, like serving it as a response or further processing
        metadata = process_pdf_file(file_name)
        try:
            os.remove(file_name)
        except OSError as e:
            print(f"Error deleting file: {e}")

        if metadata:
            # You can customize the response format as needed
            response_data = {
                "title": metadata["title"],
                "authors": metadata["authors"],
                "institutions": metadata["institutions"],
                "keywords": metadata["keywords"],
                "abstract": metadata["abstract"],
                "text": metadata["text"],
                "references": metadata["references"],
            }

            # Return the metadata as a JSON response
            return JsonResponse(response_data)
        else:
            return HttpResponse("Failed to extract metadata.", status=500)

    else:
        return HttpResponse("Failed to download the file.", status=500)
