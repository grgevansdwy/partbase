# partbase

A small electronic parts database. Parts are kept as CSV files (one per component type) and built into a SQLite database, `parts.db`.

Each part row includes its electrical values, manufacturer info, and references to the schematic symbol and PCB footprint libraries (`.SchLib` / `.PcbLib`).

## Layout

```
partbase/
├── build_sqlite.py   # builds parts.db from data/*.csv
├── data/
│   ├── capacitor.csv
│   └── resistor.csv
└── parts.db          # generated
```

## Usage

Requires Python 3 (standard library only).

```bash
python3 build_sqlite.py
```

This deletes any existing `parts.db` and rebuilds it from scratch. Every `data/*.csv` file becomes a table named after the file (`capacitor.csv` → `capacitor`).

Query it with the `sqlite3` CLI:

```bash
sqlite3 parts.db 'SELECT "Part Number", Value, Package FROM capacitor;'
```

## CSV format

- The first row is the header. Column names become table columns.
- `Part Number` is required in every file. It becomes the `PRIMARY KEY`.
- All columns are stored as `TEXT` and are `NOT NULL`, so empty cells must still be present in the row.

### Columns

| Table | Columns |
|-------|---------|
| `capacitor` | Part Number, Value, Voltage, Dielectric, Tolerance, Package, Manufacturer, MPN, Description, Library Ref, Library Path, Footprint Ref, Footprint Path |
| `resistor` | Part Number, Value, Power, Tolerance, Composition, Package, Manufacturer, MPN, Description, Library Ref, Library Path, Footprint Ref, Footprint Path |

Part numbers use a type prefix and a counter, e.g. `CAP-0001`, `RES-0001`.

## Adding a component type

1. Add a new CSV to `data/` with a `Part Number` column.
2. Re-run `python3 build_sqlite.py`.

## Later decisions

- Capacitor values: decide how to normalise them, since `100nF` and `0.1uF` are the same value.
