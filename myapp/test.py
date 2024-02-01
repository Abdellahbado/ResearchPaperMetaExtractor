from django.test import TestCase
from unittest.mock import patch, MagicMock
import os


class MyAppTests(TestCase):
    @patch("requests.get")
    def test_download_pdf_from_drive(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"Test PDF content"
        mock_get.return_value = mock_response

        from myapp.utils import download_pdf_from_drive

        file_name = download_pdf_from_drive("mock_url")

        self.assertIsNone(file_name)  # Assert None when 'id=' not found

    @patch("pdfplumber.open")
    def test_extract_keywords(self, mock_open):
        mock_pdf = MagicMock()
        mock_pdf.pages = [MagicMock()]
        mock_pdf.pages[0].extract_text.return_value = "This is a mock PDF text"
        mock_open.return_value.__enter__.return_value = mock_pdf

        from myapp.utils import extract_keywords

        keywords = extract_keywords("mock_pdf_path", 5)

        self.assertEqual(len(keywords), 5)

    @patch("pdfplumber.open")
    @patch("fitz.open")
    def test_extract_publication_date(self, mock_fitz_open, mock_pdf_open):
        mock_doc = MagicMock()
        mock_doc.metadata = {"created": "D:20230101120000"}
        mock_fitz_open.return_value = mock_doc

        from myapp.utils import extract_publication_date

        pub_date = extract_publication_date("mock_pdf_path")

        self.assertEqual(pub_date["day"], 1)
        self.assertEqual(pub_date["month"], "January")
        self.assertEqual(pub_date["year"], 2023)

    @patch("requests.get")
    def test_download_pdf_from_url(self, mock_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"Test PDF content"
        mock_get.return_value = mock_response

        from myapp.utils import download_pdf_from_url

        file_name = download_pdf_from_url("mock_url")

        self.assertIsNotNone(file_name)
        self.assertTrue(os.path.exists(file_name))

        os.remove(file_name)
