.. _tutorials:

=========
Tutorials
=========

``ixdat`` has a growing number of tutorials and examples available, addressing different steps in your ``ixdat`` workflow.




Getting data in and out
-----------------------

In ``ixdat`` your data is imported with a ``reader`` (specific to your data format) into a ``Measurement`` object and can then be plotted and/or 
exported into a format of your choice. You can figure out how in this tutorial: 


Techniques
----------

Each technique comes with its own methods developed specifically for the types of data handling that are of interest. For example, the electrochemistry technique subclass comes with a subclass ``CyclicVoltammogram`` which allows you to select your data according to cycles, the mass spectrometry technique subclass comes with a method to calibrate the MS signals, and the spectroelectrochemistry technique subclass with a method to set a reference spectrum.
The tutorials for the technique-specific methods are still work in progress - please, bear with us - you can find all the ones already available below.

As an open source project, ``ixdat`` is always happy to get contributions from the users, e.g. in form of new techniques.

.. list-table::
   :widths: 30 30
   :header-rows: 1

   * - Technique
     - Tutorials
   * - EC
     - :ref:`ec_tutorials`
   * - MS
     -
   * - EC-MS
     - :ref:`ecms_tutorial`
   * - SEC
     - :ref:`sec_tutorial`
   * - XRD
     -

Advanced data handling
----------------------

While the existing technique subclasses allow for a wide range of general and technique specific data treatment, sometimes this is not enough for your
individual needs. Luckily, ``ixdat`` also allows for direct data handling in array-type form. How to access data in this way is demonstrated in the tutorials on advanced data handling.

In the future there will also be a tutorial on data manipulation and treatment including how to cut and select different sections of your data, as well as
an introduction to calibration.

=====================
The jupyter notebooks
=====================

All tutorials linked to above are also available as fully interactive Jupyter notebooks in the ixdat Tutorials repository:
https://github.com/ixdat/tutorials/


.. _readers_tutorial:

Readers
-------
https://github.com/ixdat/tutorials/blob/main/L1_basic_concepts/01_Readers.ipynb

.. toctree::
    :maxdepth: 1

    tutorials_repo/L1_basic_concepts/01_Readers.ipynb


.. _ec_tutorials:

Electrochemistry
----------------
https://github.com/ixdat/tutorials/blob/main/L2_techniques/electrochemistry/02_comparing_cycles.ipynb

.. toctree::
    :maxdepth: 1

    tutorials_repo/L2_techniques/electrochemistry/02_comparing_cycles


.. _ecms_tutorial:

EC-MS
-----
https://github.com/ixdat/tutorials/blob/main/L2_techniques/ec_ms_quantification/EC-MS_ixdat_tutorial.ipynb

.. toctree::
    :maxdepth: 1

    tutorials_repo/ec_ms_quantification/EC-MS_ixdat_tutorial

.. _sec_tutorial:

spectroelectrochemistry
-----------------------
https://github.com/ixdat/tutorials/blob/main/L2_techniques/spectroelectrochemistry/spectroelectrochemistry_demo.ipynb

.. toctree::
    :maxdepth: 1

    tutorials_repo/L2_techniques/spectroelectrochemistry/spectroelectrochemistry_demo


.. _data_tutorial:

Data concepts
-------------
https://github.com/ixdat/tutorials/blob/main/L3_data_structure/01_reading_and_using_data.ipynb

.. toctree::
    :maxdepth: 1

    tutorials_repo/L3_data_structure/01_reading_and_using_data


This repository is a bit of a mess at the moment, apologies, but the tutorials themselves are
not bad, if we may say so ourselves. More are in progress.


Development scripts
-------------------
For developers:

The basics of importing and plotting from each reader are demonstrated in
the **development_scripts/reader_testers** folder of the repository:
hhttps://github.com/ixdat/ixdat/tree/main/development_scripts/reader_demonstrators