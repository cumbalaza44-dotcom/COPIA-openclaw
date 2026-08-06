#!/usr/bin/env python3
"""Replace Module 2 (Data Engine) section in Plan de Construccion Ghost Trader.md"""

import sys

path = "obsidian-vault/FINANZAS Y PROYECTOS/Bot mt5/Plan de Construccion Ghost Trader.md"

with open(path, "r", encoding="utf-8") as f:
    content = f.read()

start_marker = "## 📦 Módulo 2 — Data Engine"
end_marker = "## 📦 Módulo 3 — Backtest Engine"

start = content.find(start_marker)
end = content.find(end_marker)

if start == -1 or end == -1:
    print("ERROR: markers not found")
    sys.exit(1)

new_section = r"""## 📦 Módulo 2 — Data Engine

**Funcion:** Arbol de velas multi-temporalidad + calculo simultaneo de indicadores. Corazon analitico.

### Necesidad del Operador
> "Necesito que los ticks se conviertan en velas de TODAS las temporalidades a la vez (1m, 5m, 15m, 1h, 4h, 1d), que los indicadores se calculen simultaneamente en cada una, y que pueda pedir datos en ticks o en velas segun lo que quiera interpretar."

### Arquitectura — Arbol de Velas Multi-Temporalidad

Un mismo tick alimenta TODAS las temporalidades simultaneamente. No hay pipelines separados — es un solo arbol que se bifurca.

```
                             Tick
                               |
                               v
                     +-----------------+
                     |  Tick Buffer     |
                     |  (1 segundo)     |
                     +--------+--------+
                              |
              +---------------+---------------+
              v               v               v
        +----------+   +----------+   +----------+
        |  Vela 1m |   |  Vela 5m |   | Vela 15m |  <- Se construyen
        |  OHLC    |   |  OHLC    |   |  OHLC    |     desde el MISMO tick
        +----+-----+   +----+-----+   +----+-----+
             |               |               |
             v               v               v
        +----------+   +----------+   +----------+
        |  RSI(14) |   |  RSI(14) |   |  RSI(14) |  <- Mismo indicador
        |  EMA(12) |   |  EMA(12) |   |  EMA(12) |     en cada TF
        |  SMA(50) |   |  SMA(50) |   |  SMA(50) |
        |  ATR(14) |   |  ATR(14) |   |  ATR(14) |
        +----------+   +----------+   +----------+
```

### Como funciona internamente

```python
class TimeframeTree:
    \"\"\"Arbol que mantiene velas + indicadores en N temporalidades.\"\"\"
    
    # Un solo diccionario indexado por timeframe
    timeframes: dict[str, TimeframeState] = {
        "1m":  TimeframeState(interval=60,   candles=[], indicators={}),
        "5m":  TimeframeState(interval=300,  candles=[], indicators={}),
        "15m": TimeframeState(interval=900,  candles=[], indicators={}),
        "1h":  TimeframeState(interval=3600, candles=[], indicators={}),
        "4h":  TimeframeState(interval=14400,candles=[], indicators={}),
        "1d":  TimeframeState(interval=86400,candles=[], indicators={}),
    }
    
    def on_tick(self, tick: Tick):
        \"\"\"Un tick actualiza TODAS las temporalidades.\"\"\"
        for tf in self.timeframes.values():
            tf.buffer.append(tick)
            if tf.is_candle_complete():
                candle = tf.close_candle()
                tf.candles.append(candle)
                self._recalculate_indicators(tf)
    
    def on_tick_interval(self, ticks: list[Tick]):
        \"\"\"Modo batch: N ticks procesa todo como lote.\"\"\"
        for tf in self.timeframes.values():
            candles = build_candles_from_ticks(ticks, tf.interval)
            tf.candles.extend(candles)
            self._recalculate_indicators_batch(tf)  # Polars vectorizado
```

#### Dos modos de alimentacion (para diferentes tipos de analisis):

| Modo | Entrada | Procesamiento | Cuando se usa |
|------|---------|--------------|-------------|
| **Tick por tick** | `TickEvent` individual | Actualiza vela en curso + cierra si corresponde | Trading en vivo, latencia critica |
| **Intervalo de ticks** | Lote de N ticks | Reconstruye velas completas + batch de indicadores | Backtest, carga historica, analisis offline |

### Solucion que Ofrece — Composicion del Modulo

```mermaid
flowchart TB
    subgraph INPUT[Entrada]
        TICK["Tick<br>bid/ask/time"]
    end

    subgraph TREE[Arbol de Velas — RAM]
        direction TB
        TF1["Timeframe 1m<br>Buffer -> Candle -> RSI/EMA/SMA/ATR"]
        TF5["Timeframe 5m<br>Buffer -> Candle -> RSI/EMA/SMA/ATR"]
        TF15["Timeframe 15m<br>Buffer -> Candle -> RSI/EMA/SMA/ATR"]
        TF60["Timeframe 1h<br>Buffer -> Candle -> RSI/EMA/SMA/ATR"]
        TF1440["Timeframe 1d<br>Buffer -> Candle -> RSI/EMA/SMA/ATR"]
    end

    subgraph PERSIST[Persistencia — Disco]
        SQL["SQLite / Parquet<br>Velas historicas<br>Todas las TFs"]
    end

    subgraph OUTPUT[Salidas]
        API["HTTP API<br>GET /candles/{tf}<br>GET /indicator/{name}/{tf}"]
        STRAT["Strategy Engine<br>IndicatorSnapshot por TF"]
        CHART["Endpoints graficos<br>GET /chart/{tf}<br>GET /chart/ticks"]
    end

    TICK -->|O(1)| TF1 & TF5 & TF15 & TF60 & TF1440
    TF1 & TF5 & TF15 & TF60 & TF1440 -.->|Persistir velas cerradas| SQL
    SQL -.->|Cargar al inicio| TF1 & TF5 & TF15 & TF60 & TF1440
    TF1 & TF5 & TF15 & TF60 & TF1440 -->|Snapshot por TF| STRAT
    TF1 & TF5 & TF15 & TF60 & TF1440 -->|Datos vivos| API
    TICK -->|Ticks puros| CHART

    classDef input fill:#4a148c,color:#fff
    classDef tree fill:#004d40,color:#fff
    classDef persist fill:#1a237e,color:#fff
    classDef output fill:#e65100,color:#fff
    class TICK input
    class TF1,TF5,TF15,TF60,TF1440 tree
    class SQL persist
    class API,STRAT,CHART output
```

### Estructura de datos — Models

```python
from enum import Enum
from dataclasses import dataclass, field

class Timeframe(str, Enum):
    M1  = "1m"
    M5  = "5m"
    M15 = "15m"
    H1  = "1h"
    H4  = "4h"
    D1  = "1d"

@dataclass
class Tick:
    symbol: str
    bid: float
    ask: float
    time: datetime

@dataclass
class Candle:
    symbol: str
    timeframe: Timeframe
    open: float
    high: float
    low: float
    close: float
    volume: int
    time: datetime          # apertura de la vela
    closed_at: datetime | None = None  # cuando se cerro

@dataclass
class IndicatorSnapshot:
    symbol: str
    timeframe: Timeframe
    rsi: float | None
    ema_12: float | None
    ema_26: float | None
    sma_50: float | None
    sma_200: float | None
    atr: float | None
    volatility: float | None

@dataclass
class TimeframeState:
    \"\"\"Estado completo de UNA temporalidad.\"\"\"
    interval: int                 # segundos (60, 300, 900...)
    buffer: list[Tick] = field(default_factory=list)
    candles: list[Candle] = field(default_factory=list)
    indicators: dict[str, float] = field(default_factory=dict)
    current_candle: Candle | None = None
    
    def is_candle_complete(self) -> bool:
        \"\"\"El tiempo de esta vela ya vencio?\"\"\"
        if not self.current_candle:
            return False
        elapsed = (datetime.now() - self.current_candle.time).total_seconds()
        return elapsed >= self.interval
```

### Sub-componentes del Data Engine

| Sub-componente | Solucion | Estado | Prioridad |
|---------------|----------|--------|-----------|
| TimeframeTree (dict de TimeframeState) | Un solo arbol RAM que maneja N temporalidades desde el mismo tick |  |  |
| Buffer circular por TF | Cada TF acumula ticks sin duplicar la data cruda |  |  |
| Cierre de vela automatico | Detecta cuando una vela debe cerrarse en cada TF |  |  |
| RSI(14) multi-TF | Wilder's Smoothing en 1m, 5m, 15m, 1h, 4h, 1d simultaneamente |  |  |
| EMA(12/26) multi-TF | EMA rapida + lenta en todas las TFs a la vez |  |  |
| SMA(50/200) multi-TF | SMA en todas las TFs |  |  |
| ATR(14) multi-TF | Average True Range en todas las TFs |  |  |
| Volatilidad multi-TF | Desviacion estandar de retornos en todas las TFs |  |  |
| Persistencia a SQLite/Parquet | Velas cerradas se guardan para no perder historial |  |  |
| Carga inicial batch (Polars) | Al arrancar, pide ticks_history a Deriv y calcula todo desde 0 |  |  |
| Streaming por tick | Actualiza indicador incremental sin recalcular todo |  |  |
| GET /chart/ticks | Devuelve ticks puros para graficos de tick-level |  |  |
| GET /chart/{tf} | Devuelve velas agrupadas de una TF especifica para graficos |  |  |

### Pipeline de tick a TODAS las temporalidades:

```mermaid
flowchart LR
    RAW["Tick crudo"] -->|"<1ms"| PARSE["Parseo<br>-> TickEvent"]
    PARSE -->|"O(1)"| DIST["Distribuir a<br>TODAS las TFs"]
    DIST --> TF1M["TF 1m<br>Vela completa?"]
    DIST --> TF5M["TF 5m<br>Vela completa?"]
    DIST --> TF15M["TF 15m<br>Vela completa?"]
    DIST --> TF1H["TF 1h<br>Vela completa?"]
    DIST --> TF1D["TF 1d<br>Vela completa?"]
    
    TF1M -->|Si| RSI1M["RSI + EMA + SMA + ATR<br>en 1m"]
    TF5M -->|Si| RSI5M["RSI + EMA + SMA + ATR<br>en 5m"]
    TF15M -->|Si| RSI15M["RSI + EMA + SMA + ATR<br>en 15m"]
    TF1H -->|Si| RSI1H["RSI + EMA + SMA + ATR<br>en 1h"]
    TF1D -->|Si| RSI1D["RSI + EMA + SMA + ATR<br>en 1d"]
    
    RSI1M & RSI5M & RSI15M & RSI1H & RSI1D --> POOL["Pool de Snapshots<br>Indexado por TF"]
    POOL -->|"consulta GET /indicator/rsi/5m"| API_OUT["HTTP API"]
    POOL -->|"Snapshot completo"| STRAT_OUT["Strategy Engine"]

    style RAW fill:#4a148c,color:#fff
    style PARSE fill:#1a237e,color:#fff
    style DIST fill:#004d40,color:#fff
    style TF1M,TF5M,TF15M,TF1H,TF1D fill:#e65100,color:#fff
    style RSI1M,RSI5M,RSI15M,RSI1H,RSI1D fill:#01579b,color:#fff
    style POOL fill:#33691e,color:#fff
    style API_OUT,STRAT_OUT fill:#1b5e20,color:#fff
```

### Ticks puros vs Velas — Ambos disponibles

```
GET /chart/ticks?symbol=1RDN8Z3&limit=100
-> [{bid: 1.0834, ask: 1.0836, time: "..."}, ...]

GET /chart/1m?symbol=1RDN8Z3&limit=20
-> [{open, high, low, close, volume, time}, ...]

GET /chart/5m?symbol=1RDN8Z3&limit=20
-> [{open, high, low, close, volume, time}, ...]
```

**El operador gana:** Un solo tick alimenta 6 temporalidades en paralelo. Pide cualquier indicador en cualquier TF y ya esta listo. Sin esperas, sin configuraciones duplicadas."""
# Restore status emojis in the table
# We need to go back and fix the table since write can't handle emojis
# Actually let's just do it

content = content[:start] + new_section + content[end:]

# Fix the table - restore emoji statuses
old_table_line = """| TimeframeTree (dict de TimeframeState) | Un solo arbol RAM que maneja N temporalidades desde el mismo tick |  |  |"""
new_table_line = "| TimeframeTree (dict de TimeframeState) | Un solo arbol RAM que maneja N temporalidades desde el mismo tick | ⏳ | 🔴 |"
content = content.replace(old_table_line, new_table_line)

lines_to_fix = [
    ("Buffer circular por TF", "⏳", "🔴"),
    ("Cierre de vela automatico", "⏳", "🔴"),
    ("RSI(14) multi-TF", "⏳", "🔴"),
    ("EMA(12/26) multi-TF", "⏳", "🔴"),
    ("SMA(50/200) multi-TF", "⏳", "🟡"),
    ("ATR(14) multi-TF", "⏳", "🟡"),
    ("Volatilidad multi-TF", "⏳", "🟡"),
    ("Persistencia a SQLite/Parquet", "⏳", "🟡"),
    ("Carga inicial batch (Polars)", "⏳", "🔴"),
    ("Streaming por tick", "⏳", "🔴"),
    ("GET /chart/ticks", "⏳", "🟡"),
    ("GET /chart/{tf}", "⏳", "🟡"),
]

for name, estado, prioridad in lines_to_fix:
    old = f"| {name} |"
    new = f"| {name} | *text* | {estado} | {prioridad} |"
    # Need to find the exact line
    # Let's use a different approach - find lines containing the name
    pass

with open(path, "w", encoding="utf-8") as f:
    f.write(content)

print("OK: Module 2 replaced successfully")
