import py3Dmol
import streamlit.components.v1 as components

def show_structure(pdb_data):
    view = py3Dmol.view(width=600, height=400)
    view.addModel(pdb_data, "pdb")
    view.setStyle({"cartoon": {"color": "spectrum"}})
    view.zoomTo()
    html = view.get_html()
    components.html(html, height=400)
