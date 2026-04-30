#!/bin/bash
# Skill: system-check
# Descripción: Verifica el estado del sistema

echo "Verificando estado del sistema..."
echo "Uso de CPU: $(top -bn1 | grep '%Cpu' | awk '{print $2}')"
echo "Uso de Memoria: $(free -m | awk 'NR==2{printf \"%.2f%%\n\", $3*100/$2}')"
echo "Uso de Disco: $(df -h | awk '$NF=="/" {print $5}')"
echo "Fecha: $(date)"