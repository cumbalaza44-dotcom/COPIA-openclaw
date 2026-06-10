# TOOLS.md - Local Notes

Skills define _how_ tools work. This file is for _your_ specifics — the stuff that's unique to your setup.

## QMD — Motor de Búsqueda del Vault

**Instalado:** `@tobilu/qmd` v2.5.3
**Modelo embedding:** `embeddinggemma-300M-Q8_0.gguf` (local, CPU)
**Índice:** `/root/.cache/qmd/index.sqlite`

### Colecciones
| Colección | Ruta | Contexto |
|-----------|------|----------|
| `vault` | `obsidian-vault/` | Sistema personal de Mr. Jair — tareas, proyectos, notas |
| `memory` | `memory/` + `MEMORY.md` | Memoria a largo plazo, preferencias, decisiones |

### Comandos clave
```bash
# Búsqueda rápida (BM25, sin embeddings)
qmd search "Meta Ads" --json -n 5

# Búsqueda semántica (requiere embeddings)
qmd vsearch "cómo deployar" --json -n 5

# Query híbrido (BM25 + vector + reranking, mejor calidad)
qmd query "prototipo moto sensor" --json -n 5

# Retrieve documento específico
qmd get "qmd://vault/tasks.md"
qmd get "#abc123"  # por docid

# Listar colección
qmd ls vault

# Status del índice
qmd status

# Re-indexar después de cambios
qmd update
qmd embed  # re-generar embeddings
```

### Regla de uso
- **SIEMPRE** usar `qmd search` antes de `grep` o `find` en el vault
- `--json` para output procesable por el agente
- `-n 5` para limitar resultados (ahorrar tokens)
- `qmd get` para leer documento completo después de encontrarlo

---

Add whatever helps you do your job. This is your cheat sheet.
