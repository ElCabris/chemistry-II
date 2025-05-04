# Explicación punto 2

## `vibspectrum`
Este archivo tiene las frecuencias vibracionales. Estas frecuencias a fectan a los potenciales termodinámicos de la siguiente forma:

### Energía del punto cero
$$
E_{ZEP} = \frac{1}{2} \sum_{i = 1}^{N}v_{i}^{kcal/mol}
$$

### Entalpía vibracional $H_{vib}$
$$
H_{vib} = \sum_{i = 1}^{N} \frac{v_{i}^{kcal/mol}}{exp\left(\frac{v_{i}^{kcal/mol}}{kdi{RT}\right) - 1}
$$

### Entropía vibracional $S_{vib}$
$$
S_{vib} = R \sum_{i = 1}^{N}\left[\frac{x_{i}}{exp(x_{i} - 1)} - \ln{(1 - exp(-x_{i}))}\right]
$$
donde:
$$
x_{i} = \frac{v_{i}^{kmol/mol}}{RT}
$$

### Energía libre de Gibbs $G$
$$
G = H_{total} - TS_{total}
$$

donde:
$$
S_{total} = S_{vib} + S_{rot} + S_{trans}
$$

## `name_hess.out`

## Entalpía total (con energía electrónica SCF incluida)
$$
H_{total} = E_{SCF} + H_{vib} + H_{rot} + H_{trans}
$$
donde:
- $E_{SCF} es la energía electrónica botenida del cálculo cuántico (SCF),
- $H_{vib}, H_{rot}, H_{trans}$ son las contribuciones térmicas vibracional, rotacional y tranlacional, respectivamente.

### Energía libre de Gibbs total (incluyendo ZPE)
$$
G_{total} = H_{total} - TS_{total} + ZPE
$$
donde:
- $T$ es la temperatura
- $S_{total} = S_{vib} + S_{rot} + S_{trans}$ es la entropía$
- $ZPE$ es la energía de punto cero, que se añade explícitamente.

**Las anteriores ecuaciones fueron sacadas del archivo `script_thermoo_xtb_complete_all.py`**
