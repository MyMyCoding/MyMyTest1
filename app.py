import streamlit as st
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from utils.visualizer import show_structure
from utils.pdb_utils import get_pdb_info, calculate_rmsd, fetch_plip_data, extract_interaction_features, predict_affinity

st.set_page_config(layout="wide")
st.title("GlioTarget-Aptamer Explorer v5 – ML Affinity & Docking Enhanced")

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

    st.header("📏 RMSD Matrix + PCA Clustering")
    n = len(aptamer_data)
    rmsd_matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            rmsd = calculate_rmsd(aptamer_data[i], aptamer_data[j])
            rmsd_matrix[i, j] = rmsd
            rmsd_matrix[j, i] = rmsd
    st.dataframe(pd.DataFrame(rmsd_matrix, index=names, columns=names))

    reduced = PCA(n_components=2).fit_transform(rmsd_matrix)
    clusters = KMeans(n_clusters=min(3, len(uploaded_files))).fit_predict(reduced)
    fig, ax = plt.subplots()
    for i, name in enumerate(names):
        ax.scatter(reduced[i, 0], reduced[i, 1], s=100)
        ax.text(reduced[i, 0] + 0.1, reduced[i, 1], name, fontsize=9)
    ax.set_title("PCA Clustering")
    st.pyplot(fig)

    st.header("🔮 ML-Based Affinity Scoring (Beta)")
    for name, pdb_data in zip(names, aptamer_data):
        features = extract_interaction_features(pdb_data)
        score = predict_affinity(features)
        st.write(f"Predicted Affinity for {name}: **{score:.2f} (AI Score)**")

    st.header("🧬 Docking & Contact Maps (Coming Soon)")
    st.info("This section will support EGFR–aptamer docking with scoring via AlphaFold/HDOCK + PLIP.")
else:
    st.info("Please upload at least one aptamer PDB file.")
