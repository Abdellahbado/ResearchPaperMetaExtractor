from django.test import TestCase
from unittest.mock import patch, MagicMock
import os
from myapp.utils import download_pdf_from_drive


class MyAppTests(TestCase):
    @patch("requests.get")
    def test_download_pdf_from_drive(self, mock_get):
        # Prepare mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.content = b"Test PDF content"
        mock_get.return_value = mock_response

        # Define test URL with 'id' parameter
        test_url_with_id = "https://example.com/download?id=123"

        # Call the function being tested
        file_name = download_pdf_from_drive(test_url_with_id)

        # Assert file name is not None
        self.assertIsNotNone(file_name)

        # Verify file name
        expected_file_name = "123.pdf"
        self.assertEqual(file_name, expected_file_name)

        # Verify file content
        with open(file_name, "rb") as f:
            file_content = f.read()
        self.assertEqual(file_content, b"Test PDF content")

        # Clean up: remove the downloaded file
        os.remove(file_name)

    @patch("pdfplumber.open")
    def test_extract_keywords(self, mock_open):
        mock_pdf = MagicMock()
        mock_pdf.pages = [MagicMock()]
        mock_pdf.pages[0].extract_text.return_value = "This is a mock PDF text"
        mock_open.return_value.__enter__.return_value = mock_pdf

        from myapp.utils import extract_keywords

        keywords = extract_keywords("mock_pdf_path", 5)

        self.assertEqual(len(keywords), 5)

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
