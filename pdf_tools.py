import io
from PyPDF2 import PdfReader
from pdf2image import convert_from_bytes
from PIL import Image, ImageChops, ImageDraw
import numpy as np

def extract_text_from_pdf(pdf_input):
    """Retourne une liste de texte par page."""
    if isinstance(pdf_input, str):
        reader = PdfReader(pdf_input)
    elif isinstance(pdf_input, bytes):
        reader = PdfReader(io.BytesIO(pdf_input))
    else:
        raise ValueError("Le format du PDF n'est ni un chemin ni des bytes.")

    texts = []
    for page in reader.pages:
        texts.append(page.extract_text() or "")
    return texts

def convert_pdf_to_images(pdf_input, dpi=200):
    if isinstance(pdf_input, str):
        with open(pdf_input, 'rb') as f:
            pdf_bytes = f.read()
    elif isinstance(pdf_input, bytes):
        pdf_bytes = pdf_input
    else:
        raise ValueError("Le format du PDF n'est ni un chemin ni des bytes.")

    images = convert_from_bytes(pdf_bytes, dpi=dpi)
    return images

def compare_images(img1, img2, threshold=30, margin=20):
    img1 = img1.convert('RGB')
    img2 = img2.convert('RGB')

    diff = ImageChops.difference(img1, img2)
    diff_np = np.array(diff)

    mask = np.any(diff_np > threshold, axis=-1)
    coords = np.column_stack(np.where(mask))

    draw = ImageDraw.Draw(img2)

    if coords.size > 0:
        for y, x in coords:
            draw.rectangle([
                (max(x - margin, 0), max(y - margin, 0)),
                (min(x + margin, img2.width), min(y + margin, img2.height))
            ], outline='red', width=2)

    return img2
