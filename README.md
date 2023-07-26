# TFS_EPU_parser

A simple Python 3 script to parse EPU session files.

This script can be useful to analyze EPU parameters from sessions of different facility users. It will analyze **EpuSession.dm** (one per session) and a FoilHole data xml file (from a first found movie), then create a CSV table.

How to use
----------

1) Locate *EpuSession.dm* files. You can use **get_files.sh** as an example script to find all files modified in 2023. This script will output a list of file paths (see **examples/scope0**).
2) Run the main script:

.. code-block:: python

    python3 parse_epu_session.py /path/to/scope0

It will generate **scope0.csv** which you can see in examples folder.

3) PROFIT!! You are done. You can analyse the output CSV in any way you like with downstream tools.


CSV columns
-----------

* Autofocus distance
* Autofocus recurrence
* BeamSize
* Binning
* C2Aperture
* ClusteringMode
* ClusteringRadius
* Defocus list
* DelayAfterImageShift
* DelayAfterStageShift
* Detector
* Dose
* DoseFractionsOutputFormat
* DoseOnCamera
* DosePerFrame
* Drift recurrence
* Drift threshold
* EnergySelectionSlitWidth
* EPUversion
* ExposureTime
* ExtractorVoltage
* GunLens
* HoleSize
* HoleSpacing
* Magnification
* MicroscopeID
* Mode
* Name
* Number of exposures
* NumSubFrames
* ObjAperture
* PhasePlateEnabled
* PhasePlateUsed
* PixelSpacing
* ProbeMode
* SpecimenCarrierType
* SpotSize
* StartDateTime
* Voltage

![image](https://github.com/azazellochg/TFS_EPU_parser/assets/6952870/ceeb41ae-b9cc-4ae9-bd49-6216c58bb013)
![image](https://github.com/azazellochg/TFS_EPU_parser/assets/6952870/279ea58f-03a4-4aec-a3c9-7462ffe2e31b)

