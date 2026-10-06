# CMasher colours and colormaps

Colours and colormaps from [CMasher](https://cmasher.readthedocs.io).
CMasher is **optional**: install it with `pip install cmasher` (or
`pip install "plotastro[cmasher]"`). plotastro imports it only when one of
these features is used. See the {doc}`CMasher section of the colours guide <../colors>`
for choosing a map and worked examples.

```{eval-rst}
.. currentmodule:: plotastro
```

## Functions

```{eval-rst}
.. autofunction:: cmasher_colors

.. autofunction:: cmasher_cmap
```

## Through `set_style`

| argument | effect |
|---|---|
| `set_style(palette="cmr.<name>")` | colour cycle of 8 colours, `cmasher_colors("<name>")` |
| `set_style(cmap="cmr.<name>")` | default colormap for `imshow`, `pcolormesh`, `scatter`, ... |

Here the `cmr.` prefix is required. The two functions above accept names
with or without it. Add `_r` to any name for the reversed map.

Once CMasher has been imported, by one of these calls or by
`import cmasher`, matplotlib also accepts its maps by name:
`cmap="cmr.iceburn"`.

## Errors

| error | cause |
|---|---|
| `ImportError: This feature needs the optional CMasher package` | CMasher isn't installed |
| `ValueError: Unknown CMasher colormap '...'` | the name isn't a CMasher map in your version; `cmasher.get_cmap_list()` lists them |
| `ValueError: Unknown palette '...'` | `set_style(palette=...)` got a CMasher name without the `cmr.` prefix |
| `ValueError: '...' is not a valid value for cmap` | raised by matplotlib: a `cmr.` name was used before CMasher was imported |

`set_style` checks the palette and colormap before it changes anything,
so when it raises one of these errors the previous style is still active.
