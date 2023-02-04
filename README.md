# Intro
`pvsc49-satellite-sampling` is an investigation on the effect of averaging interval and sampling rate on hourly modeling errors, presented in **Effects of Solar Resource Sampling Rate and Averaging Interval on Hourly Modeling Errors** published in IEEE _Journal of Photovoltaics_, available from IEEE Xplore, DOI: [10.1109/JPHOTOV.2023.3238512](https://doi.org/10.1109/JPHOTOV.2023.3238512). This repository contains the analysis as well as the LaTeX files used to generate the preprint for submission.

# Analysis
The [analysis folder](https://github.com/mikofski/pvsc49-satellite-sampling/blob/main/analysis/) containes a separate [Jupyter notebook](https://jupyter.org/) for each of the seven SURFRAD sites:
* [Bondville, IL](https://github.com/mikofski/pvsc49-satellite-sampling/blob/main/analysis/instantaneous_weather-SURFRAD-bon.ipynb)
* [Desert Rock, NV](https://github.com/mikofski/pvsc49-satellite-sampling/blob/main/analysis/instantaneous_weather-SURFRAD-dra.ipynb)
* [Fort Peck, MT](https://github.com/mikofski/pvsc49-satellite-sampling/blob/main/analysis/instantaneous_weather-SURFRAD-fpk.ipynb)
* [Goodwin Creek, MS](https://github.com/mikofski/pvsc49-satellite-sampling/blob/main/analysis/instantaneous_weather-SURFRAD-gwn.ipynb)
* [Penn State, PA](https://github.com/mikofski/pvsc49-satellite-sampling/blob/main/analysis/instantaneous_weather-SURFRAD-psu.ipynb)
* [Sioux Falls, ID](https://github.com/mikofski/pvsc49-satellite-sampling/blob/main/analysis/instantaneous_weather-SURFRAD-sxf.ipynb)
* [Table Mountain (Boulder), CO](https://github.com/mikofski/pvsc49-satellite-sampling/blob/main/analysis/instantaneous_weather-SURFRAD-tbl.ipynb)

Each Jupyter notebook is a based on a template. Therefore, the organization of each is the same:
1. Useful Functions
2. Accessing SURFRAD Data
3. Narrowing Selection
4. Quality Assurance & Control
5. Load SURFRAD Daily Weather Data
6. Simulate Sampled Data at Different Rates
7. Visual Comparisons
8. PV Model
9. All (Good) Years Results

## Python Packages
The analysis uses [pvlib](https://pvlib-python.readthedocs.io/en/stable/) to model PV performance.
[![powered by pvlib](https://pvlib-python.readthedocs.io/en/stable/_images/pvlib_powered_logo_horiz.png)](https://pvlib-python.readthedocs.io/en/stable/)

Other [Python](https://www.python.org/) libraries used are [Matplotlib](https://matplotlib.org/), [NumPy](https://numpy.org/), [Pandas](https://pandas.pydata.org/), and [Seaborn](https://seaborn.pydata.org/).

## SURFRAD Data
[SURFRAD data](https://gml.noaa.gov/grad/surfrad/) is required to run the analysis. This data can be obtained using [`pvlib.iotools.read_surfrad`](https://pvlib-python.readthedocs.io/en/stable/reference/generated/pvlib.iotools.read_surfrad.html), but be patient. It's many gigabytes of data and can take a few hours to download.

# Preprint
This repo contains the manuscript that was submitted as original research and published in JPV at IEEE Xplore. LaTeX was used to render the manuscript. The coauthors collaborated online using [Overleaf](https://www.overleaf.com/), and I also used [Sublime Text](https://www.sublimetext.com/) with [LaTeXTools plugin](https://latextools.readthedocs.io/en/latest/) and [Sumatra](https://www.sumatrapdfreader.org/free-pdf-reader). A PDF is rendered and deployed to GitHub pages automatically on each commit using GitHub actions in the `workflows` folder. Note: this PDF is not the final version published by IEEE.

# Licences & Copyrights
* The LaTeX document in this repo is a preprint of **Effects of Solar Resource Sampling Rate and Averaging Interval on Hourly Modeling Errors** published in IEEE _Journal of Photovoltaics_, available from IEEE Xplore, DOI: [10.1109/JPHOTOV.2023.3238512](https:/doi.org/10.1109/JPHOTOV.2023.3238512).
* The analysis code in this repo is [BSD-3 licensed](https://github.com/mikofski/pvsc49-satellite-sampling/blob/main/LICENSE).
* This README and all other text are licensed under [Creative Common BY-SA 4.0](http://creativecommons.org/licenses/by-sa/4.0/).

<p xmlns:cc="http://creativecommons.org/ns#" xmlns:dct="http://purl.org/dc/terms/">
<img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/cc.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/by.svg?ref=chooser-v1"><img style="height:22px!important;margin-left:3px;vertical-align:text-bottom;" src="https://mirrors.creativecommons.org/presskit/icons/sa.svg?ref=chooser-v1">
<a property="dct:title" rel="cc:attributionURL" href="https://github.com/mikofski/pvsc49-satellite-sampling">PVSC49-Satellite-Sampling</a> by <a rel="cc:attributionURL dct:creator" property="cc:attributionName" href="https://mikofski.github.io/">Mark A. Mikofski</a> is licensed under <a href="http://creativecommons.org/licenses/by-sa/4.0/?ref=chooser-v1" target="_blank" rel="license noopener noreferrer" style="display:inline-block;">CC BY-SA 4.0</a>
</p>

Mark A. Mikofski (c) 2023
