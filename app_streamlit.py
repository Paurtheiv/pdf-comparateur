import streamlit as st
import tempfile
import os
import difflib
from pdf_tools import extract_text_from_pdf
from image_tools import convert_pdf_to_images, get_diff_boxes, draw_diff_boxes
from report_tools import create_pdf_report

def get_line_differences(text1, text2):
    lines1 = text1.splitlines()
    lines2 = text2.splitlines()
    diff = list(difflib.unified_diff(lines1, lines2, lineterm=''))
    filtered_diff = []
    for line in diff:
        if line.startswith('-') or line.startswith('+'):
            if not line.startswith('---') and not line.startswith('+++'):
                filtered_diff.append(line[0] + ' ' + line[1:].strip())
    return filtered_diff

def main():
    st.set_page_config(page_title="Comparateur PDF", layout="centered")
    st.title("📄 Comparateur de PDF (texte + images)")

    uploaded_file1 = st.file_uploader("Uploader le premier fichier PDF", type=["pdf"])
    uploaded_file2 = st.file_uploader("Uploader le deuxième fichier PDF", type=["pdf"])

    if uploaded_file1 and uploaded_file2:
        page_num = st.number_input("Numéro de page (à partir de 0)", min_value=0, step=1, value=0)
        margin = st.slider("Largeur de l'encadré rouge (marge autour de la différence)", min_value=5, max_value=100, value=20)

        # Sauvegarder temporairement les PDFs
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp1, \
             tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp2:
            tmp1.write(uploaded_file1.read())
            tmp2.write(uploaded_file2.read())
            tmp1_path = tmp1.name
            tmp2_path = tmp2.name

        try:
            # Extraire texte par page
            text1 = extract_text_from_pdf(tmp1_path)
            text2 = extract_text_from_pdf(tmp2_path)

            # Extraire images par page
            images1 = convert_pdf_to_images(tmp1_path, dpi=300)
            images2 = convert_pdf_to_images(tmp2_path, dpi=300)

            max_pages = min(len(text1), len(text2), len(images1), len(images2))

            if page_num >= max_pages:
                st.error(f"❌ Le numéro de page dépasse le nombre de pages ({max_pages}).")
                return

            st.subheader("📝 Texte extrait")
            col1, col2 = st.columns(2)
            with col1:
                st.text_area("Texte du PDF 1", text1[page_num], height=300)
            with col2:
                st.text_area("Texte du PDF 2", text2[page_num], height=300)

            boxes = get_diff_boxes(images1[page_num], images2[page_num], threshold=10, min_area=100, margin=margin)
            diff_img = draw_diff_boxes(images1[page_num], boxes)

            st.subheader("🔍 Comparaison visuelle des pages")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.image(images1[page_num], caption="PDF 1", use_column_width=True)
            with col2:
                st.image(images2[page_num], caption="PDF 2", use_column_width=True)
            with col3:
                st.image(diff_img, caption="Différences détectées (zones rouges)", use_column_width=True)

            if st.button("📄 Générer le rapport PDF"):
                differences_text = get_line_differences(text1[page_num], text2[page_num])
                differences_text_by_page = {page_num: differences_text}
                visual_diff_boxes_by_page = {page_num: boxes}

                report_path = os.path.join(tempfile.gettempdir(), "rapport_comparaison.pdf")
                create_pdf_report(
                    differences_text_by_page=differences_text_by_page,
                    visual_diff_boxes_by_page=visual_diff_boxes_by_page,
                    path=report_path,
                    page_image=diff_img
                )

                with open(report_path, "rb") as f:
                    st.download_button("Télécharger le rapport PDF", f, file_name="rapport_comparaison.pdf")

        finally:
            os.remove(tmp1_path)
            os.remove(tmp2_path)

if __name__ == "__main__":
    main()
