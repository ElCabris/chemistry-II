import os
from ase.build import molecule
from ase.io import read
from ase.atoms import Atoms
import subprocess

PATH_IR = "ir"
PATH_OPT = "opt"
POINT_DIR = "punto_1"


def opt_molecule(mol: Atoms):
    name = mol.get_chemical_formula()
    mol_path = os.path.join(POINT_DIR, PATH_OPT, name)
    os.makedirs(mol_path, exist_ok=True)

    xyz_filename = f"{name}.xyz"
    xyz_path = os.path.join(mol_path, xyz_filename)

    mol.write(xyz_path, format="xyz")
    subprocess.run(["xtb", xyz_filename, "--opt"], cwd=mol_path, check=True)


def ir_molecule(xyz_file: str):
    name = read(xyz_file, format="xyz").get_chemical_formula()
    mol_path = os.path.join(POINT_DIR, PATH_IR, name)
    os.makedirs(mol_path, exist_ok=True)

    subprocess.run(
        f"xtb {os.path.abspath(xyz_file)} --hess > {name}_hess.out",
        cwd=mol_path,
        shell=True,
    )


def create_molecules() -> list[Atoms]:
    return [
        molecule("H2", cell=[5, 5, 5]),
        molecule("Cl2", cell=[5, 5, 5]),
        molecule("HCl", cell=[5, 5, 5]),
    ]


if __name__ == "__main__":
    molecules = create_molecules()

    for mol in molecules:
        mol.center()
        opt_molecule(mol)
        ir_molecule(f"{POINT_DIR}/{PATH_OPT}/{mol.get_chemical_formula()}/xtbopt.xyz")
