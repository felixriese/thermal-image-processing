.. image:: https://api.codacy.com/project/badge/Grade/5a09a21296eb4f1ba84d1abb232267d9
    :target: https://www.codacy.com?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=felixriese/thermal-image-processing&amp;utm_campaign=Badge_Grade
    :alt: Codacy
.. image:: https://img.shields.io/github/license/felixriese/thermal-image-processing
    :target: LICENSE
    :alt: BSD-3-License
.. image:: https://zenodo.org/badge/DOI/10.5281/zenodo.3576242.svg
   :target: https://doi.org/10.5281/zenodo.3576242
   :alt: Zenodo

Processing Scripts for Thermal Infrared Cameras
================================================

Functions and scripts for thermal images like the ones of the camera FLIR Tau
2.

:License:
    `3-Clause BSD license <LICENSE>`_

:Author:
    `Felix M. Riese <mailto:github@felixriese.de>`_

:Requirements:
    Python 3 with these `packages <requirements.txt>`_

:Citation:
    see `Citation`_ and in the `bibtex <bibliography.bib>`_ file

:Paper:
    `Link <https://doi.org/10.5194/isprs-annals-IV-1-101-2018>`_

Workflow
--------

1. Process frames from TMC to csv files:

  - `process_ir_movie.py <thermal-image-processing/process_ir_movie.py>`_
  - `process_ir_timelapse.py <thermal-image-processing/process_ir_timelapse.py>`_

2. Analyze csv-files in different zones: `analyze_ir_data.py <thermal-image-processing/analyze_ir_data.py>`_

Citation
--------

A bibtex file is available `here <bibliography.bib>`_.

**Paper**

S. Keller, F. M. Riese, J. Stötzer, P. M. Maier, and S. Hinz, “Developing
a machine learning framework for estimating soil moisture with VNIR
hyperspectral data,” ISPRS Annals of Photogrammetry, Remote Sensing and
Spatial Information Sciences, vol. IV-1, pp. 101–108, 2018.
`Link <https://doi.org/10.5194/isprs-annals-IV-1-101-2018>`_

.. code:: bibtex

    @article{keller2018developing,
        author = {Keller, Sina and Riese, Felix~M. and St\"{o}tzer, Johanna
                  and Maier, Philipp~M. and Hinz, Stefan},
        title = {{Developing a machine learning framework for estimating soil
                  moisture with VNIR hyperspectral data}},
        year = {2018},
        address = {Karlsruhe, Germany},
        journal = {ISPRS Annals of Photogrammetry, Remote Sensing and Spatial Information Sciences},
        volume = {IV-1},
        pages = {101--108},
        url = {https://www.isprs-ann-photogramm-remote-sens-spatial-inf-sci.net/IV-1/101/2018/},
        doi = {10.5194/isprs-annals-IV-1-101-2018}
    }

**Code**

F. M. Riese, “Processing Scripts for Thermal Infrared Cameras,"
doi.org/10.5281/zenodo.3576242, 2019.

.. code:: bibtex

    @misc{riese2019processing,
        author = {Riese, Felix~M.},
        title = {{Processing Scripts for Thermal Infrared Cameras}},
        year = {2019},
        DOI = {10.5281/zenodo.3576242},
        publisher = {Zenodo},
        howpublished = {\href{https://doi.org/10.5281/zenodo.3576242}{doi.org/10.5281/zenodo.3576242}}
    }
