.. figure:: docs/source/figures/logo.svg
    :width: 200

=============================================
``ixdat``: The In-situ Experimental Data Tool
=============================================

With ``ixdat``, you can import, combine, and export complex experimental datasets
as simply as::

    ec = Measurement.read_set("awesome_EC_data", reader="biologic")
    ec.plot_measurement()

    ms = Measurement.read("2021-03-30 16_59_35 MS data.tsv", reader="zilien")
    ms.plot_measurement()

    ecms = ec + ms
    ecms.plot_measurement()

    ecms.export("my_combined_data.csv")

Output:

.. figure:: docs/source/figures/ixdat_example_figures.png
    :width: 700

    In-situ experimental data made easy

Or rather, than exporting, you can take advantage of ``ixdat``'s powerful analysis
tools and database backends to be a one-stop tool from messy raw data to public
repository accompanying your breakthrough publication and advancing our field.

About
-----

``ixdat`` provides a powerful **object-oriented** interface to experimental data, especially in-situ experimental data for which it is of interest to combine data obtained simultaneously from multiple techniques.

Documentation is at https://ixdat.readthedocs.io

In addition to a **pluggable** parser interface for importing your data format, ``ixdat`` it also includes
pluggable exporters and plotters, as well as a database interface. A relational model of experimental data is
thought into every level.

.. list-table:: Techniques and Readers
   :widths: 20 15 50
   :header-rows: 1


   * - Measurement technique
     - Status
     - Readers
   * - Electrochemistry
     - Released
     - - biologic: .mpt files from Biologic's EC-Lab software
       - autolab: ascii files from AutoLab's NOVA software
       - ivium: .txt files from Ivium's IviumSoft software
   * - Mass Spectrometry
     - Released
     - - pfeiffer: .dat files from Pfeiffer Vacuum's PVMassSpec software
       - cinfdata: text export from DTU Physics' cinfdata system
       - zilien: .tsv files from Spectro Inlets' Zilien software
   * - Electrochemistry - Mass Spectrometry
     - Released
     - - zilien: .tsv files from Spectro Inlets' Zilien software
       - EC_MS: .pkl files from the legacy EC_MS python package
   * - Spectroelectrochemistry
     - Released
     - - msrh_sec: .csv file sets from Imperial College London's SEC system
   * - X-ray photoelectron spectroscopy (XPS)
     - Future
     -
   * - X-ray diffraction (XRD)
     - Future
     -
   * - Low-Energy Ion Scattering (LEIS)
     - Future
     -

Tutorials are described at https://ixdat.readthedocs.io/en/latest/tutorials.html

Installation
------------

To use ``ixdat``, you need to have python installed. We recommend
`Anaconda python <https://www.anaconda.com/products/individual>`_.

To install ``ixdat``, just type in your terminal or Anaconda prompt::

    $ pip install ixdat

And hit enter.

``ixdat`` is under development, and to make use of the newest features,
you may need to upgrade to the latest version. This is also easy. Just type::

    $ pip install --upgrade ixdat


Article repositories
--------------------

``ixdat`` is shown in practice in a growing number of open repositories of data and analysis
for academic publications:

- Tracking oxygen atoms in electrochemical CO oxidation - Part II: Lattice oxygen reactivity in oxides of Pt and Ir

  - Article: https://doi.org/10.1016/j.electacta.2021.137844
  - Repository: https://github.com/ScottSoren/pyCOox_public

- Dynamic Interfacial Reaction Rates from Electrochemistry - Mass Spectrometry

  - Article: https://doi.org/10.1021/acs.analchem.1c00110
  - Repository: https://github.com/kkrempl/Dynamic-Interfacial-Reaction-Rates


Join us
-------

`ixdat`` is free and open source software and we welcome input and new collaborators. Please help us improve!

Contact us (sbscott@ic.ac.uk) or just
`get started developing <https://ixdat.readthedocs.io/en/latest/developing.html>`_.