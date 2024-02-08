## Django Metadata Extraction API - Extract Metadata from PDFs Online or from Open Drive

This Django application provides a powerful and user-friendly API to extract various metadata elements (title, authors, institutions, abstract, text, references, publication date, keywords) from PDF documents, leveraging both online sources and OpenDrive storage connectivity. It partially integrates the Cermine API (accessed via its Docker container) for exceptional metadata extraction capabilities.

Key Features:

    Versatile Metadata Extraction: Extract comprehensive metadata from diverse PDF sources, including title, authors, institutions, abstract, full text, references, publication date, and keywords.
    Multiple Source Options: Process PDFs hosted online via URLs or conveniently access them from your OpenDrive account for seamless workflow.
    RESTful API Endpoint: Interact with the application programmatically through a well-defined and accessible RESTful API endpoint.
    JSON Output: Receive extracted metadata in a structured JSON format, ready for consumption by your applications.
    Docker-based Cermine Integration: Leverage the Cermine API's advanced metadata extraction capabilities by running it as a Docker container.
