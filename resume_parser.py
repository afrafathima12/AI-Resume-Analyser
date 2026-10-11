import pymupdf


def extract_resume_text(pdf_file):
    """Extract text from an uploaded PDF resume."""
    text = ""

    try:
        with pymupdf.open(stream=pdf_file.read(), filetype="pdf") as document:
            for page in document:
                text += page.get_text()

        return text.strip()

    except Exception as error:
        return f"Error reading PDF: {error}"
    