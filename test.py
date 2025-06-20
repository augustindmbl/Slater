import streamlit as st # type: ignore
from streamlit_autorefresh import st_autorefresh # type: ignore
import os
import time

# Initialiser la liste des orbitales dans la session
if "orbitals" not in st.session_state:
    st.session_state.orbitals = []

# Dictionnaire des l → lettres et j possibles
l_dict = {"s": 0, "p": 1, "d": 2, "f": 3}
j_options = {
    0: [0.5],
    1: [0.5, 1.5],
    2: [1.5, 2.5],
    3: [2.5, 3.5],
}

st.title("Configuration électronique")

# Bouton pour ajouter une orbitale
if st.button("➕ Ajouter une orbitale"):
    st.session_state.orbitals.append({"n": 1, "l": "s", "j": 0.5, "occupation": 0})

# Affichage des orbitales
for i, orbital in enumerate(st.session_state.orbitals):
    cols = st.columns([1, 1, 1, 1, 0.5])
    with cols[0]:
        st.session_state.orbitals[i]["n"] = st.selectbox(f"n {i+1}", range(1, 8), key=f"n_{i}")
    with cols[1]:
        st.session_state.orbitals[i]["l"] = st.selectbox(f"l {i+1}", ["s", "p", "d", "f"], key=f"l_{i}")
    with cols[2]:
        l_value = l_dict[st.session_state.orbitals[i]["l"]]
        st.session_state.orbitals[i]["j"] = st.selectbox(f"j {i+1}", j_options[l_value], key=f"j_{i}")
    with cols[3]:
        st.session_state.orbitals[i]["occupation"] = st.number_input(f"Occupation {i+1}", min_value=0, max_value=20, step=1, key=f"occ_{i}")
    with cols[4]:
        if st.button("❌", key=f"remove_{i}"):
            st.session_state.orbitals.pop(i)
            st.rerun()

# Bouton de validation
if st.button("✅ Valider la configuration"):
    config = []
    for orb in st.session_state.orbitals:
        n = orb["n"]
        l = orb["l"]
        j = orb["j"]
        occ = orb["occupation"]
        config.append(f"({n}{l}{j:.1f})^{occ}")
    st.success("Configuration : " + ", ".join(config))


# 🔒 Auto-fermeture après 5 minutes d'inactivité


count = st_autorefresh(interval=60000, key="auto_refresh")  # 60 sec

if "last_ping" not in st.session_state:
    st.session_state.last_ping = time.time()
else:
    if time.time() - st.session_state.last_ping > 300:  # 5 min
        st.write("Inactivité détectée, fermeture du serveur...")
        time.sleep(2)
        os._exit(0)
    else:
        st.session_state.last_ping = time.time()
