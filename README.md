### Django Metadata Extraction API - Extract Metadata from PDFs Online or from Open Drive

This Django application provides a powerful and user-friendly API to extract various metadata elements (title, authors, institutions, abstract, text, references, publication date, keywords) from PDF documents, leveraging both online sources and OpenDrive storage connectivity. It partially integrates the Cermine API (accessed via its Docker container) for exceptional metadata extraction capabilities.

Key Features:

- Versatile Metadata Extraction: Extract comprehensive metadata from diverse PDF sources, including title, authors, institutions, abstract, full text, references, publication date, and keywords.
Multiple Source Options: Process PDFs hosted online via URLs or conveniently access them from your OpenDrive account for seamless workflow.
- RESTful API Endpoint: Interact with the application programmatically through a well-defined and accessible RESTful API endpoint.
- JSON Output: Receive extracted metadata in a structured JSON format, ready for consumption by your applications.
- Docker-based Cermine Integration: Leverage the Cermine API's advanced metadata extraction capabilities by running it as a Docker container.
  Certainly! Here's a more detailed installation guide:

### Installation Guide

#### Prerequisites
- Docker installed on the host system
- Python 3.x installed on the host system

#### 1. Clone the Repository
Clone this repository to your local machine using Git:

```
git clone https://github.com/Abdellahbado/ResearchPaperMetaExtractor
```

#### 2. Navigate to the Project Directory
Change your current directory to the cloned project directory:

```bash
cd ResearchPaperMetaExtractor
```

#### 3. Start the Cermine API Docker Container
Run the following command to start the Cermine API Docker container:

```bash
docker run -p 8072:8080 elifesciences/cermine:1.13
```

#### 4. Set Up a Python Virtual Environment
Create and activate a Python virtual environment to isolate dependencies:

```bash
python3 -m venv env
```

- On Windows:

    ```bash
    env\Scripts\activate
    ```

- On macOS and Linux:

    ```bash
    source env/bin/activate
    ```

#### 5. Install Python Dependencies
Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

#### 6. Apply Django Migrations
Apply database migrations to set up the initial database schema:

```bash
python manage.py migrate
```

### Usage

#### 1. Start the Django Development Server
Run the following command to start the Django development server:

```bash
python manage.py runserver
```

#### 2. Access the API Endpoint
Use the following API endpoint to extract metadata from a PDF:

```
GET /metadata/url/<pdf_url>
```
Or if the pdf is on a drive 

```
GET /metadata/drive/<pdf_url>
```

Replace `<pdf_url>` with the URL of the PDF document you want to extract metadata from.

#### 3. Retrieve Metadata
The extracted metadata will be returned as a JSON response.


### Notes
- This application provides only an API endpoint and does not include a user interface.
- Ensure that the Cermine API Docker container is running before using the application.

### Contributing
Contributions are welcome! Feel free to submit issues or pull requests.
