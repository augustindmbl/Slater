import streamlit as st # type: ignore
from streamlit_autorefresh import st_autorefresh # type: ignore
from fractions import Fraction
import os
import time

import Constant
import Functions

st.title("Calcul d'énergies de transition")
st.markdown("[Atomic Spectra Database (NIST)](https://www.nist.gov/pml/atomic-spectra-database)")


# --------------- User Input ---------------

st.header("Initialisation")

## Atomic number ##
atom = st.selectbox("Numéro atomique", Constant.element_atomic_number_dict.keys())
atomic_number = Constant.element_atomic_number_dict[atom]
atomic_symbol = Constant.element_symbol_dict[atom]

## Choice of screening constants ##
method = st.selectbox("Constantes d'écrantage", ["Mendozza", "Lanzini", "Faussurier"])

if method == "Mendozza":
    screen_constants = Functions.read_csv_screening_constants(Constant.file_path_mendozza)

elif method == "Lanzini":
    screen_constants = Functions.read_csv_screening_constants(Constant.file_path_lanzini)

elif method == "Faussurier":
    screen_constants = Functions.read_csv_screening_constants(Constant.file_path_faussurier)

## Units for energy and precision ##
col1, col2 = st.columns([2, 1])
with col1:
    units = st.radio("Unité pour l'énergie", ["eV", "a.u.", "Rydberg"], horizontal=True)
with col2:
    precision = st.selectbox("Précision sur l'énergie", [2, 3, 4, 5]) 

## Configuration init ##
st.subheader("Configuration initiale")

# Initialization of the list of orbitals
if "orbitals_initial" not in st.session_state:
    st.session_state.orbitals_initial = [{"n": 1, "l": "s", "j": "1/2", "occupation": 0}]

# Button to add an orbital or reset the list
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("➕ Ajouter une orbitale", key="add_orbital_initial"):
        st.session_state.orbitals_initial.append({"n": 1, "l": "s", "j": "1/2", "occupation": 0})
with col2:
    if st.button("Reset", key = "reset_initial"):
        st.session_state.orbitals_initial = [{"n": 1, "l": "s", "j": "1/2", "occupation": 0}]

# Orbitals display
for i, orbital in enumerate(st.session_state.orbitals_initial):
    
    # Position of the selectbox/button (n, l, j, P, delete buttons)
    cols = st.columns([1, 1, 1, 1, 0.5])
    
    with cols[0]: #n
        st.session_state.orbitals_initial[i]["n"] = st.selectbox(f"n", range(1, 7), key=f"n_{i}")
    
    with cols[1]: #l
        n_value = float(st.session_state.orbitals_initial[i]["n"])
        st.session_state.orbitals_initial[i]["l"] = st.selectbox(f"l", Constant.l_possible_dict[n_value], key=f"l_{i}")
    
    with cols[2]: #j
        l_value = Constant.l_dict[st.session_state.orbitals_initial[i]["l"]] #To obtain the quantum number from the letter (exp : s -> 1)
        st.session_state.orbitals_initial[i]["j"] = st.selectbox(f"j", Constant.j_possible_dict[l_value], key=f"j_{i}")
    
    with cols[3]: #Occupation
        j_value = float(Fraction(st.session_state.orbitals_initial[i]["j"])) #To convert j in a float (exp : 3/2 -> 1.5)
        st.session_state.orbitals_initial[i]["occupation"] = st.number_input(f"Occupation", min_value=0, max_value=int(2*j_value+1), step=1, key=f"occ_{i}")
    
    with cols[4]: # Button to remove an orbital
        st.markdown("<br>", unsafe_allow_html=True) #To align the button with the rest of the line
        if st.button("❌", key=f"remove_{i}"):
            st.session_state.orbitals_initial.pop(i)
            st.rerun()

## Configuration final ##
st.subheader("Configuration finale")

# Initialization of the list of orbitals
if "orbitals_final" not in st.session_state:
    st.session_state.orbitals_final = [{"n": 1, "l": "s", "j": "1/2", "occupation": 0}]

#Button to add an orbital or reset the list
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("➕ Ajouter une orbitale", key="add_orbital_final"):
        st.session_state.orbitals_final.append({"n": 1, "l": "s", "j": "1/2", "occupation": 0})
with col2:
    if st.button("Reset", key = "reset_final"):
        st.session_state.orbitals_final = [{"n": 1, "l": "s", "j": "1/2", "occupation": 0}]

# Orbitals display
for i, orbital in enumerate(st.session_state.orbitals_final):
    
    # Position of the selectbox/button (n, l, j, P, delete buttons)
    cols = st.columns([1, 1, 1, 1, 0.5])
    
    with cols[0]:  # n
        st.session_state.orbitals_final[i]["n"] = st.selectbox(f"n", range(1, 7), key=f"n_final_{i}")
    
    with cols[1]:  # l
        n_value = float(st.session_state.orbitals_final[i]["n"])
        st.session_state.orbitals_final[i]["l"] = st.selectbox(f"l", Constant.l_possible_dict[n_value], key=f"l_final_{i}")
    
    with cols[2]:  # j
        l_value = Constant.l_dict[st.session_state.orbitals_final[i]["l"]] #To obtain the quantum number from the letter (exp : s -> 1)
        st.session_state.orbitals_final[i]["j"] = st.selectbox(f"j", Constant.j_possible_dict[l_value], key=f"j_final_{i}")
    
    with cols[3]:  # Occupation
        j_value = float(Fraction(st.session_state.orbitals_final[i]["j"])) #To convert j in a float (exp : 3/2 -> 1.5)
        st.session_state.orbitals_final[i]["occupation"] = st.number_input(f"Occupation", min_value=0, max_value=int(2*j_value + 1), step=1, key=f"occ_final_{i}")
    
    with cols[4]:  # Button to remove an orbital
        st.markdown("<br>", unsafe_allow_html=True) #To align the button with the rest of the line
        if st.button("❌", key=f"remove_final_{i}"):
            st.session_state.orbitals_final.pop(i)
            st.rerun()



# --------------- Calculation ---------------

if st.button("✅ Calculer"):

    # Initialization of list for configuration. Each element is an orbital (index given by Constant.orbital_dict) and the values is the occupation
    config_initial_list = [0]*24
    config_final_list = [0]*24

    # Fill config_initial_list with the selectbox values
    for orb in st.session_state.orbitals_initial:

        nlj = str(orb["n"]) + str(orb["l"]) + str(orb["j"])
        orbital_index = Constant.orbital_dict[nlj]
        config_initial_list[orbital_index] += orb["occupation"]
    
    # Fill config_final_list with the selectbox values
    for orb in st.session_state.orbitals_final:

        nlj = str(orb["n"]) + str(orb["l"]) + str(orb["j"])
        orbital_index = Constant.orbital_dict[nlj]
        config_final_list[orbital_index] += orb["occupation"]

    # Transform config list in a string to print the configuration with LaTeX style
    config_initial = Functions.print_config(config_initial_list)
    config_final = Functions.print_config(config_final_list)

    # Calculates the number of electron for initial and final configuration
    number_electron_initial = sum(config_initial_list)
    number_electron_final = sum(config_final_list)
    
    # Test to verify that there is no too much electron for a single configuration. Initialy the condition is True and then it's modified in False if there is problem.
    good_number_of_electron_initial = True
    good_number_of_electron_final = True

    for index, value in enumerate(config_initial_list): 

        if value > Constant.orbital_max_electrons[index]:
            good_number_of_electron_initial = False
            error_initial = f"Il y a trop d'électrons dans l'orbital ${Constant.orbital_latex_dict[index]}$ dans la configuration initiale."
            break

    for index, value in enumerate(config_final_list): 

        if value > Constant.orbital_max_electrons[index]:
            good_number_of_electron_final = False
            error_final = f"Il y a trop d'électrons dans l'orbital ${Constant.orbital_latex_dict[index]}$ dans la configuration finale."
            break
    
    #Calculation of initial, final and transition energy
    energy_init = Functions.energy_configuration(atomic_number, config_initial_list, screen_constants)
    energy_final = Functions.energy_configuration(atomic_number, config_final_list, screen_constants) 
    energy_transition = energy_final - energy_init


# --------------- Output ---------------

    st.header("Résultats") 

    ## Error test section ##

    # Initial and final configurations must have the same number of electrons
    if number_electron_initial != number_electron_final:
        st.markdown(
        "<span style='color:red; font-weight:bold;'>❌ Erreur :</span> "
        "Les deux configurations n'ont pas le même nombre d'électrons.",
        unsafe_allow_html=True)
    
    # Configurations must have at least one electrons
    elif number_electron_initial == 0:
        st.markdown(
        "<span style='color:red; font-weight:bold;'>❌ Erreur :</span> "
        "Aucune configuration n'a été rentrée.",
        unsafe_allow_html=True)
    
    # Occupation for an orbital is determined by j. Test for initial configuration
    elif not good_number_of_electron_initial:
        st.markdown(
        "<span style='color:red; font-weight:bold;'>❌ Erreur :</span> "
        + error_initial,
        unsafe_allow_html=True)
    
    # Occupation for an orbital is determined by j. Test for final configuration
    elif not good_number_of_electron_final:
        st.markdown(
        "<span style='color:red; font-weight:bold;'>❌ Erreur :</span> "
        + error_final,
        unsafe_allow_html=True)
    
    # If everything is good resultats are printed
    else:

        charge_state = atomic_number - number_electron_initial
        
        # Display difference if it's a positive or negative ions 
        if charge_state > 0:
            ion_name = atomic_symbol + "^{" + str(int(charge_state)) + "+}"
        elif charge_state < 0:
            ion_name = atomic_symbol + "^{" + str(int(-charge_state)) + "-}"
        else:
            ion_name = atomic_symbol

        # Results in eV
        if units == "eV":
            st.markdown(
            f"**Ion** : ${ion_name}$  \n"
            f"**Configuration initiale** : ${config_initial}$ ({energy_init:.{precision}f} eV)  \n"
            f"**Configuration finale** : ${config_final}$ ({energy_final:.{precision}f} eV)")

            st.markdown(
            f"### Énergie de la transition : **{energy_transition:.{precision}f} eV**")
        
        # Results in atomic units
        elif units == "a.u.":
            st.markdown(
            f"**Ion** : ${ion_name}$  \n"
            f"**Configuration initiale** : ${config_initial}$ ({energy_init/(2*Constant.Rydberg_constant):.{precision}f} a.u.)  \n"
            f"**Configuration finale** : ${config_final}$ ({energy_final/(2*Constant.Rydberg_constant):.{precision}f} a.u.)")

            st.markdown(
            f"### Énergie de la transition : **{energy_transition/(2*Constant.Rydberg_constant):.{precision}f} a.u.**")
        
        # Results in Rydberg
        elif units == "Rydberg":
            st.markdown(
            f"**Ion** : ${ion_name}$  \n"
            f"**Configuration initiale** : ${config_initial}$ ({energy_init/Constant.Rydberg_constant:.{precision}f} Ry)  \n"
            f"**Configuration finale** : ${config_final}$ ({energy_final/Constant.Rydberg_constant:.{precision}f} Ry)")

            st.markdown(
            f"### Énergie de la transition : **{energy_transition/Constant.Rydberg_constant:.{precision}f} Ry**")






 
