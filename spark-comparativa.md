# Comparativa: Muse Spark 1.2 Contributor vs 1.3 Contributor (OpenRouter)

> Fuente: `https://openrouter.ai/api/v1/models` — consulta directa 2026-09-05. Precios en USD.

## 1. Precios y limites actuales (API OpenRouter)

| Concepto | 1.2 Contributor | 1.3 Contributor | Variacion |
|---|---|---|---|
| **ID OpenRouter** | `meta/muse-spark-1.2-contributor` | `meta/muse-spark-1.3-contributor` | — |
| **Canonical slug** | `...-20260805` | `...-20260902` | +28 dias |
| **Precio input (prompt)** | USD 0,10 / M tokens | USD 0,10 / M tokens | sin cambio |
| **Precio output (completion)** | USD 0,20 / M tokens | USD 0,20 / M tokens | sin cambio |
| **Cache read (input_cache_read)** | USD 0,002 / M tokens | USD 0,002 / M tokens | sin cambio |
| **Cache write** | no facturado (no expuesto en pricing) | no facturado (no expuesto en pricing) | — |
| **Web search** | USD 0,0025 / request | USD 0,0025 / request | sin cambio |
| **Contexto maximo** | 1.048.576 tokens (1 M) | 1.048.576 tokens (1 M) | sin cambio |
| **Output maximo** | 943.718 tokens | 943.718 tokens | sin cambio |
| **Modalidades** | text+image+file+audio+video -> text | text+image+file+audio+video -> text | sin cambio |
| **Reasoning obligatorio** | si | si | — |
| **Reasoning efforts soportados** | `xhigh, high, medium, low, minimal` | `max, xhigh, high, medium, low, minimal` | **+1 nivel: `max`** |
| **Reasoning default** | `medium` | `medium` | sin cambio |
| **Parametros soportados** | reasoning, include_reasoning, max_tokens, repetition_penalty, top_k, temperature, top_p, tools, tool_choice, structured_outputs, response_format, reasoning_effort | identico | sin cambio |
| **Proveedor / tag** | Meta / `meta` | Meta / `meta` | — |
| **Uptime 30m / 5m** | 100% / 100% | 100% / 100% | — |

Valores raw de la API para referencia:

```
prompt:            "0.0000001"  => 0,10 / M
completion:        "0.0000002"  => 0,20 / M
input_cache_read:  "0.000000002" => 0,002 / M
```

> Nota sobre el tier no-contributor: `meta/muse-spark-1.2` y `meta/muse-spark-1.3` (sin sufijo contributor) cuestan USD 1,25/M input, USD 4,25/M output y USD 0,15/M cache-read. Es decir, el tier contributor es 12,5x mas barato en input y 21x mas barato en output. Ambos tiers mantienen la misma relacion de precios entre 1.2 y 1.3.

## 2. Calculo de costo efectivo

Escenario: **30 M tokens de entrada con 75% cache hit + output equivalente al 10% del input (3 M tokens)**.

| Componente | Volumen | Tarifa | Costo |
|---|---|---|---|
| Input cacheado (cache-read) | 22,5 M | USD 0,002 / M | USD 0,045 |
| Input fresco (prompt) | 7,5 M | USD 0,10 / M | USD 0,750 |
| **Subtotal input** | **30 M** | — | **USD 0,795** |
| Output | 3 M | USD 0,20 / M | USD 0,600 |
| **Total** | — | — | **USD 1,395** |
| **Costo efectivo por M de input** | — | — | **USD 0,0465 / M** |

| Metrica | 1.2 Contributor | 1.3 Contributor |
|---|---|---|
| Costo total escenario | USD 1,395 | USD 1,395 |
| Costo efectivo / M input | USD 0,0465 | USD 0,0465 |
| Diferencia | — | USD 0,00 (0%) |

Con 75% de cache, el costo efectivo cae a menos de la mitad del precio base de input. Sin cache, el mismo escenario costaria USD 3,00 de input + USD 0,60 de output = USD 3,60. El cache ahorra USD 2,205 en este volumen.

Para referencia, el mismo escenario en tier no-contributor costaria USD 5,625 de input (22,5M x 0,15 + 7,5M x 1,25) + USD 12,75 de output = USD 18,375. El tier contributor reduce el costo total en un 92%.

## 3. Que cambio del 1.2 al 1.3

A nivel de API de OpenRouter, el cambio observable es minimo:

1. **Nuevo nivel de reasoning `max`**. Es la unica diferencia estructural en `supported_efforts`. El 1.2 ofrece hasta `xhigh`; el 1.3 anade `max` por encima. Permite forzar razonamiento mas profundo y mas tokens de pensamiento cuando la tarea lo requiere, sin cambiar el precio. El default permanece en `medium` en ambos.

2. **Modelo mas reciente**. Canonical slug del 2026-09-02 vs 2026-08-05. Un mes de diferencia sugiere pesos actualizados, correcciones y mejoras de calidad propias de una iteracion menor de Meta, aunque OpenRouter no expone changelog de capacidades ni benchmarks.

3. **Paridad total en precio, contexto y limites**. Input, output, cache, contexto de 1 M, output maximo de 943 K, modalidades multimodales y lista de parametros son identicos. No hay regresion ni incremento de costo.

4. **Sin cambios en tooling ni formato**. Ambos soportan `tools`, `tool_choice`, `structured_outputs`, `response_format` y `include_reasoning` de la misma forma.

Lo que no se puede verificar desde la API: mejoras de calidad en razonamiento, codigo, uso de herramientas y seguimiento de instrucciones que Meta tipicamente introduce entre versiones menores. Para eso se requieren benchmarks externos (Artificial Analysis, LMArena, evaluaciones propias).

## 4. Vale la pena el upgrade

Si. El upgrade de 1.2 contributor a 1.3 contributor no tiene contrapartida negativa:

- **Mismo precio** en todos los conceptos, incluido cache.
- **Mismo contexto y limites**, sin riesgo de romper integraciones.
- **Mas capacidad de razonamiento** con el nivel `max` cuando se necesite, manteniendo compatibilidad hacia atras (si se usa `xhigh` o inferior, el comportamiento es equivalente).
- **Modelo mas nuevo**, por lo que recoge las ultimas correcciones de Meta.

Recomendacion practica: migrar el alias por defecto a `meta/muse-spark-1.3-contributor` y mantener `meta/muse-spark-1.2-contributor` solo como fallback si se detecta alguna regresion puntual. Dado que el tier contributor esta pensado para experimentacion y flujos agenticos tempranos, usar siempre la version mas reciente maximiza calidad sin costo adicional.

---

*Generado el 2026-09-05 desde datos en vivo de OpenRouter. Verificar precios antes de estimaciones de produccion, ya que pueden cambiar sin aviso.*
