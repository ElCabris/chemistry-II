#!/bin/bash

# Verifica si se pasó el nombre de la carpeta
if [ -z "$1" ]; then
    echo "Uso: $0 <carpeta>"
    exit 1
fi

carpeta="$1"
archivo="$carpeta/xtbopt.log"

if [ ! -f "$archivo" ]; then
    echo "No se encontró xtbopt.log en $carpeta"
    exit 1
fi

energia=$(grep "energy:" "$archivo" | tail -n 1 | awk '{print $2}')

echo "$energia"
