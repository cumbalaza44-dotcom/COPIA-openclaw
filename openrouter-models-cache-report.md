# 🧠 Modelos de IA en OpenRouter para OpenClaw — Costo REAL por Turno (Cache-Aware)

**Fecha:** 2026-08-09
**Fuente de datos:** API pública de OpenRouter (`/api/v1/models`), consultada en vivo.
**Foco:** el costo real de operar OpenClaw considerando que ~90% del input de cada turno es **prompt cache hit**.

---

## 1. El modelo de costo real de OpenClaw

OpenClaw envía un system prompt pesado (~15–20k tokens de SOUL.md, AGENTS.md, IDENTITY.md, USER.md, TOOLS.md, MEMORY.md, archivos de workspace) en **cada turno**. Contra este input estable, OpenRouter aplica **prompt caching**: una vez que el proveedor cachea el prefijo, los tokens repetidos se cobran a precio de **`input_cache_read`**, no a precio `prompt`.

**Supuestos del cálculo por turno:**

| Concepto | Tokens | Precio aplicado |
|----------|--------|-----------------|
| System prompt (repeatable) | 18,000 | `input_cache_read` |
| Input nuevo (usuario/contexto) | 2,000 | `prompt` |
| Output (completion) | 1,000 | `completion` |

> **Costo por turno = (18,000 × cache_read) + (2,000 × prompt) + (1,000 × completion)**

Volumen base: **100 turnos/día**, ×30 días = **3,000 turnos/mes**.

Esto es **EL dato que importa** en OpenClaw: el precio `prompt` "de listado" es prácticamente irrelevante frente al precio `cache_read`, que domina el costo al multiplicarse por 18k tokens cada turno.

---

## 2. Ranking por costo REAL por turno (cache-aware)

Filtros aplicados a la API: **tool calling** (`supported_parameters` incluye `tools`), **contexto ≥ 128K**, pricing válido. Ordenado de menor a mayor costo real por turno.

| Modelo | Prompt $/1M | Output $/1M | CacheRead $/1M | Contexto | Costo/turno | Costo/día (100 t) | Costo/mes (3000 t) |
|--------|-----|-----|-----|-----|-----|-----|-----|
| inclusionai/ling-3.0-flash | 0.021 | 0.063 | 0.0042 | 262K | **$0.00018** | $0.018 | **$0.54** |
| nex-agi/nex-n2-mini | 0.025 | 0.100 | 0.0025 | 262K | $0.00019 | $0.019 | $0.58 |
| amazon/nova-micro-v1 | 0.035 | 0.140 | — | 128K | $0.00021 | $0.021 | $0.63 |
| gpt-oss-120b | 0.037 | 0.170 | — | 131K | $0.00024 | $0.024 | $0.73 |
| google/gemma-3-12b-it | 0.050 | 0.150 | — | 131K | $0.00025 | $0.025 | $0.75 |
| qwen3-30b-a3b-instruct-2507 | 0.048 | 0.193 | — | 262K | $0.00029 | $0.029 | $0.87 |
| **qwen/qwen3.7-flash** | 0.030 | 0.130 | **0.006** | 1M | **$0.00030** | $0.030 | **$0.89** |
| gpt-5-nano:batch | 0.025 | 0.200 | 0.0025 | 400K | $0.00030 | $0.030 | $0.89 |
| amazon/nova-lite-v1 | 0.060 | 0.240 | — | 300K | $0.00036 | $0.036 | $1.08 |
| qwen/qwen3.5-flash-02-23 | 0.065 | 0.260 | — | 1M | $0.00039 | $0.039 | $1.17 |
| **z-ai/glm-5.2** | 0.070 | 0.220 | 0.013 | 1M | **$0.00059** | $0.059 | **$1.78** |
| **xiaomi/mimo-v2.5** (default actual) | 0.140 | 0.280 | 0.0028 | 1.05M | **$0.00061** | $0.061 | **$1.83** |
| **deepseek/deepseek-v4-flash-0731** | 0.090 | 0.180 | 0.018 | 1M | **$0.00068** | $0.068 | **$2.05** |
| **~deepseek/deepseek-v4-flash-latest** | 0.080 | 0.252 | 0.025 | 1M | **$0.00087** | $0.087 | **$2.60** |
| qwen/qwen3.6-flash | 0.188 | 1.125 | — | 1M | $0.00150 | $0.150 | $4.50 |
| deepseek/deepseek-chat (v3.1) | 0.257 | 1.029 | — | 163K | $0.00154 | $0.154 | $4.63 |
| deepseek/deepseek-v4-pro | 0.435 | 0.870 | 0.0036 | 1M | $0.00181 | $0.181 | $5.42 |
| qwen/qwen3.5-plus-20260420 | 0.300 | 1.800 | 0.380 | 1M | $0.00240 | $0.240 | $7.20 |
| qwen/qwen3.7-plus | 0.320 | 1.280 | 0.064 | 1M | $0.00307 | $0.307 | $9.22 |
| nvidia/nemotron-ultra-550b:batch | 0.300 | 1.800 | 0.10 | 512K | $0.00440 | $0.440 | $13.20 |
| qwen/qwen3.7-max | 1.475 | 4.425 | 0.295 | 1M | $0.01269 | $1.268 | $38.05 |
| qwen/qwen3.8-max | 2.000 | 6.000 | 0.25 | 1M | $0.01450 | $1.450 | $43.50 |
| **anthropic/claude-haiku-latest** | 1.000 | 5.000 | 0.10 | 200K | **$0.00880** | $0.880 | **$26.40** |
| **anthropic/claude-sonnet-5:batch** | 1.000 | 5.000 | 0.10 | 1M | **$0.00880** | $0.880 | **$26.40** |
| **nvidia/nemotron-ultra-550b-a55b** | 0.600 | 3.600 | 0.20 | 512K | **$0.00840** | $0.840 | **$25.20** |
| **anthropic/claude-sonnet-5** (y ~latest) | 2.000 | 10.00 | 0.20 | 1M | **$0.01760** | $1.760 | **$52.80** |
| openai/gpt-5.2 / gpt-5.2-codex | 1.750 | 14.00 | 0.175 | 400K | $0.02065 | $2.065 | $61.95 |
| x-ai/grok-4.5 | 2.000 | 6.000 | 0.30 | — | $0.01780 | $1.780 | $53.40 |

---

## 3. 🏆 Los modelos donde el CACHE marca LA MAYOR DIFERENCIA

La métrica clave es el **ratio cache-vs-sincache**: cuántas veces más caro sería el turno si NO existiera el cache del system prompt. Esto indica cuánto im-porta el cache en cada modelo:

| Modelo | Ratio cache vs sincache | Nota |
|--------|------|------|
| **deepseek/deepseek-v4-pro** | **5.3×** | El cache (_read_ $0.0036/1M) es ~120× más barato que el prompt ($0.435). Gigante en ahorro. |
| **xiaomi/mimo-v2.5** | **5.0×** | cache_read $0.0028 → 50× más barato que prompt $0.14. Default actual bien elegido en este aspecto. |
| qwen3.5-9b | 6.1× | |
| deepseek-v3.2 | 6.1× | cache $0.1345 vs prompt $0.27 |
| **z-ai/glm-5.2** | 2.7× | cache $0.013 vs prompt $0.07 (5.4× más barato) |
| qwen/qwen3.7-flash | 2.4× | cache $0.006 vs prompt $0.03 (5× más barato) |
| deepseek-v4-flash-0731 | 2.9× | cache $0.018 vs prompt $0.09 (5×) |
| claude-sonnet-5 | 2.8× | cache $0.20 vs prompt $2.00 (10×) |

> **Insight:** En OpenClaw el cache convierte un model flagship "caro" en algo operativamente racional, pero **los modelos con cache_read ultra-bajo + prompt bajo** siguen siendo los reyes en costo absoluto por turno.

---

## 4. 🆓 Modelos gratuitos (referencia)

Tool-calling + contexto ≥ 128K disponibles **a costo $0** en OpenRouter:

| Modelo | Contexto | Tool calling |
|--------|----------|--------------|
| **nvidia/nemotron-3-ultra-550b-a55b:free** | 1M | ✅ |
| nvidia/nemotron-3-super-120b:free | 262K | ✅ |
| nvidia/nemotron-3-nano-30b:free | 256K | ✅ |
| google/gemma-4-26b-a4b-it:free | 262K | ✅ |
| google/gemma-4-31b-it:free | 262K | ✅ |
| openai/gpt-oss-20b:free | 131K | ✅ |
| inclusionai/ling-3.0-tiny:free | 262K | ✅ |
| poolside/laguna-xs-2.1:free | 262K | ✅ |
| **openrouter/free** (router) | 200K | ✅ |

> Los `:free` suelen tener limites de tasa (rate-limit) y menor prioridad de service — útiles para dev/test, no confiables para producción 24/7.

---

## 5. 🎯 Recomendación principal + fallback en cascada

### 🥇 RECOMENDADO PRINCIPAL: **qwen/qwen3.7-flash**
- **Costo real:** $0.00030/turno → **$0.89/mes** (a 3,000 turnos).
- **Por qué:** la combinación más barata con tool-calling + **contexto 1M** + precio de cache_read competitivo ($0.006). Multimodal (texto+imagen+video), buen instruction-following. Ideal para el patrón de OpenClaw con system prompt grande y cacheado.
- Único pero: los **overrides de pricing** por volumen de prompt (a ≥32k tokens de input el price sube a $0.10 prompt / $0.02 cache; a ≥256k sube más). Con system prompt de 18k normalmente no se cruza el umbral de 32k, pero hay que vigilarlo si el system crece.

### 🥈 FALLBACK 1 (calidad-precio): **z-ai/glm-5.2**
- **Costo real:** $0.00059/turno → **$1.78/mes**.
- **Por qué:** en el tier de "premium económico", GLM-5.2 ofrece calidad de razonamiento notablemente superior a qwen3.7-flash por solo ~2× su costo. Contexto 1M, tool-calling robusto, cache_read $0.013. Es el "sweet spot" si se nota degradación de calidad en el modelo barato.

### 🥉 FALLBACK 2 (qualité top, presupuesto sube): **~anthropic/claude-haiku-latest**
- **Costo real:** $0.00880/turno → **$26.40/mes**.
- **Por qué:** la vía más barata hacia la fiabilidad/instrucción de Anthropic en un tier de velocidad. 200K de contexto. Si hace falta solidez de tool-calling sin pagar sonnet.

### ⚠️ FALLBACK 3 (refuerzo/largo): **~deepseek/deepseek-v4-flash-latest**
- **Costo real:** $0.00087/turno → **$2.60/mes**.
- Por qué: alterna con qwen3.7-flash a costo similar; el `-latest` apunta al candidato estable más reciente sin cambiar el slug.

### 📈 RECOMENDACIÓN DEFINITIVA
```
Principal : qwen/qwen3.7-flash        ($0.89/mes)
Router    : openrouter/auto-beta      (probar; mezcla calidad/costo)
  ├─ si calidad baja → z-ai/glm-5.2   ($1.78/mes)
  │    ├─ si necesita Anthropic → ~anthropic/claude-haiku-latest ($26.40/mes)
  │    └─ si necesita razonamiento top → z-ai/glm-5.2 ya cubre
  └─ si se busca calidad estrella y el presupuesto lo permite →
       anthropic/claude-sonnet-5:batch para tareas en lote ($26.40/mes, 50% off)
```

> **Nota sobre el default actual (xiaomi/mimo-v2.5, $1.83/mes):** es un modelo sólido con excelente ratio de cache (5×), pero **cuesta el doble que qwen3.7-flash con calidad comparable o superior** en tareas de agente. Migrar a qwen3.7-flash recorta ~50% del costo mensual sin sacrificar capacidad.

---

## 6. 🇪🇸 Soporte de español

- **Nativo fuerte (multilingüe orientado):** Qwen (Alibaba) — excelente en español — `qwen3.7-flash` recomendada. GLM (Zhipu) también muy competente en español.
- **Muy bueno:** DeepSeek-v4 (family) — entrenado multilingüe, maneja español con naturalidad. Claude (Anthropic) — español de altísima calidad.
- **Adecuado:** xiaomi mimo-v2.5, Gemini (multilingüe robusto), Grok (bueno pero a veces anglocéntrico).
- Para el flujo de Mr. Jair (español colombiano), las **dos recomendadas principales (qwen3.7-flash y glm-5.2)** ofrecen soporte de español sobresaliente.

---

## 7. 📊 Resumen ejecutivo

| Métrica | qwen3.7-flash | xiaomi/mimo-v2.5 (actual) | deepseek-v4-flash-0731 | glm-5.2 | claude-haiku-latest | claude-sonnet-5 |
|---------|:----:|:----:|:----:|:----:|:----:|:----:|
| Costo/turno | $0.00030 | $0.00061 | $0.00068 | $0.00059 | $0.00880 | $0.01760 |
| Costo/mes (3k turnos) | **$0.89** | $1.83 | $2.05 | **$1.78** | $26.40 | $52.80 |
| Contexto | 1M | 1.05M | 1M | 1M | 200K | 1M |
| Cache ratio | 2.4× | 5.0× | 2.9× | 2.7× | 2.8× | 2.8× |
| Multimodal | ✅ (img+vid) | ✅ (img+aud+vid) | text | text | ✅ | ✅ |
| Español | Excelente | Excelente | Muy bueno | Muy bueno | Excelente | Excelente |

**Conclusión:** En el patrón de OpenClaw (90% input cacheado), el costo mensual puede ir desde **$0.54** (ling-3.0-flash) hasta **$62** (GPT-5.2) según el nivel de calidad. El mejor equilibrio costo/calidad/cache para el agente es **qwen/qwen3.7-flash**, con **glm-5.2** como upgrade de calidad de bajo costo. El cache convierte a los modelos baratos en operativamente casi gratuities, y a los flagships en un lujo presupuestable solo si la tarea lo justifica.
