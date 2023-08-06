# RWTH-colors

This package provides hexcodes for the official RWTH Aachen colorspace as documented by the RWTH corporate design
guidelines.

## Installation

```shell
pip install <path_to_repo>
```

## Usage

```python
from rwth_colors import colors
from matplotlib import pyplot as plt

plt.bar(1, 1, color=colors[("blue", 50)])  # Opacity 50%. Available values: 100%, 75%, 50%, 25%, 10%
plt.bar(1, 1, color=colors["blue"])  # Alias for the default blue color (opacity 100%)
```

## Available colors (_requires matplotlib_)

```python
from rwth_colors import plot_colors

plot_colors()
```

![Available colors.png](Available colors.png)