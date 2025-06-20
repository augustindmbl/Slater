import os


# Physical constants
mass_electron = 9.10939*10**(-31)  # (en kg)
light_speed = 2.99792*10**8  # (en m/s)
fine_structure_constant = 1/137.03 
eV = 1.60218*10**(-19)  # (en J) 
Rydberg_constant = 13.60569  # (en eV)

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

element_dict = {"Hydrogen (1)": 1,
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

l_dict = {"s": 0, 
          "p": 1, 
          "d": 2, 
          "f": 3}

j_possible_dict = {0: ["1/2"], 
                   1: ["1/2", "3/2"], 
                   2: ["3/2", "5/2"], 
                   3: ["5/2", "7/2"]}

# File path for screening constants and automatic configuration
directory = os.getcwd()  

file_path_mendozza = os.path.join(directory, "mendozza_constants.csv")
file_path_lanzini = os.path.join(directory, "lanzini_constants.csv")
file_path_config = os.path.join(directory, "config.csv")