from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.enums import TA_CENTER, TA_LEFT

def export_pdf_report(output_path, document_title, chunks):
    """
    chunks = [
        {
            "text": ...,
            "best": ...,
            "score": ...,
            "explanation": ...
        }
    ]
    """
    doc = SimpleDocTemplate(output_path, pagesize=letter)
    story = []
    styles = getSampleStyleSheet()

    # Title style
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=24,
        textColor='darkblue',
        spaceAfter=30,
        alignment=TA_CENTER
    )

    # Add title
    story.append(Paragraph(f"Strategy Mapper Report: {document_title}", title_style))
    story.append(Spacer(1, 0.2*inch))

    # Process each chunk
    for i, ch in enumerate(chunks, start=1):
        # Chunk header
        chunk_header = ParagraphStyle(
            'ChunkHeader',
            parent=styles['Heading2'],
            fontSize=14,
            textColor='darkgreen',
            spaceAfter=10
        )
        story.append(Paragraph(f"Chunk {i}", chunk_header))

        # Chunk text
        story.append(Paragraph(ch["text"], styles['Normal']))
        story.append(Spacer(1, 0.1*inch))

        # Best match
        match_style = ParagraphStyle(
            'Match',
            parent=styles['Normal'],
            fontSize=12,
            textColor='darkblue',
            fontName='Helvetica-Bold'
        )
        story.append(Paragraph(f"Best match: {ch['best']} ({ch['score']:.3f})", match_style))
        story.append(Spacer(1, 0.1*inch))

        # Explanation
        story.append(Paragraph(f"<b>Explanation:</b> {ch['explanation']}", styles['Normal']))
        story.append(Spacer(1, 0.2*inch))

        # Add page break between chunks (except for last one)
        if i < len(chunks):
            story.append(PageBreak())

    doc.build(story)
