import streamlit as st
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from utils.visualizer import show_structure
from utils.pdb_utils import get_pdb_info, calculate_rmsd, fetch_plip_data

st.set_page_config(layout="wide")
st.title("GlioTarget-Aptamer Explorer v3 - with Clustering")

uploaded_files = st.file_uploader("Upload Aptamer PDB Files", type="pdb", accept_multiple_files=True)

if uploaded_files:
    st.header("🔍 Aptamer Viewer & Summary")
    aptamer_data = []
    names = []
    for uploaded_file in uploaded_files:
        pdb_data = uploaded_file.read().decode("utf-8")
        aptamer_data.append(pdb_data)
        names.append(uploaded_file.name)
        st.subheader(f"📁 {uploaded_file.name}")
        show_structure(pdb_data)
        info = get_pdb_info(pdb_data)
        st.json(info)

        if st.checkbox(f"🔗 Show PLIP Interactions for {uploaded_file.name}"):
            plip_output = fetch_plip_data(pdb_data)
            st.write(plip_output or "No interaction data available.")

    st.header("📏 RMSD Comparison Matrix")
    n = len(aptamer_data)
    rmsd_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            rmsd = calculate_rmsd(aptamer_data[i], aptamer_data[j])
            rmsd_matrix[i, j] = rmsd
            rmsd_matrix[j, i] = rmsd
    st.dataframe(pd.DataFrame(rmsd_matrix, index=names, columns=names))

    st.header("📊 Clustering of Aptamers (PCA + KMeans)")
    pca = PCA(n_components=2)
    reduced = pca.fit_transform(rmsd_matrix)
    clusters = KMeans(n_clusters=min(3, len(uploaded_files))).fit_predict(reduced)

    fig, ax = plt.subplots()
    for i, name in enumerate(names):
        ax.scatter(reduced[i, 0], reduced[i, 1], label=name, s=100, alpha=0.7)
        ax.text(reduced[i, 0] + 0.1, reduced[i, 1], name, fontsize=9)
    ax.set_title("2D PCA Clustering (based on RMSD)")
    st.pyplot(fig)

else:
    st.info("Please upload at least one aptamer PDB file.")
