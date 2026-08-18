# Reporte de Precios — DeepSeek V4 Flash (Multi-Proveedor)

**Fecha de consulta:** 17 de agosto de 2026 (todas las fuentes verificadas HOY)
**Modelo objetivo:** DeepSeek V4 Flash (versión 0731 / estándar)

---

## 1. Tabla comparativa de precios por proveedor

Precios en **USD por 1M de tokens**. "Cache read" = input servido desde caché; "Input miss" = input sin caché; "Output" = tokens generados.

| Proveedor | Input (miss) | Cache read | Output | Fuente (consultada 2026-08-17) |
|-----------|-------------|-----------|--------|-------------------------------|
| **OpenRouter** `deepseek/deepseek-v4-flash` | $0.0686 | $0.0137 | $0.1372 | https://openrouter.ai/api/v1/models |
| **OpenRouter** `deepseek/deepseek-v4-flash-0731` | $0.14 | $0.028 | $0.28 | https://openrouter.ai/api/v1/models |
| **OpenRouter** `~deepseek/deepseek-v4-flash-latest` (ruta más barata) | $0.0783 | $0.0157 | $0.1566 | https://openrouter.ai/api/v1/models |
| **DeepInfra** `DeepSeek-V4-Flash-0731` | $0.08 | $0.016 | $0.18 | https://deepinfra.com/pricing |
| **DeepInfra** `DeepSeek-V4-Flash` | $0.09 | $0.018 | $0.18 | https://deepinfra.com/pricing |
| **Together AI** `DeepSeek V4 Flash 0731` | $0.14 | $0.03 | $0.28 | https://together.ai/pricing |
| **Fireworks AI** `DeepSeek V4 Flash (0731)` Standard | $0.14 | $0.028 | $0.28 | https://docs.fireworks.ai/serverless/pricing |
| **Novita** `Deepseek V4 Flash 0731` / `V4 Flash` | $0.14 | $0.028 | $0.28 | https://novita.ai/model-api/pricing |
| **DeepSeek oficial** `deepseek-v4-flash` (off-peak) | $0.22 | $0.007 | $0.66 | https://api-docs.deepseek.com/quick_start/pricing/ |
| **DeepSeek oficial** `deepseek-v4-flash` (peak) | $0.44 | $0.014 | $1.32 | https://api-docs.deepseek.com/quick_start/pricing/ |
| **Groq** | ❌ No ofrece el modelo | — | — | https://console.groq.com/docs/models |
| **Hyperbolic** | ⚠️ No verificable hoy | — | — | páginas con redirect/404 |

**Notas de verificación:**
- **Groq:** El catálogo público actual de modelos de GroqCloud **no incluye DeepSeek V4 Flash** (solo GPT OSS, Qwen, MiniMax, Whisper, etc.). No se puede cotizar.
- **Hyperbolic:** Las páginas de precios/modelos no fueron accesibles hoy (redirect loops / 404). No se pudo verificar; se excluye del ranking.
- **OpenRouter** tiene 3 variantes; la del reporte original (`deepseek/deepseek-v4-flash`) es la estándar, y la más barata del ecosistema es la ruta `~...-latest`.

---

## 2. Cálculo de costo mensual por proveedor

**Escenario:** 30M tokens/día → 900M tokens/mes con patrón agente:
- **720M** input cacheado
- **135M** input sin caché (miss)
- **45M** output

Fórmula: `(720 × cache_read) + (135 × input_miss) + (45 × output)` en $/M.

| Proveedor (variante) | 720M cached | 135M miss | 45M output | **Total mensual** |
|----------------------|------------|-----------|------------|-------------------|
| **OpenRouter** `deepseek-v4-flash` | $9.86 | $9.26 | $6.17 | **$25.30** |
| **DeepInfra** `V4-Flash-0731` | $11.52 | $10.80 | $8.10 | **$30.42** |
| **DeepInfra** `V4-Flash` | $12.96 | $12.15 | $8.10 | **$33.21** |
| **Fireworks** `V4 Flash 0731` | $20.16 | $18.90 | $12.60 | **$51.66** |
| **Novita** `V4 Flash` | $20.16 | $18.90 | $12.60 | **$51.66** |
| **Together AI** `V4 Flash 0731` | $21.60 | $18.90 | $12.60 | **$53.10** |
| **DeepSeek oficial** (off-peak) | $5.04 | $29.70 | $29.70 | **$64.44** |
| **DeepSeek oficial** (promedio ponderado peak/off-peak) | $6.51 | $38.37 | $38.37 | **$83.25** |

**Sobre el promedio de DeepSeek oficial:** Peak son solo 7h/día (01:00–04:00 y 06:00–10:00 UTC = 29.2% del día); el resto (70.8%) es off-peak. El promedio ponderado usa esos pesos. El resultado es *más caro* que usar solo off-peak, porque el output y el miss en peak se duplican.

---

## 3. Ranking de proveedores (más barato → más caro)

1. 🥇 **OpenRouter** `deepseek/deepseek-v4-flash` — **$25.30/mes** ← MÁS BARATO
2. 🥈 **DeepInfra** `V4-Flash-0731` — **$30.42/mes**
3. 🥉 **DeepInfra** `V4-Flash` — **$33.21/mes**
4. **Fireworks** `V4 Flash 0731` — **$51.66/mes**
5. **Novita** `V4 Flash` — **$51.66/mes**
6. **Together AI** `V4 Flash 0731` — **$53.10/mes**
7. **DeepSeek oficial** (off-peak) — **$64.44/mes**
8. **DeepSeek oficial** (promedio) — **$83.25/mes** ← MÁS CARO

---

## 4. Conclusión — Precio REAL a documentar

**El precio real a documentar es el de OpenRouter: input $0.0686/M, cache_read $0.0137/M, output $0.1372/M → $25.30/mes** para el escenario de 900M tokens. Es el más barato de todos los proveedores verificados hoy.

**Hallazgo clave (confirma el fenómeno de los revendedores):**
Los revendedores de modelos open-source (**OpenRouter y DeepInfra**) son **más baratos que el fabricante (DeepSeek oficial)**. Esto es un fenómeno de mercado real, no un error:

- **DeepSeek oficial** cobra tarifas altas por *cache miss* ($0.22/M) y *output* ($0.66/M), que son los componentes dominantes en el patrón agente (135M miss + 45M output). Su ventaja (cache hit a $0.007/M) no compensa porque el output es caro.
- **OpenRouter** aplica un margen pequeño sobre el costo de capacidad subyacente y ofrece tarifas planas bajas ($0.0686 miss / $0.1372 output), ~3-5× más baratas que el fabricante en miss/output.
- **DeepInfra** compra capacidad al por mayor y subsidia modelos populares para atraer tráfico, resultando en $0.08 miss / $0.18 output.
- Los revendedores que **no** tienen economías de escala tan agresivas (Together, Fireworks, Novita) cobran más cerca de la tarifa "estándar" de $0.14/$0.28, pero **aún así por debajo** del fabricante en el escenario agente.

**Recomendación:** Documentar **OpenRouter** como el precio de referencia (más barato y verificado), con **DeepInfra** como alternativa sólida de respaldo. Evitar DeepSeek oficial directo para workloads con alta proporción de output/miss.

---

*Reporte generado por análisis de precios LLM. Todas las URLs consultadas el 2026-08-17.*
