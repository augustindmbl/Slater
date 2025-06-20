import csv
import numpy as np
import Constant

def read_csv_screening_constants(filepath):
    """ Lit un fichier CSV (séparateur = ;), supprime la première ligne et la première colonne,
    puis retourne un tableau NumPy avec les données restantes.

    Args:
        filepath (str): Chemin vers le fichier CSV.

    Returns:
        np.ndarray: Données du CSV sous forme de tableau NumPy (sans la première ligne/colonne).
    """

    with open(filepath, 'r', newline='') as f:
        reader = csv.reader(f, delimiter=';')
        rows = list(reader)[1:]  # Supprime la première ligne (nom des orbitales)

    # Supprime la première colonne de chaque ligne (nom des orbitales)
    data = [row[1:] for row in rows if len(row) > 1]

    return np.array(data, dtype=float)


def read_csv_config(filepath, mode="init"):
    """ Lit un fichier CSV séparé par des points-virgules, supprime la première ligne
    et la première colonne, puis retourne la ligne spécifiée :
    
    - mode="init" : première ligne restante
    - mode="final" : dernière ligne restante

    Retourne un tableau NumPy 1D.
    """
    
    if mode not in ["init", "final"]:
        raise ValueError("Le paramètre 'mode' doit être 'init' ou 'final'.")

    with open(filepath, 'r', newline='') as f:
        reader = csv.reader(f, delimiter=';')
        rows = list(reader)[1:]  # Supprime la première ligne (nom des orbitales)

    # Supprime la première colonne de chaque ligne (nom de la configuration)
    data = [row[1:] for row in rows if len(row) > 1]

    if not data:
        raise ValueError("Le fichier ne contient pas de données après suppression.")

    # Choix de la ligne
    line = data[0] if mode == "init" else data[-1]

    return np.array(line, dtype=float)


def read_orbital (orbital):
    """Prend une chaîne de type '4f7/2' et retourne un tuple (n, l, j)
    où :
    - n est un entier
    - l est un entier (0=s, 1=p, 2=d, 3=f)
    - j est un float (par ex. 1.5)
    """
    # Dictionnaire pour convertir lettre -> l
    l_dict = {'s': 0, 'p': 1, 'd': 2, 'f': 3}

    # Extraire n (chiffre au début)
    n = int(orbital[0])

    # Extraire l (lettre unique : s, p, d, f)
    l_char = orbital[1]
    l = l_dict[l_char]

    # Extraire j (peut être "1/2", "3/2", etc.)
    j_str = orbital[2:]
    if '/' in j_str:
        num, denom = j_str.split('/')
        j = int(num) / int(denom)
    else:
        j = float(j_str)  # Pour les cas comme "1s0" (rare mais possible en modèle)

    return n, l, j


def energy_orbital(orbital, effecive_charge):
    """ Calcule l'énergie d'une orbitale donnée en fonction de la charge effective à partir de la forumule de Dirac.
    Args:
        orbital (str): Nom de l'orbital (par exemple, "1s1/2").
        effecive_charge (float): Charge effective de l'orbital.
    Returns:
        float: Énergie de l'orbital en eV.
    """

    n, l , j = read_orbital(orbital)

    energy = Constant.mass_electron*Constant.light_speed**2*((1 + 
            (Constant.fine_structure_constant*effecive_charge/(n - j - 0.5 + np.sqrt((j + 0.5)**2 - (Constant.fine_structure_constant*effecive_charge)**2)))**2)**(-1/2) - 1) / Constant.eV

    return energy


def screened_charge(atomic_number, orbital, config, screen_constants):
    """ Calcule la charge effective vu par un électron à partir de la configuration électronique.
    Args:
        orbital (str): Nom de l'orbital (par exemple, "1s1/2").
        config (str): Configuration électronique sous forme de chaîne (par exemple, "1s1/2 2s1/2 2p1/2").
        screen_constants (array): Tableau des constantes d'écrantages.
    Returns:
        float: Charge effective vue par l'électron dans l'orbital.
    """

    orbital_index = Constant.orbital_dict[orbital]
    effective_charge = atomic_number

    for index, occupation in enumerate(config):
            if orbital_index == index:
                effective_charge -= screen_constants[orbital_index][index]*(occupation - 1)
            
            else:
                effective_charge -= screen_constants[orbital_index][index]*occupation

    return effective_charge


def energy_configuration(config, screen_constants):
    """ Calcule la charge effective vu par un électron à partir de la configuration électronique.
    Args:
        config (list): Configuration électronique sous forme de liste avec pour valeurs les occupations de chaque orbitale.
    Returns:
        float: Energie totale de la configuration en eV.
    """

    energy_total = 0
    for index, occupation in enumerate(config):
        if occupation != 0:
            orbital = Constant.orbital_dict_inv[index]
            
            effective_charge = screened_charge(orbital, config, screen_constants)
            energy = energy_orbital(orbital, effective_charge)
            
            energy_total += occupation*energy

    return energy_total