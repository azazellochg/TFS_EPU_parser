# TFS_EPU_parser

A simple Python 3 script to parse EPU session files. No dependencies or installation is required!

This script can be useful to analyze EPU parameters from sessions of different facility users. It will analyze **EpuSession.dm** (one per session) and a FoilHole data xml file (from a first found movie), then create a CSV table.

How to use
----------

1) Locate *EpuSession.dm* files. You can use **get_files.sh** as an example script to find all files modified in 2023. This script will output a list of file paths (see **examples/scope0**).
2) Run the main script:

   ``python3 parse_epu_session.py /path/to/scope0``

   It will generate **scope0.csv** which you can see in examples folder.

3) PROFIT!! You are done. You can analyse the output CSV in any way you like with downstream tools.


CSV columns
-----------

* Autofocus distance (um)
* Autofocus recurrence
* BeamSize (um)
* Binning
* C2Aperture (um)
* ClusteringMode
* ClusteringRadius (um)
* Defocus list (um)
* DelayAfterImageShift (s)
* DelayAfterStageShift (s)
* Detector
* Dose (e/A^2)
* DoseFractionsOutputFormat
* DoseOnCamera (e/unbinned_px/s)
* DosePerFrame (e/A^2/frame)
* Drift recurrence
* Drift threshold (m/s)
* EnergySelectionSlitWidth (eV)
* EPUversion
* ExposureTime (s)
* ExtractorVoltage (V)
* GunLens
* HoleSize (um)
* HoleSpacing (um)
* Magnification
* MicroscopeID
* Mode
* Name
* Number of exposures (per hole)
* NumSubFrames
* ObjAperture (um)
* PhasePlateEnabled
* PhasePlateUsed
* PixelSpacing (A)
* ProbeMode
* SpecimenCarrierType
* SpotSize
* StartDateTime
* Voltage (kV)

![image](https://github.com/azazellochg/TFS_EPU_parser/assets/6952870/ceeb41ae-b9cc-4ae9-bd49-6216c58bb013)
![image](https://github.com/azazellochg/TFS_EPU_parser/assets/6952870/279ea58f-03a4-4aec-a3c9-7462ffe2e31b)

