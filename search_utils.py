import re

def extract_text_from_pdf(path, include_pages=False):
    import fitz
    doc = fitz.open(path)
    if include_pages:
        return [(i + 1, page.get_text()) for i, page in enumerate(doc)]
    else:
        return "\n".join(page.get_text() for page in doc)

def extract_text_from_docx(path):
    from docx import Document
    doc = Document(path)
    return "\n".join(p.text for p in doc.paragraphs)

def extract_text_from_txt(path):
    with open(path, 'r', encoding='utf-8', errors='ignore') as f:
        return f.read()

def search_text_in_content(content, search_terms, case_sensitive=False, exact_match=False):
    lines = content.splitlines()
    matches = []
    for i, line in enumerate(lines, start=1):
        for term in search_terms:
            pattern = r'\b{}\b'.format(re.escape(term)) if exact_match else re.escape(term)
            flags = 0 if case_sensitive else re.IGNORECASE

            if re.search(pattern, line, flags=flags):
                matches.append((i, line.strip()))
                break  # Avoid duplicate hits per line
    return matches
