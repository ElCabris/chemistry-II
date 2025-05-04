import re
from sre_parse import parse
from punto_1.punto_1 import create_molecules


def parse_thermo_output(file_path):
    data = {}
    with open(file_path, "r") as f:
        lines = f.readlines()

    current_temp = None
    for line in lines:
        temp_match = re.match(r"--- (\d+\.\d) K ---", line)
        if temp_match:
            current_temp = float(temp_match.group(1))
            data[current_temp] = {}
            continue

        if current_temp is not None:
            if "Zero-point energy" in line:
                data[current_temp]["ZPE"] = float(
                    re.search(r"([-]?\d+\.?\d*) eV", line).group(1)
                )
            elif "Enthalpy" in line:
                data[current_temp]["H"] = float(
                    re.search(r"([-]?\d+\.?\d*) eV", line).group(1)
                )
            elif "Entropy" in line:
                match = re.search(
                    r"([-]?\d+\.?\d*) kcal/\(mol·K\).*?([-]?\d+\.?\d*) eV/K", line
                )
                data[current_temp]["S_kcal"] = float(match.group(1))
                data[current_temp]["S_eV"] = float(match.group(2))
            elif "Gibbs Free Energy" in line:
                data[current_temp]["G"] = float(
                    re.search(r"([-]?\d+\.?\d*) eV", line).group(1)
                )

    return data


PATH_POINT_2 = "punto_2"
PATH_POINT_3 = "punto_3"

temps = [300.0, 350.0, 400.0, 500.0, 800.0]

if __name__ == "__main__":
    molecules = create_molecules()

    results = {}

    for mol in molecules:
        name = mol.get_chemical_formula()
        results[name] = parse_thermo_output(
            f"{PATH_POINT_2}/{name}/thermodynamics_output.txt"
        )

    for T in temps:
        H = 0
        S = 0
        for mol in molecules:
            name = mol.get_chemical_formula()
            if name == "HCL":
                H += 2 * results[name][T]["H"]
                S += 2 * results[name][T]["S_eV"]
            else:
                H -= results[name][T]["H"]
                S -= results[name][T]["S_eV"]
        G = H - T * S
        print(f"para la temperatura {T} se tiene: H (eV) = {H}, S (eV) = {S}, G = {G}")
