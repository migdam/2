import re

def basic_paragraph_split(text: str):
    """
    Split text into paragraphs using double newline or line breaks.
    """
    paragraphs = re.split(r"\n\s*\n", text)
    paragraphs = [p.strip() for p in paragraphs if p.strip()]
    return paragraphs

def sanitize(paragraph):
    """
    Clean weird whitespace, repeated punctuation, etc.
    """
    paragraph = paragraph.replace("\xa0", " ")
    paragraph = re.sub(r"\s+", " ", paragraph)
    return paragraph.strip()

def merge_short_paragraphs(paragraphs, min_length=120):
    """
    If a paragraph is very short (example: title, header),
    merge it with the next one to give more context for embeddings.
    """
    merged = []
    buffer = ""

    for p in paragraphs:
        p = sanitize(p)
        if len(p) < min_length:
            buffer += " " + p
        else:
            if buffer:
                merged.append((buffer + " " + p).strip())
                buffer = ""
            else:
                merged.append(p)

    if buffer:
        merged.append(buffer.strip())

    return merged

def agentic_chunk(text: str, mode="auto"):
    """
    Main chunking logic:
    - "basic": simple paragraph split
    - "merged": merge short paragraphs
    - "auto": best-of-both (recommended)
    """
    paragraphs = basic_paragraph_split(text)

    if mode == "basic":
        return paragraphs

    if mode == "merged":
        return merge_short_paragraphs(paragraphs)

    # AUTO MODE
    if len(max(paragraphs, key=len)) < 120:
        return merge_short_paragraphs(paragraphs)

    return paragraphs
