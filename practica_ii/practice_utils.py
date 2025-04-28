def get_charges(path: str, n_atoms: int) -> list[float]:
    """
    función para obtener las cargas de los átomos desde un archivo 'charges'
    generado por xtb

    Parámetros:
    - path: ruta al archivo charges
    - n_atoms: cantidad de átomos de la molécula
    """

    with open(path, 'r') as file:
        lines = file.readlines()

    return [float(lines[i]) for i in range(n_atoms)]

def get_wbo(path: str) -> dict[int, dict[int, float]]:
    """
    función para obtener los ordenes de enlace para una molécula
    
    parámetros:
    - path: ruta al archivo 'wbo'
    """
    
    bonds: dict[int, dict[int, float]] = {}
    
    with open(path, 'r') as file:
        for line in file:
            line = line.split()
            line[0] = int(line[0]) - 1 # se le resta 1 para poder hacer la transformación de base 1 a base 0
            line[1] = int(line[1]) - 1
            line[2] = float(line[2])
            
            if line[0] not in bonds:
                bonds[line[0]] = {}
            
            bonds[line[0]][line[1]] = line[2]

            if line[1] not in bonds:
                bonds[line[1]] = {}

            # Se agrega la relación inversa al diccionario
            bonds[line[1]][line[0]] = line[2]

    return bonds

def get_type_wbo(bound: float) -> float:
    """
    función para hacer el redondo e identicar el orden de enlace
    de una molecula

    parámetros:
    bounds: el número wbo
    """

    bounds_types = (1, 1.5, 2, 2.5, 3)
    # se retorna la mínima distancia entre los posibles tipos de wbo
    return min(bounds_types, key=lambda x: abs(x - bound))

def count_elements(path: str) -> int:
    """
    función para contar los elementos de
    la matriz hessina

    Parámetros:
    path: ruta a la matriz hessiana
    """
    result: int = 0
    with open(path, 'r') as file:
        for line in file:
            line = line.split()
            if '$hessian' in line:
                continue
            result += len(line)
    return result

def vibrational_spectrum_count(path: str) -> int:
    """
    función para contar la cantidad de modos normales de vibración
    generados desde un archivo vimspectrum
    """
    result: int = 0
    with open(path, 'r') as file:
        for line in file:
            line = line.split()
            # se agregan aquellos que la regla de selección sea 'YES'
            if 'YES' in line:
                result += 1
    return result
            