# OpenRouter — Precio Efectivo Real para OpenClaw

**Fecha:** 2026-08-09 · **Fuente:** API `openrouter.ai/api/v1/models` (236 modelos con `input_cache_read` definido) + datos reales de pantallas Effective Pricing de OpenRouter.

---

## Metodología

Para cada modelo con `input_cache_read > 0` se calculó el **costo efectivo real por turno de OpenClaw**:

```
Hit rate REAL medido (pantallas Effective Pricing):
  xiaomi/mimo-v2.5        → 94.2% (provider propio Xiaomi)
  nex-agi/nex-n2-mini     → 33.8% (NexAGI)
  qwen/qwen3.7-flash      → 50.2% (Alibaba Cloud)
  resto third-party       → 55% (default prudente)

effective_input = (hit_rate × cache_read) + ((1−hit_rate) × prompt_price)

Asunción carga OpenClaw: 90% de los 20k tokens de input son cacheados (system prompt + contexto reutilizado)
Costo/turno  = (0.9 × cache_read + 0.1 × prompt) × 20,000 + completion × 1,000
Costo/mes    = costo/turno × 3,000 turnos
```

El input domina el costo (output de OpenClaw es ~5% del uso). El **cache hit rate es el factor decisivo**, no el precio listado.

---

## 📢 Hallazgo 1 — Los modelos GRATIS son los más baratos (obvio pero importante)

Hay **14 modelos `:free` en OpenRouter**, todos a $0.00 sin `input_cache_read` definido (por eso no salen en el query filtrado por cache, pero son reales):

| Modelo | Contexto |
|---|---|
| `nvidia/nemotron-3-ultra-550b-a55b:free` | 1,000,000 |
| `nvidia/nemotron-3-super-120b-a12b:free` | 262,144 |
| `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free` | 256,000 |
| `nvidia/nemotron-3-nano-30b-a3b:free` | 256,000 |
| `google/gemma-4-31b-it:free` | 262,144 |
| `google/gemma-4-26b-a4b-it:free` | 262,144 |
| `inclusionai/ling-3.0-tiny:free` | 262,144 |
| `poolside/laguna-s-2.1:free` | 262,144 |
| `poolside/laguna-xs-2.1:free` | 262,144 |
| `openai/gpt-oss-20b:free` | 131,072 |
| `cohere/north-mini-code:free` | 256,000 |
| `nvidia/nemotron-nano-12b-v2-vl:free` | 128,000 |
| `nvidia/nemotron-nano-9b-v2:free` | 128,000 |
| `nvidia/nemotron-3.5-content-safety:free` | 128,000 |

**Recomendación:** `nvidia/nemotron-3-ultra-550b-a55b:free` (la "nemotron-ultra:free") es el mejor gratis: 550B params, 1M de contexto, tool calling, $0.00/M. Aparte, restricción de rate-limit en free (sin garantía de disponibilidad).

---

## 🏆 Hallazgo 2 — Top 10 modelos PAGO más baratos por costo efectivo/turno

Filtrado: contexto ≥ 128k + tool calling soportado.

| # | Modelo | Ctx | Cache | Prompt | Hit | Costo/turno | Costo/mes (3k) |
|---|---|---|---|---|---|---|---|
| 1 | `inclusionai/ling-2.6-flash` | 262k | $0.002 | $0.010 | 55% | **$0.086 m** | **$0.26** |
| 2 | `inclusionai/ling-3.0-flash` | 262k | $0.0042 | $0.021 | 55% | $0.181 m | $0.54 |
| 3 | `nex-agi/nex-n2-mini` | 262k | $0.0025 | $0.025 | 33.8% | $0.195 m | $0.58 |
| 4 | `openai/gpt-5-nano:batch` | 400k | $0.0025 | $0.025 | 55% | $0.295 m | $0.89 |
| 5 | `qwen/qwen3.7-flash` | 1,000k | $0.006 | $0.030 | 50.2% | $0.298 m | $0.89 |
| 6 | `mistralai/ministral-3b-2512` | 131k | $0.010 | $0.100 | 55% | $0.480 m | $1.44 |
| 7 | `google/gemini-2.5-flash-lite:batch` | 1,048k | $0.010 | $0.050 | 55% | $0.480 m | $1.44 |
| 8 | `poolside/laguna-s-2.1` | 1,048k | $0.009 | $0.090 | 55% | $0.522 m | $1.57 |
| 9 | `openai/gpt-4.1-nano:batch` | 1,048k | $0.0125 | $0.050 | 55% | $0.525 m | $1.57 |
| 10 | `openai/gpt-5-nano` | 400k | $0.005 | $0.050 | 55% | $0.590 m | $1.77 |

**Sigue mimo-v2.5 en puesto 12** — $0.610 m/turno, $1.83/mes (detalle en sección de verificación).

---

## ✅ Hallazgo 3 — Verificación de mimo-v2.5, nex-n2-mini y qwen3.7-flash

Cargamos los precios REALES de la API y los cruzamos con los hit-rate REALES medidos en las pantallas:

### `xiaomi/mimo-v2.5` (proveedor propio Xiaomi)
```
API:  cache_read=$0.0028/M  prompt=$0.14/M  completion=$0.28/M
Hit:  94.2% (medido real)

effective_input = (0.942×0.0028) + (0.058×0.14) = $0.0108/M
Costo/turno = $0.610 m  →  $1.83/mes
```
> ✅ CONFIMADO vs pantalla real ($0.0113/M). Nuestro $0.0108/M es casi idéntico.
> **En el top pero NO el #1.** Su fuerte es el input cacheado (casi gratis a $0.0028/M), pero el prompt base es caro ($0.14/M), así que mis 2k tokens nuevos de cada turno cuestan. Solo gana si el hit es consistentemente >94% y la carga es 90%+ cacheada. Con mi modelo (deepseek) actual es una alternativa sólida y barata.

### `nex-agi/nex-n2-mini` (NexAGI)
```
API:  cache_read=$0.0025/M  prompt=$0.025/M  completion=$0.10/M
Hit:  33.8% (medido real)

effective_input = (0.338×0.0025) + (0.662×0.025) = $0.0174/M
Costo/turno = $0.195 m  →  $0.58/mes
```
> ✅ CONFIMADO (pantalla: $0.01732/M). Está en el **puesto 3** del top. Excelente relación precio/rendimiento.
> Aunque su hit real es bajo (33.8%), su prompt es tan barato ($0.025/M) que el costo efectivo sigue siendo bajísimo.

### `qwen/qwen3.7-flash` (Alibaba Cloud)
```
API:  cache_read=$0.006/M  prompt=$0.03/M  completion=$0.13/M
Hit:  50.2% (medido real)

effective_input = (0.502×0.006) + (0.498×0.03) = $0.018/M
Costo/turno = $0.298 m  →  $0.89/mes
```
> ⚠️ La API reporta $0.018/M, la pantalla citada decía $0.041/M. La diferencia viene del **tier por volumen** de Alibaba (los `overrides` suben precio con más tokens de prompt: $0.10, $0.20, $0.40 por tramos de 32k/256k). Para single-turno corto de OpenClaw aplica el tramo bajo = $0.018/M. Aun con el tramo alto, sigue siendo barato. **Puesto 5** del top.

---

## 🧮 Hallazgo 4 — El cache hit rate REAL es el factor decisivo

Comparación de que el **precio listado engaña**:

| Modelo | Prompt listado | Nuestro costo/turno | Ranking |
|---|---|---|---|
| inclusionai/ling-2.6-flash | $0.010 | $0.086 m | 1 |
| mim-v2.5 | $0.14 (caro!) | $0.610 m | 12 |
| openai/gpt-4o-mini | $0.075 | $1.125 m | 33+ |

`mimo-v2.5` **parece caro** por su prompt de $0.14/M pero su cache ultra-barata ($0.0028/M) + hit de 94% lo hunde al rango de los más económicos. Al revés, modelos con prompt barato pero **sin cache_read definido** (como gpt-4o-mini) terminan costando el doble que mimo. **Siempre mirar cache_read, no el list price.**

---

## 🎯 Recomendación final para OpenClaw

1. **Mejor opción costo cero:** `nvidia/nemotron-3-ultra-550b-a55b:free` — 1M contexto, 550B, tool calling, pero sujeto a rate limits y disponibilidad de free.
2. **Mejor opción paga ultra-económica:** `inclusionai/ling-2.6-flash` — $0.26/mes (asumiendo 3k turnos). Alternativa: `ling-3.0-flash` ($0.54/mes).
3. **Confirmados baratos con dato real:** `nex-agi/nex-n2-mini` ($0.58/mes) y `qwen/qwen3.7-flash` ($0.89/mes).
4. **mimo-v2.5** es una apuesta sólida ($1.83/mes) para cargas con hit muy alto y >90% contexto cacheado — el perfil típico de un agente con system prompt pesado.
5. **Evitar** modelos con prompt alto y cache_read bajo/ausente (gpt-4o, claude-opus, etc.) salvo que la calidad lo justifique: el input domina el costo.

> ⚠️ Nota: modelos `:batch` y `:free` tienen latencia/rate-limit distintos; para OpenClaw en tiempo real, los no-batch no-free de arriba son los más fiables. Las free no tienen `input_cache_read` (la API no reporta cache en `:free`), así que su costo real es $0 directo.
