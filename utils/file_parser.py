from pypdf import PdfReader
from docx import Document


def read_txt(uploaded_file):
    return uploaded_file.read().decode("utf-8")


def read_pdf(uploaded_file):
    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text + "\n"

    return text


def read_docx(uploaded_file):
    document = Document(uploaded_file)

    text = ""

    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"

    return text


def extract_text(uploaded_file):
    file_name = uploaded_file.name.lower()

    if file_name.endswith(".txt"):
        return read_txt(uploaded_file)

    elif file_name.endswith(".pdf"):
        return read_pdf(uploaded_file)

    elif file_name.endswith(".docx"):
        return read_docx(uploaded_file)

    else:
        raise ValueError("Unsupported file type")