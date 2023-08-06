# PyLauda

This package holds python driver to communicate with the serial ports of Lauda temperature control systems.

## Installation

Perform a package install:

```bash
pip install .
```

## Usage

```python
from PyLauda import re206

dev = re206('/dev/ttyUSB0')
dev.temperature = 20
print(dev.temperature)

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
MIT
