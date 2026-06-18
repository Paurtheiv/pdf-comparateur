from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as PlatypusImage, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
from reportlab.lib import colors
import io
from PIL import Image, ImageDraw


def draw_visual_diff_boxes_on_image(image_pil, visual_diff_boxes_by_page):
    """
    Dessine des rectangles bleus avec fond rouge semi-transparent autour des zones visuelles.
    """
    if not visual_diff_boxes_by_page:
        return image_pil

    draw = ImageDraw.Draw(image_pil, "RGBA")
    for page_num, boxes in visual_diff_boxes_by_page.items():
        for (x0, y0, x1, y1) in boxes:
            draw.rectangle([(x0, y0), (x1, y1)], fill=(255, 0, 0, 60), outline=(0, 0, 255, 255), width=3)
    return image_pil


def create_text_diff_table(differences_text_by_page):
    data = [['Page', 'Ligne modifiée']]
    for page_num in sorted(differences_text_by_page.keys()):
        diffs = differences_text_by_page[page_num]
        if not diffs:
            data.append([str(page_num + 1), "Aucune différence"])
        else:
            for line in diffs:
                clean_line = line.strip().replace('\n', ' ')
                data.append([str(page_num + 1), clean_line])

    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ])
    table = Table(data, colWidths=[0.7 * inch, 5.8 * inch])
    table.setStyle(style)
    return table


def create_visual_diff_table(visual_diff_boxes_by_page):
    data = [['Page', 'Coordonnées des différences détectées']]
    for page_num in sorted(visual_diff_boxes_by_page.keys()):
        boxes = visual_diff_boxes_by_page[page_num]
        if boxes:
            for (x0, y0, x1, y1) in boxes:
                coords = f"({int(x0)},{int(y0)},{int(x1)},{int(y1)})"
                data.append([str(page_num + 1), coords])
        else:
            data.append([str(page_num + 1), "Aucune différence"])

    style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 11),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.black),
    ])
    table = Table(data, colWidths=[0.7 * inch, 5.8 * inch])
    table.setStyle(style)
    return table


def create_pdf_report(differences_text_by_page=None, visual_diff_boxes_by_page=None,
                      path="rapport_comparaison.pdf", page_image=None):
    """
    Génère un rapport PDF avec :
    - un tableau ligne par ligne des différences textuelles,
    - un tableau des zones visuelles détectées (coordonnées),
    - une image annotée si fournie (zones encadrées).

    Params :
        differences_text_by_page : dict {page_num: [lignes_diff]}
        visual_diff_boxes_by_page : dict {page_num: [(x0,y0,x1,y1), ...]}
        path : str, chemin de sortie
        page_image : PIL.Image (optionnel)
    """
    if differences_text_by_page is None:
        differences_text_by_page = {}
    if visual_diff_boxes_by_page is None:
        visual_diff_boxes_by_page = {}

    doc = SimpleDocTemplate(path, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Table des différences textuelles
    elements.append(Paragraph("<b>Tableau des différences textuelles :</b>", styles['Heading3']))
    elements.append(Spacer(1, 12))
    elements.append(create_text_diff_table(differences_text_by_page))
    elements.append(Spacer(1, 24))

    # Table des différences visuelles
    elements.append(Paragraph("<b>Tableau des différences visuelles :</b>", styles['Heading3']))
    elements.append(Spacer(1, 12))
    elements.append(create_visual_diff_table(visual_diff_boxes_by_page))
    elements.append(Spacer(1, 24))

    # Image annotée
    if page_image:
        annotated_image = draw_visual_diff_boxes_on_image(page_image.copy(), visual_diff_boxes_by_page)
        img_buffer = io.BytesIO()
        annotated_image.save(img_buffer, format='PNG')
        img_buffer.seek(0)
        img_flowable = PlatypusImage(img_buffer, width=6 * inch, height=7 * inch)
        elements.append(Paragraph("<b>Page annotée :</b>", styles['Heading3']))
        elements.append(Spacer(1, 12))
        elements.append(img_flowable)

    doc.build(elements)
