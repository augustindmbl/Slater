""" All physical constants / Usefull dictionaries to manipulate orbital configuration and atoms / Path to screening constants csv
"""

import os

# Physical constants
mass_electron = 9.10939*10**(-31)  # (in kg)
light_speed = 2.99792*10**8  # (in m/s)
fine_structure_constant = 1/137.03 
eV = 1.60218*10**(-19)  # (in J) 
Rydberg_constant = 13.60569  # (in eV)
Ht = 2*Rydberg_constant # (in eV)

# Dictionaries
orbital_dict = {"1s1/2": 0, 
                "2s1/2": 1, 
                "2p1/2": 2, 
                "2p3/2": 3, 
                "3s1/2": 4, 
                "3p1/2": 5, 
                "3p3/2": 6, 
                "3d3/2": 7, 
                "3d5/2": 8, 
                "4s1/2": 9, 
                "4p1/2": 10, 
                "4p3/2": 11, 
                "4d3/2": 12, 
                "4d5/2": 13, 
                "4f5/2": 14, 
                "4f7/2": 15,
                "5s1/2": 16, 
                "5p1/2": 17, 
                "5p3/2": 18, 
                "5d3/2": 19, 
                "5d5/2": 20, 
                "6s1/2": 21, 
                "6p1/2": 22, 
                "6p3/2": 23}

orbital_dict_inv = {v: k for k, v in orbital_dict.items()} # Reverse orbital dictionary

orbital_latex_dict = {0: "1s_{1/2}",
    1: "2s_{1/2}",
    2: "2p_{1/2}",
    3: "2p_{3/2}",
    4: "3s_{1/2}",
    5: "3p_{1/2}",
    6: "3p_{3/2}",
    7: "3d_{3/2}",
    8: "3d_{5/2}",
    9: "4s_{1/2}",
    10: "4p_{1/2}",
    11: "4p_{3/2}",
    12: "4d_{3/2}",
    13: "4d_{5/2}",
    14: "4f_{5/2}",
    15: "4f_{7/2}",
    16: "5s_{1/2}",
    17: "5p_{1/2}",
    18: "5p_{3/2}",
    19: "5d_{3/2}",
    20: "5d_{5/2}",
    21: "6s_{1/2}",
    22: "6p_{1/2}",
    23: "6p_{3/2}"}

element_atomic_number_dict = {"Hydrogen (1)": 1,
    "Helium (2)": 2,
    "Lithium (3)": 3,
    "Beryllium (4)": 4,
    "Boron (5)": 5,
    "Carbon (6)": 6,
    "Nitrogen (7)": 7,
    "Oxygen (8)": 8,
    "Fluorine (9)": 9,
    "Neon (10)": 10,
    "Sodium (11)": 11,
    "Magnesium (12)": 12,
    "Aluminum (13)": 13,
    "Silicon (14)": 14,
    "Phosphorus (15)": 15,
    "Sulfur (16)": 16,
    "Chlorine (17)": 17,
    "Argon (18)": 18}

element_symbol_dict = {
    "Hydrogen (1)": "H",
    "Helium (2)": "He",
    "Lithium (3)": "Li",
    "Beryllium (4)": "Be",
    "Boron (5)": "B",
    "Carbon (6)": "C",
    "Nitrogen (7)": "N",
    "Oxygen (8)": "O",
    "Fluorine (9)": "F",
    "Neon (10)": "Ne",
    "Sodium (11)": "Na",
    "Magnesium (12)": "Mg",
    "Aluminum (13)": "Al",
    "Silicon (14)": "Si",
    "Phosphorus (15)": "P",
    "Sulfur (16)": "S",
    "Chlorine (17)": "Cl",
    "Argon (18)": "Ar"}


l_dict = {"s": 0, 
          "p": 1, 
          "d": 2, 
          "f": 3}


# File path for screening constants and automatic configuration
directory = os.getcwd()  

file_path_mendozza = os.path.join(directory, "Screening constants/mendozza_constants.csv")
file_path_lanzini = os.path.join(directory, "Screening constants/lanzini_constants.csv")
file_path_faussurier = os.path.join(directory, "Screening constants/faussurier_constants.csv")