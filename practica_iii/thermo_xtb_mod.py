from script_thermo_xtb_complete_all import *


def calculate_thermo(
    temperatures: list[float],
    vibspectrum_file: str,
    out_file: str,
    resutl_path: str = "thermodynamics_output.txt",
):

    # Extract data
    frequencies = extract_frequencies(vibspectrum_file)
    if not frequencies:
        print("No valid frequencies found.")
        exit()

    scf_energy_hartree = extract_scf_energy(out_file)
    scf_energy_eV = scf_energy_hartree * hartree_to_eV

    with open(resutl_path, "w") as f:
        f.write(
            f"Thermodynamic properties (vibrational + ZPE + SCF) from {vibspectrum_file}\n"
        )
        f.write(
            f"SCF Energy extracted from {out_file}: {scf_energy_hartree:.8f} Hartree = {scf_energy_eV:.5f} eV\n\n"
        )

        for T in temperatures:
            # Here, num_atoms is provided in case you need it later;
            # Adjust 'is_linear_molecule' to False if your molecule is nonlinear.
            ZPE_eV, H_total_eV, S_total, G_total_eV_with_ZPE = thermodynamics(
                frequencies, T, num_atoms=10, is_linear_molecule=True
            )

            # Add SCF energy to the total enthalpy
            H_total_eV_with_SCF = scf_energy_eV + H_total_eV
            # Final Gibbs free energy with SCF and including ZPE explicitly
            G_total_eV_with_SCF_and_ZPE = (
                H_total_eV_with_SCF - T * (S_total * kcal_to_eV) + ZPE_eV
            )

            # Write out values. S_total is in kcal/(mol·K); we also show it in eV/K by multiplying by kcal_to_eV.
            f.write(f"--- {T:.1f} K ---\n")
            f.write(f"Zero-point energy (ZPE): {ZPE_eV:.5f} eV\n")
            f.write(f"Enthalpy (H total): {H_total_eV_with_SCF:.5f} eV\n")
            f.write(
                f"Entropy (S total): {S_total:.5f} kcal/(mol·K) or {S_total * kcal_to_eV:.5f} eV/K\n"
            )
            f.write(
                f"Gibbs Free Energy (G total, with ZPE): {G_total_eV_with_SCF_and_ZPE:.5f} eV\n\n"
            )

            print(
                f"{T:.1f} K → ZPE: {ZPE_eV:.5f} eV | H: {H_total_eV_with_SCF:.5f} eV | "
                f"S: {S_total:.5f} kcal/(mol·K) or {S_total * kcal_to_eV:.5f} eV/K | "
                f"G: {G_total_eV_with_SCF_and_ZPE:.5f} eV"
            )

    print(f"\nAll results saved to '{resutl_path}'")
