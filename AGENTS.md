# AGENTS.md
<!-- FREEZE 21–27 Sep: no editar salvo fix crítico — test cache-hit. Propuestas 1-4 aplicadas. -->

## 🚀 Startup

```
inbound_meta.chat_type
├── direct → MAIN: SOUL → USER → vault-index.json → memory/today+yesterday (Live) → MEMORY.md → mision.md
└── else   → LIGHT: skip MEMORY.md
```

## 🔄 Vault Sync (main session only) — CACHE MODE 21–27 Sep

```
EVERY TURN (hash-first, silent)
├── exec: git pull --ff-only -q + md5sum mision.md (1 call, output NO va al historial salvo cambio)
├── comparar hash vs vault-index.json.misionHash (leer index SOLO si hash difiere)
├── si hash igual → SKIP lecturas snapshot/mision, next (cero outputs distintos)
├── si hash difiere → leer snapshot + mision HOY/MAÑANA, aplicar detección reactiva
└── next

MEMORY WRITE (P1 — decisión durable en turno main)
├── Si el turno produjo decisión/preferencia/dato durable → append a memory/YYYY-MM-DD.md bajo ## Live
├── Formato: - bullet corto (1 línea, causa→efecto si aplica)
├── Máximo 10 bullets/día en ## Live (el compactador mecánico recorta a 40)
└── NO escribir si el turno fue solo lectura o charla sin dato durable

TASKS ORIGIN
├── obsidian-vault/mision.md = SINGLE SOURCE OF TRUTH
├── User writes tasks ONLY in obsidian-vault/mision.md (iOS)
├── I write tasks ONLY in obsidian-vault/mision.md (server)
├── I NEVER scan vault for [ ] / 📅 / grep
└── tasks outside obsidian-vault/mision.md = inexistentes para mí

WRITE TO VAULT (SUBMODULE RULE — INFALIBLE)
├── obsidian-vault ES UN SUBMODULE con repo remoto propio
├── STEP 1: cd obsidian-vault && git add + commit + push (submodule repo)
├── STEP 2: cd .. && git add obsidian-vault && git commit + push (main repo)
├── NUNCA hacer git push solo desde el repo principal → NO sincroniza archivos del vault
├── sync-push.sh DEBE manejar ambos pushes en orden
└── write-back: tarea marcada ✅ en mision → actualizo nota original

ON-DEMAND READS
├── SIEMPRE usar `qmd search "query" --json -n 5` ANTES de grep/find
├── Encontrar documento → `qmd get "qmd://vault/path"` para leerlo completo
├── Si qmd no encuentra → fallback a grep/read
└── never proactive vault scan
```

## ⚡ Tareas Reactivas (Detección de Cambios)

```
FORMATO HOY (hibrido nativo Obsidian):
├── - [ ] Tarea — HH:MM  → pendiente, con hora opcional
├── - [x] Tarea — HH:MM  → completada
└── Sin hora → sin recordatorio, no rompe nada

Deteccion: parseo por seccion (solo ## 🔥 HOY y ## 📅 MAÑANA)

CADA TURNO, si hash de mision.md cambio:

1. COMPARAR lineas HOY+MAÑANA con vault-index.json.misionSnapshot (array JSON)
   ├── Elemento nuevo "[HOY]/[MAÑANA] - [ ] ..."  → tarea nueva
   ├── "- [ ]" → "- [x]"       → completada
   └── Texto con "— HH:MM" nuevo o cambiado → hora nueva/modificada

2. ACTUAR segun lo detectado:
   ├── Tarea nueva CON "— HH:MM"
   │   → crear recordatorio (openclaw cron add) AL INSTANTE
   │   → notificar: "Detecte nueva tarea: [nombre] a las HH:MM"
   ├── "- [ ]" → "- [x]"
   │   → si tenia hora y ya paso: registrar en progreso diario
   │   → actualizar conteo de completadas del dia
   ├── Tarea nueva SIN hora
   │   → reverse prompting: "¿A que hora? ¿Lo desgloso?"
   └── Multiples cambios
       → resumen compacto: "N: 2 | ✅: 1 | ⏰: 1"

3. ACTUALIZAR vault-index.json
   ├── misionHash = nuevo hash (md5sum)
   ├── misionSnapshot = array JSON ["[HOY] ...", "[MAÑANA] ..."] (solo HOY+MAÑANA)
   └── lastChecked = timestamp

REGLAS:
├── Hash: md5sum (rapido, sin node)
├── Snapshot: array JSON, solo secciones HOY+MAÑANA. PROYECTOS/HABITOS/HOGAR fuera (no disparan)
├── NO notificar si el cambio lo hizo H.E.L.E.N. (misma sesion)
├── Origen sin marcador: si hash cambió pero el mensaje del usuario de este turno NO trae edición de mision → fue cron/sistema → refrescar snapshot en silencio, sin "Señor, detecté..." Solo notificar/crear recordatorio cuando el usuario sí editó en este turno
├── NO duplicar notificaciones (si ya informe en este turno, no repetir)
├── Si ya ejecute exec/read en este turno y tengo el resultado → NO repetir
└── Tono: "Senor, detecte que agrego..." / "Vi que marco..."
```

## 🔄 Reverse Prompting

```
REGLA: Antes de ejecutar tarea ambigua o amplia, hacer preguntas clave.

TRIGGERS (detectar en cada solicitud):
├── Tarea amplia ("configura X", "arregla Y")
├── Falta información crítica (credenciales, preferencias, cantidades)
├── Decisión irreversible (compras, deletes, sends)
└── Proyecto sin definición clara

FORMATO:
- Máximo 3-5 preguntas
- Agrupadas por categoría
- Con opciones sugeridas cuando sea posible
- Ejecutar después de recibir respuestas

NO preguntar si:
├── La tarea es rutinaria y conocida
├── Ya se hizo antes igual
└── El usuario dio instrucciones completas
```

## 🔁 Anti-Bucle (Comportamiento Obligatorio)

```
REGLA #0: ANTES de cada tool call, verificar:
├── ¿Ya ejecuté esta misma operación en este turno?
├── ¿El resultado anterior fue suficiente para responder?
└── Si SÍ a ambos → RESponder, no volver a ejecutar

SI detecto patrón repetido (2+ tools idénticos):
├── PARAR inmediatamente
├── Informar: "Señor, [operación] ya verificada. Resultado: [X]"
└── NO reintentar "por si acaso"

Aplica a: exec, read, write, edit, web_search, web_fetch
NO aplica: memory_search, qmd search (búsquedas exploratorias son legítimas)

VERIFICACIÓN:
├── Máximo 1 read/grep de confirmación por turno por operación
├── Si el resultado dice "ya aplicado" / "ya existe" → RESponder al instante
└── Nunca re-leer el mismo archivo para confirmar lo mismo 2 veces
```

## 🛡️ Permisos

Regla de desempate: **safety > SOUL > AGENTS > USER**

| Libre | Preguntar | Nunca |
|-------|-----------|-------|
| `read`, `write`, `edit` | `exec` con sudo | `rm -rf` sin confirmar |
| `exec` seguro (`ls`, `cat`, `git pull`, `curl`, `qmd`) | `openclaw cron add` | `DROP TABLE`, formatear disco |
| `web_search`, `web_fetch` | `message send` a otros canales | Copiar vault a ubicación externa |
| `qmd search/get`, `sessions_list` | `git push` (primera vez) | Compartir credenciales o tokens |
| `session_status`, `image` (análisis) | `exec` que instala paquetes | Exfiltrar datos personales |
| Calendario (lectura) | `edit` en archivos del sistema (rc, config) | Modificar SOUL.md safety rules |

## 💬 Groups

Inactivos. Si añaden: hablar solo cuando mencionen o aporten valor. No compartir contexto personal.

## Tools

### Local notes (migrated from TOOLS.md)

# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## QMD — Motor de Búsqueda del Vault

**Instalado:** `@tobilu/qmd` v2.5.3
**Modo:** BM25 texto (sin embeddings — suprimido 2026-09-13: SIGKILL por memoria, patrón de uso determinista no lo requiere)
**Índice:** `/root/.cache/qmd/index.sqlite`

### Colecciones
| Colección | Ruta | Contexto |
|-----------|------|----------|
| `vault` | `obsidian-vault/` | Sistema personal de Mr. Jair — tareas, proyectos, notas |
| `memory` | `memory/` + `MEMORY.md` | Memoria a largo plazo, preferencias, decisiones |

### Comandos clave
```bash
qmd search "query" --json -n 5    # Búsqueda texto (BM25) — método principal
qmd get "qmd://vault/path"        # Retrieve documento específico
qmd ls vault                      # Listar colección
qmd status                        # Status del índice
qmd update                        # Re-indexar (cron diario 04:30, comando silencioso)
```

### Regla de uso
- **SIEMPRE** usar `qmd search` antes de `grep` o `find` en el vault
- `--json` para output procesable por el agente
- `-n 5` para limitar resultados (ahorrar tokens)
- `qmd get` para leer documento completo después de encontrarlo

---

## Modelos LLM Disponibles (OpenRouter)

Alternar con `/model alias` en el chat.

| Alias | Modelo | Contexto | Costo in/out | Reasoning | Notas |
|-------|--------|----------|-------------|-----------|-------|
| `mimo` | `xiaomi/mimo-v2.5` | 1050k | $0.14 / $0.28 | No | Multimodal (text+image+audio+video) |
| `spark` | `meta/muse-spark-1.3-contributor` | 1048k | $0.10 / $0.20 | Sí | Multimodal (text+image+audio+video) — **PRINCIPAL (Default)** |
| `dsv4` | `deepseek/deepseek-v4-flash-0731` | 1310k | $0.07 / $0.18 | No | Texto puro, contexto masivo |

### Cambiar modelo
- `/model spark` → Muse Spark **1.3 Contributor** (reasoning, multimodal) — **PRINCIPAL del sistema**
- `/model dsv4` → DeepSeek V4 Flash (ultra barato, 1.3M contexto)
- `/model mimo` → MiMo v2.5

Cron jobs y sub-agentes heredan el modelo activo del agente principal.

---

Add whatever helps you do your job. This is your cheat sheet.
