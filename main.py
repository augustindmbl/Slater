import streamlit as st # type: ignore
from streamlit_autorefresh import st_autorefresh # type: ignore
from fractions import Fraction
import os
import time

import Constant

st.title("Calcul d'énergies de transition")

# --------------- User Input ---------------

st.header("Initialisation")

## Atomic number ##
atom = st.selectbox("Numéro atomique", Constant.element_dict.keys())
atomic_number = Constant.element_dict[atom]

## Type of screened constants ##
method = st.selectbox("Constantes d'écrantage", ["Mendozza", "Lanzini"])

## Configuration init ##
st.subheader("Configuration initiale")

#Initialization of the list of orbitals
if "orbitals" not in st.session_state:
    st.session_state.orbitals = [{"n": 1, "l": "s", "j": "1/2", "occupation": 0}]

#Button to add an orbital
if st.button("➕ Ajouter une orbitale"):
    st.session_state.orbitals.append({"n": 1, "l": "s", "j": "1/2", "occupation": 0})

#Orbitals display
for i, orbital in enumerate(st.session_state.orbitals):
    
    #Position of the columns
    cols = st.columns([1, 1, 1, 1, 0.5])
    
    with cols[0]: #n
        st.session_state.orbitals[i]["n"] = st.selectbox(f"n", range(1, 8), key=f"n_{i}")
    
    with cols[1]: #l
        st.session_state.orbitals[i]["l"] = st.selectbox(f"l", ["s", "p", "d", "f"], key=f"l_{i}")
    
    with cols[2]: #j
        l_value = Constant.l_dict[st.session_state.orbitals[i]["l"]]
        st.session_state.orbitals[i]["j"] = st.selectbox(f"j", Constant.j_possible_dict[l_value], key=f"j_{i}")
    
    with cols[3]: #P
        j_value = float(Fraction(st.session_state.orbitals[i]["j"]))
        st.session_state.orbitals[i]["occupation"] = st.number_input(f"Occupation", min_value=0, max_value=int(2*j_value+1), step=1, key=f"occ_{i}")
    
    with cols[4]: #Button to remove an orbital
        if st.button("❌", key=f"remove_{i}"):
            st.session_state.orbitals.pop(i)
            st.rerun()

## Configuration final ##
st.subheader("Configuration finale")

# Initialisation de la liste des orbitales finales
if "orbitals_final" not in st.session_state:
    st.session_state.orbitals_final = [{"n": 1, "l": "s", "j": "1/2", "occupation": 0}]

# Bouton pour ajouter une orbitale finale
if st.button("➕ Ajouter une orbitale"):
    st.session_state.orbitals_final.append({"n": 1, "l": "s", "j": "1/2", "occupation": 0})

# Affichage des orbitales finales
for i, orbital in enumerate(st.session_state.orbitals_final):
    
    # Position des colonnes
    cols = st.columns([1, 1, 1, 1, 0.5])
    
    with cols[0]:  # n
        st.session_state.orbitals_final[i]["n"] = st.selectbox(f"n", range(1, 8), key=f"n_final_{i}")
    
    with cols[1]:  # l
        st.session_state.orbitals_final[i]["l"] = st.selectbox(f"l", ["s", "p", "d", "f"], key=f"l_final_{i}")
    
    with cols[2]:  # j
        l_value = Constant.l_dict[st.session_state.orbitals_final[i]["l"]]
        st.session_state.orbitals_final[i]["j"] = st.selectbox(f"j", Constant.j_possible_dict[l_value], key=f"j_final_{i}")
    
    with cols[3]:  # Occupation
        j_value = float(Fraction(st.session_state.orbitals_final[i]["j"]))
        st.session_state.orbitals_final[i]["occupation"] = st.number_input(f"Occupation", min_value=0, max_value=int(2*j_value + 1), step=1, key=f"occ_final_{i}")
    
    with cols[4]:  # Bouton pour supprimer une orbitale finale
        if st.button("❌", key=f"remove_final_{i}"):
            st.session_state.orbitals_final.pop(i)
            st.rerun()

# Bouton de validation
if st.button("✅ Valider la configuration"):

    config = [0]*24
    print(config)
    for orb in st.session_state.orbitals:

        nlj = str(orb["n"]) + str(orb["l"]) + str(orb["j"])
        orbital_index = Constant.orbital_dict[nlj]
        
        config[orbital_index] += orb["occupation"]
        
        
        
        """occ = orb["occupation"]
        config.append(f"({n}{l}{j:.1f})^{occ}")
        st.success("Configuration : " + ", ".join(config))
        """
    print(config)
if st.button("Calculer"):
    st.success("Ca arrive")

