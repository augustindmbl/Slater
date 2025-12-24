import csv
import os

import Constant
import Functions

# ----------------------- #
### TO COMPLETE ###
# ----------------------- #

atomic_number = 18
method = "Mendozza"  # "Mendozza", "Lanzini" or "Faussurier"
directory = "/Users/demontbel/Desktop"
input_file = "input_Ar9+.csv"


# ----------------------- #
### PARAMETERS ###
# ----------------------- #

output_file = input_file.split(".csv")[0].split("_")[1] + f"_{method}_output.csv"

input_path = os.path.join(directory, input_file)
output_path = os.path.join(directory, output_file)

if method == "Mendozza":
    screen_constants = Functions.read_csv_screening_constants(Constant.file_path_mendozza)

elif method == "Lanzini":
    screen_constants = Functions.read_csv_screening_constants(Constant.file_path_lanzini)

elif method == "Faussurier":
    screen_constants = Functions.read_csv_screening_constants(Constant.file_path_faussurier)


# ----------------------- #
### MAIN LOOP ###
# ----------------------- #

with open(input_path, newline='', encoding='utf-8-sig') as f_in, \
     open(output_path, 'w', newline='', encoding='utf-8-sig') as f_out:

    reader = csv.reader(f_in, delimiter=';')
    writer = csv.writer(f_out, delimiter=';')

    config_final = next(reader)
    config_final = [int(x) for x in config_final]
    print("Config init:",config_final)

    for i, ligne in enumerate(reader):
        config_init = [int(x) for x in ligne]
        
        energy_init = Functions.energy_configuration(atomic_number, config_init, screen_constants)
        energy_final = Functions.energy_configuration(atomic_number, config_final, screen_constants) 
        energy_transition = energy_final - energy_init

        config_init.append("")
        config_init.append(round(energy_transition, 2))

        writer.writerow(config_init)

print("✅ Traitement terminé : fichier écrit dans", output_file)

