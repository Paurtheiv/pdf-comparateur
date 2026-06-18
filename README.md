# 📄 Comparateur de PDF

> Outil de comparaison visuelle et textuelle de documents PDF  
> Développé durant le stage chez Bilfinger Peters Engineering · 2025

[![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=flat&logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.45-FF4B4B?style=flat&logo=streamlit)](https://streamlit.io)

---

## 📋 Description

Application Python développée pendant le stage IT chez **Bilfinger Peters Engineering** pour automatiser la comparaison de documents PDF techniques (plans, fiches, rapports).

L'outil détecte automatiquement les différences entre deux PDFs — textuelles et visuelles — et génère un rapport PDF annoté avec les zones de différence encadrées en rouge.

---

## 🏗️ Structure

```
pdf-comparateur-stage/
├── app_streamlit.py      # Interface Streamlit (upload, visualisation, rapport)
├── pdf_tools.py          # Extraction texte par page (PyPDF2)
├── image_tools.py        # Conversion PDF→images, détection diff pixel par pixel
├── report_tools.py       # Génération rapport PDF annoté (ReportLab)
├── requirements.txt      # Dépendances Python
└── lancer.bat            # Lancement Windows avec Python embarqué
```

---

## ⚙️ Technologies

| Composant | Technologie |
|-----------|-------------|
| Interface | Streamlit 1.45 |
| Extraction texte | PyPDF2 3.0 |
| Conversion images | pdf2image / Pillow |
| Comparaison visuelle | PIL ImageChops + flood-fill |
| Rapport PDF | ReportLab |
| Packaging Windows | Python embarqué + .bat |

---

## 🚀 Installation

```bash
# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
streamlit run app_streamlit.py
```

Ou sur Windows : double-cliquer sur `lancer.bat` (installe tout automatiquement).

---

## 📱 Fonctionnalités

- Upload de deux PDFs via interface web
- Sélection de la page à comparer
- Extraction et affichage du texte par page (côte à côte)
- Comparaison visuelle pixel par pixel avec détection de zones modifiées
- Réglage de la sensibilité (seuil, marge des encadrés)
- Génération d'un rapport PDF avec tableau des différences + image annotée

---

## 👤 Auteur

**Paurtheiv Krishna Laxman**  
Stage IT — Bilfinger Peters Engineering · 2025  
BTS CIEL A — Lycée Jean Jaurès, Argenteuil (95)

📧 paurtheiv.laxman.fr@gmail.com  
🔗 [Portfolio](https://paurtheiv.github.io)
