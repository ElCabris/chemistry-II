from punto_1.punto_1 import create_molecules
from ase.atoms import Atoms
import os
import shutil
from thermo_xtb_mod import calculate_thermo


DIR_POINT_2 = "punto_2"
DIR_POINT_1 = "punto_1"


def cp_ir_files(mol: Atoms) -> None:
    NAME_MOL = mol.get_chemical_formula()
    IR_PATH = f"{DIR_POINT_1}/ir/{NAME_MOL}"
    FIND_FILES = ["vibspectrum", f"{NAME_MOL}_hess.out"]

    for file in FIND_FILES:
        print(f"{IR_PATH}/{file}")
        shutil.copy(f"{IR_PATH}/{file}", f"{DIR_POINT_2}/{NAME_MOL}")


molecules = create_molecules()
temperatures: list[float] = [300.0, 350.0, 400.0, 500.0, 800.0]

for mol in molecules:
    name = mol.get_chemical_formula()
    mol_path = f"{DIR_POINT_2}/{name}"
    os.mkdir(mol_path)
    cp_ir_files(mol)
    calculate_thermo(
        temperatures,
        f"{mol_path}/vibspectrum",
        f"{mol_path}/{name}_hess.out",
        f"{mol_path}/thermodynamics_output.txt",
    )
