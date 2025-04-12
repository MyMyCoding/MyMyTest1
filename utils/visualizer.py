import py3Dmol
import streamlit.components.v1 as components

def show_structure(pdb_data):
    view = py3Dmol.view(width=600, height=400)
    view.addModel(pdb_data, "pdb")
    view.setStyle({"cartoon": {"color": "spectrum"}})
    view.zoomTo()
    html = f"""
    <html>
    <head>
    <script src="https://3Dmol.org/build/3Dmol.js"></script>
    </head>
    <body>
    {view._make_html()}
    </body>
    </html>
    """
    components.html(html, height=400)
