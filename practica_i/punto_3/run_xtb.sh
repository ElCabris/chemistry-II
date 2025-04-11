#!/bin/bash

for dir in */; do
    echo "Entrando en: $dir"
    cd "$dir" || continue

    if compgen -G "*.xyz" > /dev/null; then
        echo "Ejecutando: xtb *.xyz --opt"
        xtb *.xyz --opt
    else
        echo "No se encontraron archivos .xyz en $dir"
    fi

    cd ..
done
