import streamlit as st
from utils.visualizer import show_structure
from utils.pdb_utils import get_pdb_info, calculate_rmsd, fetch_plip_data

st.set_page_config(layout="wide")
st.title("GlioTarget-Aptamer Explorer v2")

uploaded_files = st.file_uploader("Upload Aptamer PDB Files", type="pdb", accept_multiple_files=True)

if uploaded_files:
    st.header("🔍 Aptamer Viewer & Summary")
    for uploaded_file in uploaded_files:
        pdb_data = uploaded_file.read().decode("utf-8")
        st.subheader(f"📁 {uploaded_file.name}")
        show_structure(pdb_data)
        info = get_pdb_info(pdb_data)
        st.json(info)

        if st.checkbox(f"🔗 Show PLIP Interactions for {uploaded_file.name}"):
            plip_output = fetch_plip_data(pdb_data)
            st.write(plip_output or "No interaction data available.")

    st.header("📏 RMSD Comparison")
    if len(uploaded_files) >= 2:
        ref_data = uploaded_files[0].read().decode("utf-8")
        uploaded_files[0].seek(0)
        for other_file in uploaded_files[1:]:
            other_data = other_file.read().decode("utf-8")
            rmsd = calculate_rmsd(ref_data, other_data)
            st.write(f"RMSD between {uploaded_files[0].name} and {other_file.name}: **{rmsd:.3f} Å**")
            other_file.seek(0)
else:
    st.info("Please upload at least one aptamer PDB file.")
