# Markers, line styles and panel labels

Markers and dash patterns that stay distinguishable at journal sizes, a
cycler that pairs them with colours, and panel labels. See
{doc}`../markers` for the guide.

```{eval-rst}
.. currentmodule:: plotastro
```

## Markers and line styles

```{eval-rst}
.. py:data:: MARKERS
   :type: list[str]

   A marker sequence that stays distinguishable at small sizes:

   .. code-block:: python

      ["o", "s", "^", "D", "v", "p", "*", "X"]

.. py:data:: LINESTYLES
   :type: dict[str, str | tuple]

   Named dash patterns beyond matplotlib's built-ins. The tuples are
   matplotlib ``(offset, (on, off, ...))`` dash specs, which scale with
   the line width and print cleanly. Use them as
   ``ls=pa.LINESTYLES["long dash"]``.

   .. code-block:: python

      {"solid": "-",
       "dashed": (0, (5, 2)),
       "dotted": (0, (1, 1.5)),
       "dashdot": (0, (5, 2, 1, 2)),
       "long dash": (0, (9, 3)),
       "dash dot dot": (0, (5, 2, 1, 2, 1, 2)),
       "densely dotted": (0, (1, 0.8)),
       "loosely dashed": (0, (5, 6))}

.. autofunction:: show_markers

.. autofunction:: show_linestyles
```

## Cycling colours, markers and dashes together

```{eval-rst}
.. autofunction:: style_cycler
```

To pair markers with colours from another palette, build the cycle
yourself, e.g.
`plt.cycler(color=pa.cmasher_colors("torch", n=4)) + plt.cycler(marker=pa.MARKERS[:4])`.

## Panel labels

```{eval-rst}
.. autofunction:: label_panels
```
