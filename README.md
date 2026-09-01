# mplstyle_for_MNRAS
This repository contains a matplotlib (mpl) stylesheet which (when imported) creates plots looking nice in MNRAS (Monthly Notices of the Royal Astronomical Society) papers, following MNRAS's official guidelines: https://academic.oup.com/mnras/pages/general_instructions!

### WHERE TO STORE THE FILE AND HOW TO IMPORT IT
An easy way to use the file is to save it together with the Python script producing the plot (in the same directory). Then,
as done in the test script `mpltest.py`, it can be imported via

`import matplotlib.pyplot as plt`</br>
`plt.style.use('./MNRAS_Style.mplstyle')`

Of course, you can also save the file in the default directory for matplotlib stylesheets. If you don't know the path of this
directory, just execute the commands

`import matplotlib as mpl`</br>
`print mpl.get_configdir()`

#### MNRAS column fig width = 3.32088003 inch ,  width_pt = 240
#### The Height isn't important, but myfigsize.py gives height with the golden ratio; try it.

### This style changes the default colours to a colour-blind-friendly palette; let's be nice to everyone.

To learn more about mpl styles: 

https://matplotlib.org/stable/users/explain/customizing.html and https://matplotlib.org/stable/users/explain/configuration.html
