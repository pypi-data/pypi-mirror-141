.. role:: raw-html-m2r(raw)
   :format: html


:raw-html-m2r:`<img alt="KIPET" src="branding/kipetlogo_full.svg" height="60">`
===================================================================================


.. image:: https://img.shields.io/github/license/salvadorgarciamunoz/kipet
   :target: https://github.com/salvadorgarciamunoz/kipet/blob/master/LICENSE
   :alt: 


.. image:: https://img.shields.io/github/last-commit/salvadorgarciamunoz/kipet
   :target: https://github.com/salvadorgarciamunoz/kipet/
   :alt: 


.. image:: https://img.shields.io/pypi/wheel/kipet
   :target: https://pypi.org/manage/project/kipet/release/0.1.1/
   :alt: 


KIPET is a Python package designed to simulate, and estimate parameters from 
chemical reaction systems through the use of maximum likelihood principles,
large-scale nonlinear programming and discretization methods. 


* **Documentation:** - https://kipet.readthedocs.io
* **Examples and Tutorials** - https://github.com/kwmcbride/kipet_examples
* **Source code:** - https://github.com/salvadorgarciamunoz/kipet
* **Bug reports:** - https://github.com/salvadorgarciamunoz/kipet/issues

It has the following functionality:


* Simulate a reactive system described with DAEs
* Solve the DAE system with collocation methods
* Pre-process data
* Estimate variances of noise from the model and measurements
* Estimate kinetic parameters from spectra or concentration data across 1 or 
  multiple experiments with different conditions
* Estimate confidence intervals of the estimated parameters
* Able to estimate variances and parameters for problems where there is dosing / inputs into the system
* Provide a set of tools for estimability analysis
* Allows for wavelength selection of most informative wavelengths from a dataset
* Visualize results

:raw-html-m2r:`<br>`

Installation
------------

There are many options for installing KIPET.

:raw-html-m2r:`<br>`

PyPi
^^^^


.. image:: https://img.shields.io/badge/Install%20with-pip-green
   :target: 
   :alt: 


.. image:: https://img.shields.io/pypi/v/kipet.svg?style=flat
   :target: https://pypi.org/pypi/kipet/
   :alt: 

:raw-html-m2r:`<br>`

A packaged version of KIPET can be installed using:

.. code-block::

   pip install kipet


If you run into errors when installing KIPET using pip, try installing the following packages beforehand:

.. code-block::

   pip install Cython numpy six
   pip install kipet


:raw-html-m2r:`<br>`

Anaconda
^^^^^^^^


.. image:: https://anaconda.org/kwmcbride/kipet/badges/installer/conda.svg
   :target: 
   :alt: 


.. image:: https://anaconda.org/kwmcbride/kipet/badges/version.svg
   :target: https://anaconda.org/kwmcbride/kipet
   :alt: Anaconda-Server Badge


.. image:: https://anaconda.org/kwmcbride/kipet/badges/latest_release_date.svg
   :target: 
   :alt: 


.. image:: https://anaconda.org/kwmcbride/kipet/badges/platforms.svg
   :target: 
   :alt: 


Finally, if you are using Anaconda, KIPET can be installed using:

.. code-block::

   conda install -c kwmcbride kipet


The anaconda packages have the benefit of including pynumero ready to go, which is needed for some of the methods included in KIPET. You will need to compile these on your own if you choose to install KIPET using a different method. See the `pynumero readme <https://github.com/Pyomo/pyomo/tree/master/pyomo/contrib/pynumero>`_ for more information. Otherwise, you can also use `k_aug <https://github.com/dthierry/k_aug>`_ for these methods as well. 

:raw-html-m2r:`<br>`

Poetry
^^^^^^

You may also install KIPET with poetry:

.. code-block::

   poetry add kipet


:raw-html-m2r:`<br>`

GitHub
^^^^^^

Additionally, KIPET may be installed directly from the repository (for example, if using poetry, simply install the desired branch (#branch) in the following manner):

.. code-block::

   poetry add git+http://github.com/salvadorgarciamunoz/kipet#master


Naturally you can simply clone or download the repository if you wish.

:raw-html-m2r:`<br>`

License
-------

GPL-3

Authors
-------

.. code-block::

   - Kevin McBride - Carnegie Mellon University
   - Kuan-Han Lin - Carnegie Mellon University
   - Christina Schenk - Basque Center for Applied Mathematics
   - Michael Short - University of Surrey
   - Jose Santiago Rodriguez - Purdue University
   - David M. Thierry - Carnegie Mellon University
   - Salvador García-Muñoz - Eli Lilly
   - Lorenz T. Biegler - Carnegie Mellon University


Please cite
-----------


* 
  C. Schenk, M. Short, J.S. Rodriguez, D. Thierry, L.T. Biegler, S. García-Muñoz, W. Chen (2020)
  Introducing KIPET: A novel open-source software package for kinetic parameter estimation from experimental datasets including spectra, Computers & Chemical Engineering, 134, 106716. https://doi.org/10.1016/j.compchemeng.2019.106716

* 
  M. Short, L.T. Biegler, S. García-Muñoz, W. Chen (2020)
  Estimating variances and kinetic parameters from spectra across multiple datasets using KIPET, Chemometrics and Intelligent Laboratory Systems, https://doi.org/10.1016/j.chemolab.2020.104012

* 
  M. Short, C. Schenk, D. Thierry, J.S. Rodriguez, L.T. Biegler, S. García-Muñoz (2019)
  KIPET–An Open-Source Kinetic Parameter Estimation Toolkit, Computer Aided Chemical Engineering, 47, 299-304.
