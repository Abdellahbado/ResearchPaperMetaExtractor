import os
import requests
import xmltodict
import pdfplumber
import yake
from urllib.parse import urlparse, parse_qs
from pdfrw import PdfReader


def download_pdf_from_drive(url):
    response = requests.get(url)

    if response.status_code == 200:
        # Check if "id=" is present in the URL
        if "id=" in url:
            file_id = url.split("id=")[1]
            # Use the file ID as the file name with .pdf extension
            file_name = f"{file_id}.pdf"
            with open(file_name, "wb") as f:
                f.write(response.content)
                print(f"File '{file_name}' has been downloaded and saved.")
            return file_name
        else:
            print("Error: 'id=' not found in the URL.")
            return None
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")
        return None

def extract_keywords(pdf_path, num_keywords):
    with pdfplumber.open(pdf_path) as pdf:
        text = ""
        for page in pdf.pages:
            text += page.extract_text()

    kw_extractor = yake.KeywordExtractor(top=num_keywords, stopwords=None)
    keywords = kw_extractor.extract_keywords(text)
    keyword_strings = [kw for kw, _ in keywords]
    return keyword_strings


def download_pdf_from_url(url):
    response = requests.get(url)

    if response.status_code == 200:
        file_name = os.path.basename(url)

        with open(file_name, "wb") as f:
            f.write(response.content)
            print(f"File '{file_name}' has been downloaded and saved.")
        return file_name
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")
        return None


def extract_pdf_keywords_and_creation_date(pdf_file_path):
    with pdfplumber.open(pdf_file_path) as pdf:
        metadata = pdf.metadata

    keywords = metadata.get("Keywords", "")
    keywords_list = (
        [keyword.strip() for keyword in keywords.split(",")] if keywords else []
    )
    creation_date_str = metadata.get("CreationDate", "")
    creation_date_dict = {}
    if creation_date_str:
        # Extracting year, month, day from the string
        year = creation_date_str[2:6]
        month = creation_date_str[6:8]
        day = creation_date_str[8:10]
        creation_date_dict = {"year": year, "month": month, "day": day}

    return keywords_list, creation_date_dict



def process_pdf_file(pdf_path):
    # Set the URL for the CERMINE REST service
    cermine_url = "http://localhost:8072/extract.do"

    # Prepare the data for the POST request
    files = {"file": open(pdf_path, "rb")}
    headers = {"Content-Type": "application/binary"}

    # Make the request
    response = requests.post(cermine_url, files=files, headers=headers)

    # Check the response status
    if response.status_code == 200:
        # Convert XML response to JSON
        cermine_json = xmltodict.parse(response.text)
        new_dict = cermine_json["article"]["front"]["article-meta"]
        contrib_group = new_dict.get("contrib-group", {})
        affiliation = contrib_group.get("aff")

        if affiliation is not None:
            if not isinstance(affiliation, list):
                contrib_group["aff"] = [affiliation]
        else:
            # Handle the case when 'aff' key is missing or None
            contrib_group["aff"] = ["No institutions available"]

        if not isinstance(new_dict["contrib-group"]["aff"], list):
            new_dict["contrib-group"]["aff"] = [new_dict["contrib-group"]["aff"]]

        authors = []
        if "contrib-group" in new_dict and "contrib" in new_dict["contrib-group"]:
            if isinstance(new_dict["contrib-group"]["contrib"], list):
                authors = [
                    author["string-name"]
                    for author in new_dict["contrib-group"]["contrib"]
                ]
            else:
                authors = [new_dict["contrib-group"]["contrib"]["string-name"]]
        else:
            authors = []
        keywords, creation_date = extract_pdf_keywords_and_creation_date(pdf_path)
        metadata = {
            "title": new_dict.get("title-group", {}).get(
                "article-title", "Unknown Title"
            ),
            "authors": authors,
            "institutions": [
                aff.get("institution") if isinstance(aff, dict) else {"name": aff}
                for aff in new_dict.get("contrib-group", {}).get("aff", [])
            ],
            "abstract": new_dict.get("abstract", {}).get("p", "No abstract available"),
        }

        metadata["pub-date"] = creation_date
        # Access attributes directly without using json.dumps
        text_dict = cermine_json["article"]["body"]

        text = " ".join(
            f"{sec_elem['title']} {' '.join(p_elem.get('#text', '') if isinstance(p_elem, dict) and '#text' in p_elem else p_elem for p_elem in sec_elem.get('p', []))}"
            for sec_elem in text_dict["sec"]
        )
        cleaned_text = text.replace("[\n        \n        ]", "")

        # Print the cleaned text
        metadata["text"] = cleaned_text

        # Print the metadata with the added 'text' attribute
        ref_list = (
            cermine_json.get("article", {})
            .get("back", {})
            .get("ref-list", {})
            .get("ref", [])
        )

        references = ref_list[:3] if isinstance(ref_list, list) else []
        reference_strings = []
        for reference in references:
            # Check if 'string-name' and 'mixed-citation' keys are present
            if (
                "string-name" in reference["mixed-citation"]
                and "article-title" in reference["mixed-citation"]
            ):
                names = reference["mixed-citation"]["string-name"]
                authors = ", ".join(
                    [
                        (
                            f"{name.get('given-names', '')} {name.get('surname', '')}"
                            if isinstance(name, dict)
                            else name
                        )
                        for name in names
                    ]
                )

                article_title = reference["mixed-citation"]["article-title"]
                source = reference["mixed-citation"].get("source", "")
                year = reference["mixed-citation"].get("year", "")

                reference_string = f"{authors}, '{article_title}', {source}, {year}"
                reference_strings.append(reference_string)

        # Printing the result
        metadata["references"] = reference_strings
        metadata["keywords"] = extract_keywords(pdf_path, 20)
        metadata["keywords"] += keywords
        return metadata

    else:
        # Print an error message
        print(f"Error: {response.status_code} - {response.text}")
