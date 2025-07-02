""" Functions for reading csv / Calculate energies or effective charge
"""

import csv
import numpy as np
import Constant

def read_csv_screening_constants(filepath):
    """Reads a CSV file (separator = ';'), removes the first row and the first column,
    then returns a NumPy array with the remaining data.

    Args:
        filepath (str): Path to the CSV file.

    Returns:
        np.ndarray: CSV data as a NumPy array (without the first row and column).
    """

    with open(filepath, 'r', newline='') as f:
        reader = csv.reader(f, delimiter=';')
        rows = list(reader)[1:]  # Delete first row (orbital name)

    # Delete first column (orbital name)
    data = [row[1:] for row in rows if len(row) > 1]

    return np.array(data, dtype=float)

def read_orbital (orbital):
    """Takes a string of the form '4f7/2' and returns a tuple (n, l, j).

    Args:
        string (str): String representing the orbital, in the format 'nlj' 
                    (e.g., '4f7/2'), where:
                    - n is the principal quantum number,
                    - l is the spectroscopic letter (s, p, d, f),
                    - j is the total angular momentum.

    Returns:
        tuple: A tuple (n, l, j) where:
            - n (int): Principal quantum number.
            - l (int): Orbital angular momentum quantum number (0=s, 1=p, 2=d, 3=f).
            - j (float): Total angular momentum.
    """

    # Extract n (first character)
    n = int(orbital[0])

    # Extract and convert l (second character)
    l_char = orbital[1]
    l = Constant.l_dict[l_char]

    # Extract j (possibly "1/2", "3/2", etc.)
    j_str = orbital[2:]
    num, denom = j_str.split('/')
    j = int(num) / int(denom)
   
    return n, l, j

def read_orbital_in_char (orbital):
    """Takes a string of the form '4f7/2' and returns a tuple (n, l, j).

    Args:
        string (str): String representing the orbital, in the format 'nlj' 
                    (e.g., '4f7/2'), where:
                    - n is the principal quantum number,
                    - l is the spectroscopic letter (s, p, d, f),
                    - j is the total angular momentum.

    Returns:
        tuple: A tuple (n, l, j) where:
            - n (int): Principal quantum number.
            - l (string): Orbital angular momentum quantum number (s, p, d, f).
            - j (string): Total angular momentum (1/2, 3/2, ...).
    """

    # Extract n (first character)
    n = int(orbital[0])

    # Extract l (second character)
    l_char = orbital[1]

    # Extract j (possibly "1/2", "3/2", etc.)
    j_str = orbital[2:]
   
    return n, l_char, j_str


def energy_orbital(orbital, effecive_charge):
    """Calculates the energy of a given orbital based on the effective charge using Dirac's formula.

    Args:
        orbital (str): Name of the orbital (e.g., "1s1/2").
        effective_charge (float): Effective charge of the orbital.

    Returns:
        float: Energy of the orbital in eV.
    """

    n, l , j = read_orbital(orbital)

    energy = Constant.mass_electron*Constant.light_speed**2*((1 + 
            (Constant.fine_structure_constant*effecive_charge/(n - j - 0.5 + np.sqrt((j + 0.5)**2 - 
            (Constant.fine_structure_constant*effecive_charge)**2)))**2)**(-1/2) - 1) / Constant.eV

    return energy


def screened_charge(atomic_number, orbital, config, screen_constants):
    """Calculates the effective charge seen by an electron based on the electronic configuration.

    Args:
        atomic number (int).
        orbital (str): Name of the orbital (e.g., "1s1/2").
        config (list): Electronic configuration as a list of occupations.
        screen_constants (array): Array of screening constants.

    Returns:
        float: Effective charge seen by the electron in the orbital.
    """

    orbital_index = Constant.orbital_dict[orbital]
    effective_charge = atomic_number

    for index, occupation in enumerate(config):
            if orbital_index == index:
                effective_charge -= screen_constants[orbital_index][index]*(occupation - 1)
            
            else:
                effective_charge -= screen_constants[orbital_index][index]*occupation

    return effective_charge


def energy_configuration(atomic_number, config, screen_constants):
    """Calculates the total energy of the configuration.

    Args:
        atomic number (int).
        config (list): Electronic configuration as a list with occupation numbers for each orbital.
        screen_constants (array): Array of screening constants.

    Returns:
        float: Total energy of the configuration in eV.
    """

    energy_total = 0
    # Sum on orbtal's energy
    for index, occupation in enumerate(config):
        if occupation != 0:
            orbital = Constant.orbital_dict_inv[index]
            
            effective_charge = screened_charge(atomic_number, orbital, config, screen_constants)
            energy = energy_orbital(orbital, effective_charge)
            
            energy_total += occupation*energy

    return energy_total

def print_config(config_list):
    """Builds the string that will display the electronic configuration in LaTeX format (interpreted as a raw string).

    Args:
        config (list): Electronic configuration as a list with occupation numbers for each orbital.

    Returns:
        str: Configuration in LaTeX format.
    """

    config = ""

    for index, value in enumerate(config_list):
        if value != 0:
            config += Constant.orbital_latex_dict[index] + "^{"+ str(int(value)) + "}" + r"\;"
    
    return config

def external_screening(atomic_number, orbital, config, screen_constants):
    """Calculates the relativistic external screening for an orbital.

    Args:
        atomic number (int).
        orbital (str): Name of the orbital (e.g., "1s1/2").
        config (list): Electronic configuration as a list of occupations.
        screen_constants (array): Array of screening constants.

    Returns:
        float: Relativistic external screening for an orbital in eV.
    """

    # Index of the orbital for which we want to calculate the external screening
    orbital_index = Constant.orbital_dict[orbital]
    
    # Loop over non empty orbital
    total_external_screening = 0
    for index, occupation in enumerate(config):

        if occupation != 0:
            
            # Current orbital over the loo
            current_orbital = Constant.orbital_dict_inv[index]
            n, l, j = read_orbital(current_orbital)

            # Effective charge seen by the current orbital
            effective_charge = screened_charge(atomic_number, current_orbital, config, screen_constants)

            # Coefficients of Mendozza's paper
            a = n - j - 0.5
            b = (j + 0.5)**2

            c = a + np.sqrt(b - (Constant.fine_structure_constant*effective_charge)**2) # c = a + sqrt(b - (alpha*Q)²)

            # Decomposition of the calculation to avoid error
            A = (1 + (Constant.fine_structure_constant*effective_charge/c)**2)**(-1.5)
            B = Constant.fine_structure_constant*effective_charge/c
            C = Constant.fine_structure_constant*(a*np.sqrt(b - (Constant.fine_structure_constant*effective_charge)**2) + b)/(np.sqrt(b - (Constant.fine_structure_constant*effective_charge)**2)*c**2)

            total_external_screening += occupation*screen_constants[index][orbital_index]*A*B*C

    return total_external_screening*Constant.mass_electron*(Constant.light_speed**2) / Constant.eV

def binding_energy_alpha (atomic_number, orbital, config, screen_constants):
    """Calculates the binding energy of an electron in a specific orbital with the K_alpha model.

    Args:
        atomic number (int).
        orbital (str): Name of the orbital (e.g., "1s1/2").
        config (list): Electronic configuration as a list of occupations.
        screen_constants (array): Array of screening constants.

    Returns:
        float: Binding energy of the electron in eV.
    """
    
    effective_charge = screened_charge(atomic_number, orbital, config, screen_constants) # Effective charge seen by the considered orbital

    orbital_energy = energy_orbital(orbital, effective_charge) # Energy of the orbital
    orbital_external_screening = external_screening(atomic_number, orbital, config, screen_constants) # External screening of the orbital

    binding_energy = orbital_energy + orbital_external_screening

    return binding_energy

def binding_energy_HF (atomic_number, orbital, config, screen_constants):
    """Calculates the binding energy of an electron in a specific orbital with the Hartree-Fock model.

    Args:
        atomic number (int).
        orbital (str): Name of the orbital (e.g., "1s1/2").
        config (list): Electronic configuration as a list of occupations.
        screen_constants (array): Array of screening constants.

    Returns:
        float: Binding energy of the electron in eV.
    """
    
    # Properties of the considered orbital
    n, l ,j = read_orbital(orbital)
    orbital_index = Constant.orbital_dict[orbital]
    effective_charge = screened_charge(atomic_number, orbital, config, screen_constants)

    # Binding energy with the K_alpha model
    energy_alpha = binding_energy_alpha(atomic_number, orbital, config, screen_constants)
    
    # Coefficients of Mendozza's paper (with errors correction)
    k = j + 0.5
    n_tilde = n - k + np.sqrt(k**2 - (Constant.fine_structure_constant*effective_charge)**2)

    #Radius of the orbital in relativistic approximation
    orbital_radius = n_tilde*np.sqrt(n_tilde**2 + (Constant.fine_structure_constant*effective_charge)**2)/effective_charge

    energy_HF  = energy_alpha - Constant.Ht*screen_constants[orbital_index][orbital_index]/orbital_radius

    return energy_HF 

