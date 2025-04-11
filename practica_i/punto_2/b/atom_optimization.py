# molecule de ase.build permite crear moleculas. Recibe el nombre de la molecula y las dimensiones de la celda
from ase.build import molecule

# Esta importación es para especificar el tipo de datos Atoms de ase (opcional)
from ase.atoms import Atoms

# Se importa el algoritmo de optmización BFGS (Broyden-Fletcher-Goldfarb-Shanno). Se usar para minimizar la energía de la molécula.
from ase.optimize import BFGS

# Se importa el motor de cálculo GPAW, con este se va a calcular la energía y fuerzas para la molecula (DFT)
from gpaw import GPAW

# módulo de python para interactual con el sistema operativo (se usa paracrear las carpetas)
import os


def create_dir(name) -> None:
    """Crea una carpeta con un nombre dado"""
    try:
        os.mkdir(name)
        print(f"directory {name} is ready")
    except OSError as error:
        print(f"Error creating directory '{name}' : {error}")

# función para crear las moleculas
def create_molecule(name: str) -> Atoms:
    # Crea una molécula dentro de una celda 8x8x8
    result: Atoms = molecule(name, cell=[8, 8, 8])
    # centra la molécula en el centro de la celda para evitar que quede pegada a un borde
    result.center()
    # Crea una carpeta con el nombre de la molecula
    create_dir(result.get_chemical_formula())
    # Asigna el calculador GPAW a la molecula
    result.calc = GPAW(
        # funcional de intercambio (PBE)
        xc="PBE",

        # método de cálculo basado en orbitales lineales combinados
        mode="lcao",

        # base de datos zeta polarizada
        basis="dzp",

        # archivo donde se guardn los resultados del cálculo
        txt=f"{result.get_chemical_formula()}/{result.get_chemical_formula()}.txt",
    )

    # retorna el objeto Atoms anteriormente configurado
    return result


def relax_molecule(molecule: Atoms) -> None:
    # se asegura que la carpeta exista
    create_dir(molecule.get_chemical_formula())

    # Crea un objeto optimizador que minimiza la energía total
    relax = BFGS(
        # se pasa la molecula para optimizar
        molecule,
        
        # archivo de texto con el registro del proceso de relajación
        logfile=f"{molecule.get_chemical_formula()}/{molecule.get_chemical_formula()}_calc.txt",
        
        # archivo donde se guarda la evolución de la estructura durante la relajación
        trajectory=f"{molecule.get_chemical_formula()}/{molecule.get_chemical_formula()}_calc.traj",
    )

    # Ejecuta la relajación hasta que las fuerzas sobre todos los átomos sean menores a 0.05 eV/A.
    relax.run(fmax=0.05)
