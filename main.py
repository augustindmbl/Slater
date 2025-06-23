import streamlit as st # type: ignore
from streamlit_autorefresh import st_autorefresh # type: ignore
from fractions import Fraction
import os
import time

import Constant
import Functions

st.title("Calcul d'énergies de transition")

# --------------- User Input ---------------

st.header("Initialisation")

## Atomic number ##
atom = st.selectbox("Numéro atomique", Constant.element_dict.keys())
atomic_number = Constant.element_dict[atom]

## Type of screened constants ##
method = st.selectbox("Constantes d'écrantage", ["Mendozza", "Lanzini"])

if method == "Mendozza":
    screen_constants = Functions.read_csv_screening_constants(Constant.file_path_mendozza)

elif method == "Lanzini":
    screen_constants = Functions.read_csv_screening_constants(Constant.file_path_lanzini)

## Units for energy ##
units = st.radio("Unité pour l'énergie :", ["eV", "a.u.", "Rydberg"], horizontal=True)

## Configuration init ##
st.subheader("Configuration initiale")

#Initialization of the list of orbitals
if "orbitals_initial" not in st.session_state:
    st.session_state.orbitals_initial = [{"n": 1, "l": "s", "j": "1/2", "occupation": 0}]

#Button to add an orbital
if st.button("➕ Ajouter une orbitale", key="add_orbital_initial"):
    st.session_state.orbitals_initial.append({"n": 1, "l": "s", "j": "1/2", "occupation": 0})

#Orbitals display
for i, orbital in enumerate(st.session_state.orbitals_initial):
    
    #Position of the columns
    cols = st.columns([1, 1, 1, 1, 0.5])
    
    with cols[0]: #n
        st.session_state.orbitals_initial[i]["n"] = st.selectbox(f"n", range(1, 8), key=f"n_{i}")
    
    with cols[1]: #l
        st.session_state.orbitals_initial[i]["l"] = st.selectbox(f"l", ["s", "p", "d", "f"], key=f"l_{i}")
    
    with cols[2]: #j
        l_value = Constant.l_dict[st.session_state.orbitals_initial[i]["l"]]
        st.session_state.orbitals_initial[i]["j"] = st.selectbox(f"j", Constant.j_possible_dict[l_value], key=f"j_{i}")
    
    with cols[3]: #P
        j_value = float(Fraction(st.session_state.orbitals_initial[i]["j"]))
        st.session_state.orbitals_initial[i]["occupation"] = st.number_input(f"Occupation", min_value=0, max_value=int(2*j_value+1), step=1, key=f"occ_{i}")
    
    with cols[4]: #Button to remove an orbital
        if st.button("❌", key=f"remove_{i}"):
            st.session_state.orbitals_initial.pop(i)
            st.rerun()

## Configuration final ##
st.subheader("Configuration finale")

# Initialisation de la liste des orbitales finales
if "orbitals_final" not in st.session_state:
    st.session_state.orbitals_final = [{"n": 1, "l": "s", "j": "1/2", "occupation": 0}]

# Bouton pour ajouter une orbitale finale
if st.button("➕ Ajouter une orbitale", key="add_orbital_final"):
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

# Validation button
if st.button("✅ Calculer"):

    config_initial_list = [0]*24
    config_final_list = [0]*24

    for orb in st.session_state.orbitals_initial:

        nlj = str(orb["n"]) + str(orb["l"]) + str(orb["j"])
        orbital_index = Constant.orbital_dict[nlj]
        config_initial_list[orbital_index] += orb["occupation"]
    
    for orb in st.session_state.orbitals_final:

        nlj = str(orb["n"]) + str(orb["l"]) + str(orb["j"])
        orbital_index = Constant.orbital_dict[nlj]
        config_final_list[orbital_index] += orb["occupation"]

    config_initial = Functions.print_config(config_initial_list)
    config_final = Functions.print_config(config_final_list)

    energy_init = Functions.energy_configuration(atomic_number, config_initial_list, screen_constants) # Conversion de J en eV
    energy_final = Functions.energy_configuration(atomic_number, config_final_list, screen_constants) 
    energy_transition = energy_final - energy_init

    st.header("Résultats")
    
    if units == "eV":
        st.markdown(
        f"**Configuration initiale** : {config_initial} ({energy_init:.2f} eV)  \n"
        f"**Configuration finale** : {config_final} ({energy_final:.2f} eV)")

        st.markdown(
        f"### Énergie de la transition : **{energy_transition:.2f} eV**")

    elif units == "a.u.":
        st.markdown(
        f"**Configuration initiale** : {config_initial} ({energy_init/(2*Constant.Rydberg_constant):.2f} a.u.)  \n"
        f"**Configuration finale** : {config_final} ({energy_final/(2*Constant.Rydberg_constant):.2f} a.u.)")

        st.markdown(
        f"### Énergie de la transition : **{energy_transition/(2*Constant.Rydberg_constant):.2f} a.u.**")
    
    elif units == "Rydberg":
        st.markdown(
        f"**Configuration initiale** : {config_initial} ({energy_init/Constant.Rydberg_constant:.2f} Ry)  \n"
        f"**Configuration finale** : {config_final} ({energy_final/Constant.Rydberg_constant:.2f} Ry)")

        st.markdown(
        f"### Énergie de la transition : **{energy_transition/Constant.Rydberg_constant:.2f} Ry**")





 
