# Add base colors
_colors = {
    "blue": {
        100: "#00549F",
        75: "#407FB7",
        50: "#8EBAE5",
        25: "#C7DDF2",
        10: "#E8F1FA"
    },
    "black": {
        100: "#000000",
        75: "#646567",
        50: "#9C9E9F",
        25: "#CFD1D2",
        10: "#ECEDED"
    },
    "magenta": {
        100: "#E30066",
        75: "#E96088",
        50: "#F19EB1",
        25: "#F9D2DA",
        10: "#FDEEF0"
    },
    "yellow": {
        100: "#FFED00",
        75: "#FFF055",
        50: "#FFF59B",
        25: "#FFFAD1",
        10: "#FFFDEE"
    },
    "petrol": {
        100: "#006165",
        75: "#2D7F83",
        50: "#7DA4A7",
        25: "#BFD0D1",
        10: "#E6ECEC"
    },
    "turqoise": {
        100: "#0098A1",
        75: "#00B1B7",
        50: "#89CCCF",
        25: "#CAE7E7",
        10: "#EBF6F6"
    },
    "green": {
        100: "#57AB27",
        75: "#8DC060",
        50: "#B8D698",
        25: "#DDEBCE",
        10: "#F2F7EC"
    },
    "lime": {
        100: "#BDCD00",
        75: "#D0D95C",
        50: "#E0E69A",
        25: "#F0F3D0",
        10: "#F9FAED"
    },
    "orange": {
        100: "#F6A800",
        75: "#FABE50",
        50: "#FDD48F",
        25: "#FEEAC9",
        10: "#FFF7EA"
    },
    "red": {
        100: "#CC071E",
        75: "#D85C41",
        50: "#E69679",
        25: "#F3CDBB",
        10: "#FAEBE3"
    },
    "darkred": {
        100: "#A11035",
        75: "#B65256",
        50: "#CD8B87",
        25: "#E5C5C0",
        10: "#F5E8E5"
    },
    "bordeaux": {
        100: "#612158",
        75: "#834E75",
        50: "#A8859E",
        25: "#D2C0CD",
        10: "#EDE5EA"
    },
    "lavender": {
        100: "#7A6FAC",
        75: "#9B91C1",
        50: "#BCB5D7",
        25: "#DEDAEB",
        10: "#F2F0F7"
    }
}

# Flatten
_flattened = {(name, op): val for name, values in _colors.items() for op, val in values.items()}

# And add defaults (100% opacity)
colors = {key: _colors[key][100] for key in _colors.keys()}

colors = {**colors, **_flattened}


def plot_colors():
    """
    Plot the colors of the RWTH colorspace by key and opacity (uses matplotlib).
    """
    try:
        from matplotlib import pyplot as plt
    except ImportError:
        import logging
        logging.error("Plotting the colorspace requires matplotlib.")
        return
    from math import floor
    numcolors = len(_colors.keys())
    rows = (floor(numcolors / 3) + 1 if numcolors % 3 else numcolors / 3)
    cols = 3
    fig, _ = plt.subplots(nrows=rows, ncols=cols)
    for ax, (cname, cvalues) in zip(fig.axes, _colors.items()):
        for idx, (op, c) in enumerate(cvalues.items()):
            ax.bar(idx, 1, color=c, tick_label=op)
        ax.set_title(cname, size=9)
        ax.set_yticklabels([])
        ax.set_yticks([])
        ax.set_xticks(range(5))
        ax.set_xticklabels((100, 75, 50, 25, 10))
    for ax in fig.axes[numcolors:]:
        ax.set_visible(False)
    fig.suptitle("RWTH Colors by key and opacity")
    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    plot_colors()
