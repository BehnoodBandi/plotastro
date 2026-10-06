# Styles and figure sizes

Activate a journal's look, then make figures at exactly the size the
journal prints them. {doc}`../journals` describes each journal and
{doc}`../quickstart` walks through a first figure.

```{eval-rst}
.. currentmodule:: plotastro
```

## Activating a style

```{eval-rst}
.. autofunction:: set_style

.. py:function:: use(journal="mnras", *, usetex=False, grid=None, palette=None, cmap=None, **rc_overrides)

   Alias of :func:`set_style`, for those who prefer ``pa.use("mnras")``,
   after which everything is plain matplotlib.

.. autofunction:: current_journal
```

(api-journal-names)=
### Journal names

`journal=` takes a key or an alias, in {func}`set_style`, {func}`figsize`,
{func}`subplots` and {func}`authorlist`. Case, spaces and hyphens are
ignored, so `"A&A"` and `"Open Journal"` work too.

| key | journal | aliases |
|---|---|---|
| `mnras` | Monthly Notices of the RAS | `mnras_full` (from the original API) |
| `rasti` | RAS Techniques and Instruments | |
| `aanda` | Astronomy & Astrophysics | `a&a`, `aa`, `astronomy&astrophysics` |
| `apj` | The Astrophysical Journal (AASTeX) | `apjl`, `aj`, `aas`, `aastex` |
| `oja` | The Open Journal of Astrophysics | `openjournal`, `theoj`, `openjournalofastrophysics` |
| `prd` | Physical Review D (REVTeX 4.2) | `prl`, `aps`, `revtex` |
| `jcap` | J. of Cosmology and Astroparticle Physics | |
| `natastro` | Nature Astronomy | `nature`, `natureastronomy`, `natastron` |
| `euclid` | Euclid Consortium (A&A, niceplots look) | `ec`, `euclidconsortium`, `niceplots` |
| `thesis` | A4 thesis text width (MNRAS look) | |
| `beamer` | Beamer slide text width (MNRAS look) | |

(api-plain-matplotlib)=
### With plain matplotlib

Importing plotastro registers its styles with matplotlib, so afterwards
they work in any code, without the helpers:

```python
import matplotlib.pyplot as plt
import plotastro                  # registers the styles

plt.style.use("mnras")
```

The registered names are the style files: `mnras`, `rasti`, `aanda`,
`apj`, `oja`, `prd`, `jcap`, `natastro` and `euclid`. Each sets the
journal's fonts, ticks and colour cycle, and a one-column default figure
size. Aliases, the `thesis` and `beamer` presets, and the extra options
(`usetex`, `grid`, `palette`, `cmap`) are only available through
{func}`set_style`.

## Figure sizes

```{eval-rst}
.. autofunction:: figsize

.. autofunction:: subplots

.. autofunction:: savefig
```

## Journal data

```{eval-rst}
.. py:data:: JOURNALS
   :type: dict

   Layout of every journal and preset, keyed by journal name (see
   :ref:`api-journal-names`). Each entry has:

   ``"column"``, ``"full"``
       One-column and full text width, in LaTeX points (1 pt = 1/72.27 in).
       They are equal for single-column layouts (``jcap``, ``thesis``,
       ``beamer``).
   ``"style"``
       The ``.mplstyle`` file the journal uses, in :data:`STYLE_DIR`.
   ``"tex"``
       The LaTeX preamble ``set_style(usetex=True)`` uses, matching the
       journal's fonts.
   ``"name"``
       The journal's full name.
   ``"aspect"`` (optional)
       Default height/width ratio, if not :data:`GOLDEN`. Only ``euclid``
       has one (0.75).

   .. code-block:: python

      >>> pa.JOURNALS["mnras"]["column"], pa.JOURNALS["mnras"]["full"]
      (240.0, 504.0)

.. py:data:: GOLDEN
   :type: float

   The golden ratio, (√5 − 1)/2 ≈ 0.618: the default height/width ratio
   of a panel in :func:`figsize` (except for ``euclid``, which uses 4:3).

.. py:data:: STYLE_DIR
   :type: pathlib.Path

   The folder holding the bundled ``.mplstyle`` files. To use the styles
   without importing plotastro, copy them into matplotlib's style
   library, ``matplotlib.get_configdir()/stylelib/``.
```

## Legacy

```{eval-rst}
.. autofunction:: set_size
```
