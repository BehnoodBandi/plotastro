# Palettes and colour tools

The colour palettes plotastro ships, the Euclid colour schemes, and
helpers for matched shades. See {doc}`../colors` for the guide, with
swatches of the palettes.

```{eval-rst}
.. currentmodule:: plotastro
```

## Palettes

All palettes are plain dicts of hex strings, so `pa.OKABE_ITO["blue"]`
works anywhere matplotlib takes a colour, and `list(palette.values())`
gives the colours in order.

```{eval-rst}
.. py:data:: COLORS
   :type: dict[str, str]

   The default colour-blind-friendly cycle of every style, by name. The
   first nine are a colour-blind-safe reordering of ColorBrewer *Set1*;
   the last three are light companions from Tableau's *Color Blind 10*,
   for bands and de-emphasised data. Matplotlib's ``"C0"`` to ``"C11"``
   refer to the same colours.

   .. code-block:: python

      {"blue": "#377eb8", "orange": "#ff7f00", "green": "#4daf4a",
       "pink": "#f781bf", "brown": "#a65628", "purple": "#984ea3",
       "grey": "#999999", "red": "#e41a1c", "yellow": "#dede00",
       "lightblue": "#a2c8ec", "lightorange": "#ffbc79", "lightgrey": "#ababab"}

.. py:data:: CYCLE
   :type: list[str]

   The colours of :data:`COLORS`, in cycle order.

.. py:data:: OKABE_ITO
   :type: dict[str, str]

   Okabe & Ito (2008): the classic 8-colour palette designed for all
   common types of colour-vision deficiency.

   .. code-block:: python

      {"black": "#000000", "orange": "#e69f00", "skyblue": "#56b4e9",
       "green": "#009e73", "yellow": "#f0e442", "blue": "#0072b2",
       "vermillion": "#d55e00", "purple": "#cc79a7"}

.. py:data:: PETROFF8
   :type: dict[str, str]

   Petroff (2021), 8 colours: matplotlib's ``petroff8`` and the default
   cycle of the Euclid Consortium's niceplots (its ``"categorical1"``
   scheme, and the cycle of the ``euclid`` style).

   .. code-block:: python

      {"blue": "#1845fb", "orange": "#ff5e02", "red": "#c91f16",
       "magenta": "#c849a9", "khaki": "#adad7d", "lightblue": "#86c8dd",
       "cornflower": "#578dff", "grey": "#656364"}

.. py:data:: PETROFF10
   :type: dict[str, str]

   Petroff (2021), 10 colours: the colour-vision-optimised cycle that is
   matplotlib's ``petroff10`` and widely used in particle physics.

   .. code-block:: python

      {"blue": "#3f90da", "yellow": "#ffa90e", "red": "#bd1f01",
       "grey": "#94a4a2", "purple": "#832db6", "brown": "#a96b59",
       "orange": "#e76300", "tan": "#b9ac70", "slate": "#717581",
       "cyan": "#92dadd"}

.. py:data:: TOL_VIBRANT
   :type: dict[str, str]

   Paul Tol's *vibrant* qualitative scheme: 7 colours, safe for
   colour-vision deficiencies. Niceplots' ``"categorical3"`` is this
   palette with black in front.

   .. code-block:: python

      {"orange": "#ee7733", "blue": "#0077bb", "cyan": "#33bbee",
       "magenta": "#ee3377", "red": "#cc3311", "teal": "#009988",
       "grey": "#bbbbbb"}

.. py:data:: PAIRED
   :type: dict[str, tuple[str, str]]

   Light/dark pairs from ColorBrewer *Paired*, for data/model or
   before/after comparisons: ``PAIRED["blue"]`` is ``(light, dark)``.
   On its own this palette is *not* fully safe for colour-vision
   deficiencies (it has red and green), so pair it with line styles or
   markers.

   .. code-block:: python

      {"blue": ("#a6cee3", "#1f78b4"), "green": ("#b2df8a", "#33a02c"),
       "red": ("#fb9a99", "#e31a1c"), "orange": ("#fdbf6f", "#ff7f00"),
       "purple": ("#cab2d6", "#6a3d9a"), "brown": ("#ffff99", "#b15928")}

.. autofunction:: euclid_colors
```

(api-palette-names)=
### Palette names for `set_style`

`set_style(palette=...)` makes any of these the colour cycle. Case,
hyphens, underscores and spaces in the name are ignored.

| `palette=` | colours |
|---|---|
| `"default"` (or `"plotastro"`) | {data}`COLORS` |
| `"okabe_ito"` | {data}`OKABE_ITO` |
| `"petroff8"`, `"petroff10"` | {data}`PETROFF8`, {data}`PETROFF10` |
| `"tol_vibrant"` | {data}`TOL_VIBRANT` |
| `"categorical1"`, `"categorical2"`, `"categorical3"`, `"sequential"`, `"diverging"` | the Euclid schemes, from {func}`euclid_colors` (8 colours for the last two) |
| `"cmr.<name>"` | 8 colours from a CMasher colormap, from {func}`cmasher_colors` (see {doc}`cmasher`) |
| a list or dict of colours | those colours |

## Shades

```{eval-rst}
.. autofunction:: lighten

.. autofunction:: darken
```

## Swatch chart

```{eval-rst}
.. autofunction:: show_colors
```
