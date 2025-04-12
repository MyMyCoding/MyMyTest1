# GlioTarget-Aptamer Explorer v2

An advanced Streamlit app to visualize, analyze, and compare aptamers for EGFR-targeted glioblastoma therapy.

## Features
- Upload and visualize multiple 3D PDB structures
- Compute residue/atom counts
- Use PLIP Web API to identify molecular interactions
- RMSD comparison between uploaded structures

## Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
```

## Deploy on Streamlit Cloud

1. Upload this project to a GitHub repo
2. Go to https://streamlit.io/cloud
3. Set the main app path as `app.py`
4. (Optional) Ensure Python version using `runtime.txt`
