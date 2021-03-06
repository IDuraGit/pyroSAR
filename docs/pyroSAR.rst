Drivers
=======

.. automodule:: pyroSAR.drivers
    :members:
    :undoc-members:
    :show-inheritance:

    .. rubric:: classes

    .. autosummary::
        :nosignatures:

        ID
        CEOS_PSR
        CEOS_ERS
        ESA
        SAFE
        TSX
        Archive

    .. rubric:: functions

    .. autosummary::
        :nosignatures:

        identify
        identify_many
        filter_processed
        findfiles
        getFileObj
        parse_date

SNAP Processing
===============

.. automodule:: pyroSAR.snap.util
    :members:
    :undoc-members:
    :show-inheritance:

GAMMA Processing
================

.. automodule:: pyroSAR.gamma
    :members: geocode, convert2gamma, ISPPar, process, ovs, S1_deburst, correctOSV, multilook, par2hdr
    :undoc-members:
    :show-inheritance:

    .. autosummary::
        :nosignatures:

        convert2gamma
        correctOSV
        geocode
        ISPPar
        multilook
        ovs
        process
        S1_deburst
        par2hdr

SRTM tools
----------

.. automodule:: pyroSAR.gamma.srtm
    :members: dem_autocreate, dempar, fill, hgt, hgt_collect, makeSRTM, mosaic, swap
    :undoc-members:
    :show-inheritance:

    .. autosummary::
        :nosignatures:

        dem_autocreate
        dempar
        fill
        hgt
        hgt_collect
        makeSRTM
        mosaic
        swap

GAMMA Command API
-----------------

This is an attempt to make it easier to execute Gamma commands by offering automatically parsed Python functions.
Thus, instead of executing the command via shell:

.. code-block:: shell

    offset_fit offs ccp off.par coffs - 0.15 3 0 > offset_fit.log

one can wrap it in a Python script:

.. code-block:: python

    import os
    from pyroSAR.gamma.api import isp

    workdir = '/data/gamma_workdir'

    parameters = {'offs': os.path.join(workdir, 'offs'),
                  'ccp': os.path.join(workdir, 'ccp'),
                  'OFF_par': os.path.join(workdir, 'off.par'),
                  'coffs': os.path.join(workdir, 'coffs'),
                  'thres': 0.15,
                  'npoly': 3,
                  'interact_flag': 0,
                  'logpath': workdir}

    isp.offset_fit(**parameters)

A file `offset_fit.log` containing the output of the command is written in both cases. Any parameters, which should
not be written and need to be set to - in the shell can be omitted in the Python call since all optional parameters
of the functions are already defined with '-' as a default.
The documentation can be called like with any Python function:

.. code-block:: python

    from pyroSAR.gamma.api import isp
    help(isp.offset_fit)

Parser Documentation
********************

.. automodule:: pyroSAR.gamma.parser
    :members:
    :undoc-members:
    :show-inheritance:

API Demo
********

This is a demonstration of an output script as generated automatically by function
:func:`~pyroSAR.gamma.parser.parse_module` for the Gamma module `ISP`.
Within each function, the command name and all parameters are passed to function
:func:`~pyroSAR.gamma.process`, which converts all input to str and then calls the command via the
:mod:`subprocess` module.

.. automodule:: pyroSAR.gamma.parser_demo
    :members:
    :undoc-members:
    :show-inheritance:

Sentinel-1 Tools
================

.. automodule:: pyroSAR.S1.auxil
    :members: OSV, removeGRDBorderNoise
    :undoc-members:
    :show-inheritance:

Auxiliary Data Tools
====================

.. automodule:: pyroSAR.auxdata
    :members: dem_autoload
    :undoc-members:
    :show-inheritance:

Datacube Tools
==============
.. automodule:: pyroSAR.datacube_util
    :members:
    :undoc-members:
    :show-inheritance:

Ancillary Functions
===================

.. automodule:: pyroSAR.ancillary
    :members:
    :undoc-members:
    :show-inheritance:

    .. autosummary::
        :nosignatures:

        find_datasets
        groupby
        groupbyTime
        parse_datasetname
        seconds
