# Logbook2Mouse

This library reads a measurement logbook and generates a script for a SAXS instrument.

## Installation

```bash
pip install .
```

## Usage

```python
from logbook2mouse.logbook_reader import Logbook2MouseReader, Logbook2MouseEntry

reader = Logbook2MouseReader("path/to/logbook.xlsx")
entries = reader.get_entries()
for idx, entry in entries.items():
    print(f"Entry {idx}: {entry}")
```
