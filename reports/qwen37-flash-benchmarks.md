# Benchmarks de rendimiento — Qwen 3.7 Flash (Alibaba)

**Fecha de investigación:** 17–18 de agosto de 2026
**Modelo:** `qwen3.7-flash` (versión API `qwen3.7-flash-20260727`), multimodal vision-language de Alibaba.

---

## ⚠️ Hallazgo principal (leer primero)

**No existen benchmarks públicos verificables de Qwen 3.7 Flash en ninguna fuente independiente consultada hoy.** El modelo es **propietario / solo-API** (no open-weights) y **ningún leaderboard independiente lo ha evaluado todavía**.

Esto se confirmó por 5 vías independientes (todas consultadas hoy):

| Fuente | Resultado | Evidencia |
|---|---|---|
| **Artificial Analysis** | ❌ NO listado | `qwen3.7-flash` = **0 ocurrencias** en toda la página `/models` (1.3 MB, consultada hoy). Solo aparecen Qwen3.7 Plus y Qwen3.7 Max. |
| **LMArena / Arena.ai** | ❌ NO listado | `qwen3.7-flash` = **0 ocurrencias** en la página del leaderboard (5.2 MB, consultada hoy). Solo aparecen `qwen3.7-plus`, `qwen3.7-plus-preview`, `qwen3.7-max`, `qwen3.7-max-preview`. |
| **OpenRouter API** | ❌ Sin benchmarks | El objeto del modelo `qwen/qwen3.7-flash` **NO tiene campo `benchmarks`** (ni `artificial_analysis` ni `design_arena`). En contraste, Gemini 3.7 Flash sí lo tiene. Latencia y throughput = `null`. |
| **Hugging Face** | ❌ No existe | Búsqueda `qwen3.7-flash` en HF API = **0 resultados**. Búsqueda `Qwen3.7` = solo un modelo de terceros no relacionado (`RscriptSQwen/Qwen3.7-plus`). |
| **GitHub QwenLM** | ❌ No hay repo | La org QwenLM tiene repos de Qwen3, Qwen3.8, Qwen3-VL, Qwen3-Coder, etc., pero **NO existe repo de Qwen3.7**. El README oficial de Qwen3 solo cubre Qwen3-2504/2507 (2025). |

**Conclusión sobre el estado:** Qwen3.7 Flash es un modelo **propietario** (no liberado como open-weights), lanzado como API muy recientemente (versión `20260727` = 27 de julio de 2026). Ningún evaluador independiente (Artificial Analysis, LMArena, OpenCompass) lo ha incorporado aún a sus leaderboards. **No hay números de IQ, coding, agentic, velocidad, latencia ni contexto efectivo medidos por terceros.**

---

## Tabla de benchmarks

| Métrica | Valor | Fuente | Fecha |
|---|---|---|---|
| Índice de inteligencia (IQ) de Artificial Analysis | **NO DISPONIBLE** — modelo no evaluado | artificialanalysis.ai/models (0 ocurrencias de qwen3.7-flash) | 2026-08-17 |
| Coding score (HumanEval/LiveCodeBench/SWE-bench) | **NO DISPONIBLE** | idem | 2026-08-17 |
| Agentic score | **NO DISPONIBLE** | idem | 2026-08-17 |
| Velocidad (tokens/seg) | **NO DISPONIBLE** — OpenRouter reporta `null` | openrouter.ai/api/v1/models/qwen/qwen3.7-flash-20260727/endpoints | 2026-08-17 |
| Latencia (TTFT) | **NO DISPONIBLE** — OpenRouter reporta `null` | idem | 2026-08-17 |
| Contexto efectivo | **1,000,000 tokens** (especificación, no medido) | OpenRouter API; Alibaba Cloud Model Studio | 2026-08-17 |
| Max salida | **65,536 tokens** | OpenRouter API | 2026-08-17 |
| Benchmarks oficiales de Alibaba (MMLU/GPQA/MATH) | **NO PUBLICADOS** para Qwen3.7 Flash | Blog de Qwen (qwen.ai) es SPA no accesible; sin model card en HF/GitHub | 2026-08-17 |

---

## Datos de referencia del contexto (familia Qwen3.7 — NO son de Flash)

Para situar el perfil, esto es lo que sí está medido en la familia Qwen3.7 (Plus/Max), que Flash **no comparte necesariamente**:

- **Artificial Analysis** (página `/models`, 2026-08-17):
  - `Qwen3.7 Plus` — en catálogo, `isReasoning: true`, release 2026-06-01. IQ no mostrado en el bloque top-11 (está por debajo del top).
  - `Qwen3.7 Max` — en catálogo, `isReasoning: true`, release 2026-05-19, **marcado `deprecated: true`**.
  - Referencia Qwen en el top de IQ: **Qwen3.8 Max IQ = 58.08**, **Qwen3.8 27B IQ = 52.02** (los modelos Qwen más recientes sí evaluados).
- **LMArena** (leaderboard, 2026-08-17): `qwen3.7-plus` rank **48** global / **25** en chat.

> ⚠️ Estos números son de Qwen3.7 Plus/Max y Qwen3.8 — **no** son de Qwen3.7 Flash. No deben usarse como si fueran del Flash.

---

## Nota sobre contradicciones / discrepancias

1. **Alibaba Cloud Model Studio** (docs oficiales, consultado hoy) lista `qwen3.7-flash` como **model ID existente** (con base URLs en Beijing, Singapur, Tokio, Frankfurt, US-Virginia), pero la página de "modelos de visión recomendados" **NO lo incluye** — solo recomienda `qwen3.7-plus` (flagship) y `qwen3.6-flash` (opción económica). Esto sugiere que **qwen3.7-flash es una adición muy reciente** (versión 2026-07-27) aún no documentada en las guías de recomendación.

2. **OpenRouter vs. catálogo Alibaba:** OpenRouter lo sirve como `qwen/qwen3.7-flash-20260727` servido por "Alibaba" (uptime 99.99% en 24h), confirmando que es un modelo real y activo. La ausencia en leaderboards independientes es por **novedad**, no por inexistencia.

3. **Blog oficial de Qwen (qwen.ai):** es una SPA renderizada por JavaScript; el contenido (donde Alibaba publicaría benchmarks oficiales) **no es accesible** vía fetch estático ni vía Wayback Machine (solo se archiva el shell JS). No pude extraer los números oficiales de Alibaba de la publicación de Qwen3.7.

---

## Qué se confirmó vs. qué sigue pendiente

**Confirmado hoy:**
- ✅ Qwen3.7 Flash es **propietario / solo-API** (no open-weights).
- ✅ **No está evaluado** por Artificial Analysis, LMArena, ni aparece en OpenRouter con datos de benchmarks.
- ✅ Specs de API verificadas: contexto 1M, max salida 65,536, multimodal texto+imagen+video→texto, razonamiento opcional.
- ✅ El modelo existe y está activo (servido por Alibaba vía OpenRouter, uptime alto).

**Pendiente (no encontrado):**
- ❌ Cualquier número de IQ, coding, agentic, velocidad, latencia o contexto efectivo medido.
- ❌ Benchmarks oficiales de Alibaba (MMLU, GPQA, MATH, etc.) — el blog de Qwen es inaccesible a scraping estático.
- ❌ Elo en LMArena / posición en OpenCompass / LiveBench / SWE-bench.

---

## Perfil de rendimiento real de Qwen 3.7 Flash

**No se puede establecer un perfil de rendimiento cuantitativo** porque no hay datos publicados. Lo que se sabe con certeza (por especificación y posicionamiento del fabricante):

- Es la variante **"Flash"** (rápida/eficiente) de la familia Qwen3.7, orientada a **agentes multimodales, coding visual, búsqueda e interacción por computadora** (descripción oficial en OpenRouter).
- **Precio muy bajo** (input $0.03/M, output $0.13/M en OpenRouter) → perfil **económico / alta velocidad**, consistente con el rol "Flash" frente al "Plus"/"Max" flagship.
- **Contexto 1M tokens** y **max salida 65,536** → capaz de tareas de contexto largo y salidas extensas.
- Es un **reasoning model** (razonamiento opcional, activado por defecto).

**Recomendación de uso:** hasta que Artificial Analysis / LMArena / Alibaba publiquen números, tratar a Qwen3.7 Flash como un modelo **económico multimodal de propósito general** sin datos de rendimiento verificados. Para decisiones que dependan de benchmarks (código, agentes), **no hay evidencia independiente** que respalde una comparación cuantitativa con alternativas. Revisitar en 2–4 semanas cuando los leaderboards probablemente lo incorporen.

---

## Fuentes consultadas (todas el 17–18 ago 2026)

- https://openrouter.ai/api/v1/models (y `/models/qwen/qwen3.7-flash-20260727/endpoints`) — specs + ausencia de benchmarks
- https://artificialanalysis.ai/models — ausencia de qwen3.7-flash
- https://lmarena.ai/leaderboard (→ arena.ai) — ausencia de qwen3.7-flash
- https://huggingface.co/api/models?search=qwen3.7-flash — 0 resultados
- https://api.github.com/orgs/QwenLM/repos — sin repo Qwen3.7
- https://raw.githubusercontent.com/QwenLM/Qwen3/main/README.md — sin contenido Qwen3.7
- https://www.alibabacloud.com/help/en/model-studio/models y `/vision-model/` — catálogo Alibaba, qwen3.7-flash como model ID pero no en recomendados
- https://www.alibabacloud.com/help/en/model-studio/models (log) — qwen3.7-max/plus/3.6-flash listados
