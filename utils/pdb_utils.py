from Bio.PDB import PDBParser, Superimposer
from io import StringIO
import requests

def get_pdb_info(pdb_data):
    parser = PDBParser(QUIET=True)
    structure = parser.get_structure("aptamer", StringIO(pdb_data))
    residues = list(structure.get_residues())
    atoms = list(structure.get_atoms())
    base_counts = {}
    for res in residues:
        name = res.get_resname()
        base_counts[name] = base_counts.get(name, 0) + 1
    return {
        "Residue Count": len(residues),
        "Atom Count": len(atoms),
        "Base Composition": base_counts
    }

def calculate_rmsd(pdb1, pdb2):
    parser = PDBParser(QUIET=True)
    s1 = parser.get_structure("ref", StringIO(pdb1))
    s2 = parser.get_structure("alt", StringIO(pdb2))
    atoms1 = [atom for atom in s1.get_atoms() if atom.get_id() == "P"]
    atoms2 = [atom for atom in s2.get_atoms() if atom.get_id() == "P"]
    si = Superimposer()
    si.set_atoms(atoms1[:min(len(atoms1), len(atoms2))], atoms2[:min(len(atoms1), len(atoms2))])
    return si.rms

def fetch_plip_data(pdb_data):
    try:
        response = requests.post(
            "https://plip-api.biotec.tu-dresden.de/plip",
            files={"pdb": ("structure.pdb", pdb_data)},
            timeout=60,
        )
        if response.status_code == 200:
            return response.json()
        else:
            return {"error": f"PLIP API returned status {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}
