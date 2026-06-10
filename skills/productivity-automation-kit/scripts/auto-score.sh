#!/bin/bash
# Automatización Score — Evalúa si una tarea vale automatizar
# Uso: bash auto-score.sh "nombre de la tarea"

TASK_NAME="${1:-Tarea no especificada}"

echo "╔══════════════════════════════════════════════════╗"
echo "║   MATRIZ DE PUNTUACIÓN DE AUTOMATIZACIÓN        ║"
echo "╠══════════════════════════════════════════════════╣"
echo "║  Evalúa: $TASK_NAME"
echo "╚══════════════════════════════════════════════════╝"
echo ""
echo "Responde con un número (0-3) para cada dimensión:"
echo ""

# Frecuencia
echo "📊 FRECUENCIA (0-3)"
echo "  0 = Mensual"
echo "  1 = Semanal"
echo "  2 = Diario"
echo "  3 = Varias veces al día"
read -p "  → " FREQ

# Tiempo
echo ""
echo "⏱️  TIEMPO POR EJECUCIÓN (0-3)"
echo "  0 = <5 minutos"
echo "  1 = 5-15 minutos"
echo "  2 = 15-60 minutos"
echo "  3 = >1 hora"
read -p "  → " TIME

# Impacto
echo ""
echo "💥 IMPACTO DE ERROR (0-3)"
echo "  0 = Sin impacto"
echo "  1 = Inconveniente menor"
echo "  2 = Requiere corrección"
echo "  3 = Pérdida financiera/reputacional"
read -p "  → " IMPACT

# Complejidad
echo ""
echo "🧩 COMPLEJIDAD (0-3)"
echo "  0 = Muchas decisiones (>5)"
echo "  1 = Varias decisiones (3-4)"
echo "  2 = Pocas decisiones (1-2)"
echo "  3 = Regla pura (sin decisiones)"
read -p "  → " COMPLEX

# Calcular total
TOTAL=$((FREQ + TIME + IMPACT + COMPLEX))

echo ""
echo "═══════════════════════════════════════════════════"
echo "  RESULTADO: $TOTAL/12 puntos"
echo "═══════════════════════════════════════════════════"
echo ""

if [ "$TOTAL" -ge 10 ]; then
  echo "🟢 RECOMENDACIÓN: AUTOMATIZAR INMEDIATAMENTE"
  echo "   Esta tarea genera alto valor al automatizarla."
elif [ "$TOTAL" -ge 7 ]; then
  echo "🟡 RECOMENDACIÓN: AUTOMATIZAR PRONTO"
  echo "   Vale la pena, pero no es urgente."
elif [ "$TOTAL" -ge 4 ]; then
  echo "🟠 RECOMENDACIÓN: CONSIDERAR"
  echo "   Automatizar solo si tienes tiempo extra."
else
  echo "🔴 RECOMENDACIÓN: NO AUTOMATIZAR"
  echo "   El esfuerzo no justifica el beneficio."
fi

echo ""
echo "Fórmula: Frecuencia($FREQ) + Tiempo($TIME) + Impacto($IMPACT) + Complejidad($COMPLEX) = $TOTAL"
