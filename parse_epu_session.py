#!/usr/bin/python3

import os
import sys
from glob import iglob
import math
import xml.etree.ElementTree as ET

DEBUG = 0
UNKNOWN = "UNKNOWN"
nspace = {
    'so': '{http://schemas.datacontract.org/2004/07/Fei.SharedObjects}',
    'ar': '{http://schemas.microsoft.com/2003/10/Serialization/Arrays}',
    'fr': '{http://schemas.datacontract.org/2004/07/Fei.Applications.Common.Omp.Interface}',
    'tp': '{http://schemas.datacontract.org/2004/07/Fei.Types}',
    'dr': '{http://schemas.datacontract.org/2004/07/System.Drawing}',
    'app': '{http://schemas.datacontract.org/2004/07/Applications.Epu.Persistence}',
    'gen': '{http://schemas.datacontract.org/2004/07/System.Collections.Generic}',
    'coser': '{http://schemas.datacontract.org/2004/07/Fei.Applications.Common.Services}',
    'ser': '{http://schemas.microsoft.com/2003/10/Serialization/}',
    'co': '{http://schemas.datacontract.org/2004/07/Fei.Applications.Common.Types}',
}


def parseFiles(path):
    dicts = []
    with open(path) as f:
        files = f.readlines()

    for sessionFn in files:
        sessionFn = sessionFn.rstrip("\n")
        if os.path.basename(sessionFn) != "EpuSession.dm":
            continue

        sessionDir = os.path.dirname(sessionFn)
        files2 = iglob(os.path.join(sessionDir, "Images-Disc*/GridSquare*/Data/FoilHole_*_Data_*.xml"), recursive=True)
        holeFn = next(files2, None)

        print("=" * 100, "\nsession xml: ", sessionFn, "\nhole xml: ", holeFn)
        acqDict = parseSessionXml(ET.parse(sessionFn).getroot())
        if holeFn:
            acqDict2 = parseHoleXml(ET.parse(holeFn).getroot(), acqDict)
            acqDict.update(**acqDict2)
        for k, v in sorted(acqDict.items()):
            print("%s = %s" % (k, v))
        dicts.append(acqDict)

    fnOut = os.path.splitext(os.path.basename(path))[0] + ".csv"
    if os.path.exists(fnOut):
        os.remove(fnOut)
    with open(fnOut, 'a+') as ofile:
        for key in dicts[0]:
            ofile.write("%s\t" % key)
        for dic in dicts:
            ofile.write("\n")
            for key in dic:
                ofile.write("%s\t" % dic[key])
    print("\n=> Output saved to %s" % fnOut)


def parseSessionXml(root):
    acqDict = dict()
    defocusList = list()
    numExp = "./{app}Samples/{app}_items/{app}SampleXml/{app}TargetAreaTemplate/{app}DataAcquisitionAreas/{ar}m_serializationArray"
    defocus = numExp + "/*[1]/{gen}value/{app}ImageAcquisitionSettingXml/{app}Defocus/{ar}_items"
    defocus = root.find(defocus.format(**nspace))

    if defocus is None:
        # try again
        defocus = numExp + "/*[1]/{gen}value/{app}ImageAcquisitionSettingXml/{app}Defocus"
        defocus = root.find(defocus.format(**nspace))

    if defocus is not None:
        for i in defocus:
            # convert to microns
            defocusList.append(round(float(i.text) * math.pow(10, 6), 2))

    numExp = root.find(numExp.format(**nspace))
    if numExp is not None:
        numExp = numExp.attrib['{ser}Size'.format(**nspace)]
    if numExp is None:
        numExp = UNKNOWN

    acqDict["Number of exposures"] = numExp
    acqDict["Defocus list"] = sorted(defocusList)

    items = {
        'ClusteringMode': "./{app}ClusteringMode",
        'ClusteringRadius': "./{app}ClusteringRadius",
        'DoseFractionsOutputFormat': "./{app}DoseFractionsOutputFormat",
        'Name': "./{app}Name",
        'PhasePlateEnabled': "./{app}PhasePlateEnabled",
        'HoleSize': "./{app}Samples/{app}_items/{app}SampleXml/{app}FilterHolesSettings/{app}HoleSize",
        'HoleSpacing': "./{app}Samples/{app}_items/{app}SampleXml/{app}FilterHolesSettings/{app}HoleSpacing",
        'SpecimenCarrierType': "./{app}Samples/{app}_items/{app}SampleXml/{app}SpecimenCarrierType",
        'StartDateTime': "./{app}StartDateTime",
        'Autofocus recurrence': "./{app}Samples/{app}_items/{app}SampleXml/{app}TargetAreaTemplate/{app}AutoFocusArea/{app}Recurrence",
        'Autofocus distance': "./{app}Samples/{app}_items/{app}SampleXml/{app}TargetAreaTemplate/{app}AutoFocusArea/{app}RecurrenceDistance",
        'Drift recurrence': "./{app}Samples/{app}_items/{app}SampleXml/{app}TargetAreaTemplate/{app}DriftStabilizationArea/{app}Recurrence",
        'Drift threshold': "./{app}Samples/{app}_items/{app}SampleXml/{app}TargetAreaTemplate/{app}DriftStabilizationArea/{app}Threshold",
        'DelayAfterImageShift': "./{app}Samples/{app}_items/{app}SampleXml/{app}TargetAreaTemplate/{app}DelayAfterImageShift",
        'DelayAfterStageShift': "./{app}Samples/{app}_items/{app}SampleXml/{app}TargetAreaTemplate/{app}DelayAfterStageShift",
        'Detector': "./{app}Samples/{app}_items/{app}SampleXml/{app}MicroscopeSettings/KeyValuePairs/*[5]/{gen}value/{coser}Acquisition/{so}camera/{so}Name",
        'Binning': "./{app}Samples/{app}_items/{app}SampleXml/{app}MicroscopeSettings/KeyValuePairs/*[5]/{gen}value/{coser}Acquisition/{so}camera/{so}Binning/{dr}x",
        'C2Aperture': "./{app}Samples/{app}_items/{app}SampleXml/{app}MicroscopeSettings/KeyValuePairs/*[5]/{gen}value/{coser}Optics/{so}Apertures/{so}C2Aperture/{so}Diameter",
        'ProbeMode': "./{app}Samples/{app}_items/{app}SampleXml/{app}MicroscopeSettings/KeyValuePairs/*[5]/{gen}value/{coser}Optics/{so}ProbeMode",
        'SpotSize': "./{app}Samples/{app}_items/{app}SampleXml/{app}MicroscopeSettings/KeyValuePairs/*[5]/{gen}value/{coser}Optics/{so}SpotIndex",
        'BeamSize': "./{app}Samples/{app}_items/{app}SampleXml/{app}MicroscopeSettings/KeyValuePairs/*[5]/{gen}value/{coser}Optics/{so}BeamDiameter",
        'EnergySelectionSlitWidth': "./{app}Samples/{app}_items/{app}SampleXml/{app}MicroscopeSettings/KeyValuePairs/*[5]/{gen}value/{coser}Optics/{so}EnergyFilter/{so}EnergySelectionSlitWidth",
    }

    for key in items:
        try:
            acqDict[key] = root.find(items[key].format(**nspace)).text
        except AttributeError:
            if DEBUG:
                print("error with key:", key)
            acqDict[key] = UNKNOWN

    if acqDict['BeamSize'] not in [UNKNOWN, None]:
        acqDict['BeamSize'] = round(float(acqDict['BeamSize']) * math.pow(10, 6), 2)
    if acqDict['Binning'] not in [UNKNOWN, None]:
        acqDict['Binning'] = int(acqDict['Binning'])
    if acqDict['HoleSize'] not in [UNKNOWN, None]:
        acqDict['HoleSize'] = round(float(acqDict['HoleSize']) * math.pow(10, 6), 2)
    if acqDict['HoleSpacing'] not in [UNKNOWN, None]:
        acqDict['HoleSpacing'] = round(float(acqDict['HoleSpacing']) * math.pow(10, 6), 2)
    if acqDict['Autofocus distance'] not in [UNKNOWN, None]:
        acqDict['Autofocus distance'] = float(acqDict['Autofocus distance']) * math.pow(10, 6)
    if acqDict['ClusteringRadius'] not in [UNKNOWN, None]:
        acqDict['ClusteringRadius'] = float(acqDict['ClusteringRadius']) * math.pow(10, 6)

    acqDict['ObjAperture'] = UNKNOWN

    if DEBUG:
        for k, v in sorted(acqDict.items()):
            print("%s = %s" % (k, v))

    return acqDict


def parseHoleXml(root, acqDict):
    items = {
        'GunLens': "./{so}microscopeData/{so}gun/{so}GunLens",
        'Voltage': "./{so}microscopeData/{so}gun/{so}AccelerationVoltage",
        'ExtractorVoltage': "./{so}microscopeData/{so}gun/{so}ExtractorVoltage",
        'MicroscopeID': "./{so}microscopeData/{so}instrument/{so}InstrumentID",
        'PixelSpacing': "./{so}SpatialScale/{so}pixelSize/{so}x/{so}numericValue",
        'EPUversion': "./{so}microscopeData/{so}core/{so}ApplicationSoftwareVersion",
        'Magnification': "./{so}microscopeData/{so}optics/{so}TemMagnification/{so}NominalMagnification",
        'ExposureTime': "./{so}microscopeData/{so}acquisition/{so}camera/{so}ExposureTime",
    }

    for key in items:
        try:
            acqDict[key] = root.find(items[key].format(**nspace)).text
        except:
            pass

    acqDict['Mode'] = 'Linear'
    acqDict['NumSubFrames'] = 0
    acqDict['PhasePlateUsed'] = 'false'
    acqDict['Dose'] = 0
    acqDict['Voltage'] = int(acqDict['Voltage']) // 1000
    acqDict['ExtractorVoltage'] = int(float(acqDict['ExtractorVoltage']))

    # get cameraSpecificInput: ElectronCountingEnabled, SuperResolutionFactor etc.
    customDict = dict()
    keys = "./{so}microscopeData/{so}acquisition/{so}camera/{so}CameraSpecificInput/{ar}KeyValueOfstringanyType/{ar}Key"
    values = "./{so}microscopeData/{so}acquisition/{so}camera/{so}CameraSpecificInput/{ar}KeyValueOfstringanyType/{ar}Value"
    for k, v in zip(root.findall(keys.format(**nspace)), root.findall(values.format(**nspace))):
        customDict[k.text] = v.text

    # check if counting/super-res is enabled
    sr = 1.0
    if customDict.get('ElectronCountingEnabled', "false") == 'true':
        sr = float(customDict['SuperResolutionFactor'])  # 1 - counting, 2 - super-res
        acqDict['Mode'] = 'Counting' if sr == 1.0 else 'Super-resolution'

    # EPU's pixel size refers to a physical pixel, which is already multiplied by Binning factor
    acqDict['PixelSpacing'] = round(float(acqDict.get('PixelSpacing', 0)) * math.pow(10, 10) / sr, 3)

    if acqDict.get('Detector', None) == 'EF-CCD':
        elem = "./{so}microscopeData/{so}acquisition/{so}camera/{so}CameraSpecificInput/{ar}KeyValueOfstringanyType/{ar}Value/{fr}NumberOffractions"
        acqDict['NumSubFrames'] = root.find(elem.format(**nspace)).text
    else:
        # count number of DoseFractions for Falcon 3
        elem = "./{so}microscopeData/{so}acquisition/{so}camera/{so}CameraSpecificInput/{ar}KeyValueOfstringanyType/{ar}Value/{fr}DoseFractions"
        try:
            acqDict['NumSubFrames'] = len(root.find(elem.format(**nspace)))
        except:
            pass

    # get customData: Dose, DoseOnCamera, PhasePlateUsed, AppliedDefocus
    customDict = dict()
    keys = "./{so}CustomData/{ar}KeyValueOfstringanyType/{ar}Key"
    values = "./{so}CustomData/{ar}KeyValueOfstringanyType/{ar}Value"
    for k, v in zip(root.findall(keys.format(**nspace)), root.findall(values.format(**nspace))):
        customDict[k.text] = v.text

    if 'Detectors[BM-Falcon].EerGainReference' in customDict:
        acqDict['NumSubFrames'] = int(int(float(acqDict['ExposureTime']) * float(customDict.get('Detectors[BM-Falcon].FrameRate', 0))) * 31 / 32)
        acqDict['Mode'] = "EER"
        acqDict['GainReference'] = os.path.basename(customDict['Detectors[BM-Falcon].EerGainReference'])
    elif 'Detectors[EF-Falcon].EerGainReference' in customDict:
        acqDict['NumSubFrames'] = int(int(float(acqDict['ExposureTime']) * float(customDict.get('Detectors[EF-Falcon].FrameRate'))) * 31 / 32)
        acqDict['Mode'] = "EER"
        acqDict['GainReference'] = os.path.basename(customDict['Detectors[EF-Falcon].EerGainReference'])
    #if 'AppliedDefocus' in customDict:
    #    acqDict['AppliedDefocus'] = float(customDict['AppliedDefocus']) * math.pow(10, 6)
    if 'Dose' in customDict:
        acqDict['Dose'] = float(customDict['Dose']) * math.pow(10, -20)
    if 'PhasePlateUsed' in customDict:
        acqDict['PhasePlateUsed'] = customDict['PhasePlateUsed']
    if 'Aperture[C2].Name' in customDict:
        acqDict['C2Aperture'] = customDict['Aperture[C2].Name']
    if 'Aperture[OBJ].Name' in customDict:
        acqDict['ObjAperture'] = customDict['Aperture[OBJ].Name']

        if customDict['PhasePlateUsed'] == 'true':
            acqDict['PhasePlateNumber'] = customDict['PhasePlateApertureName'].split(" ")[-1]
            acqDict['PhasePlatePosition'] = customDict['PhasePlatePosition']

    if 'DoseOnCamera' in customDict:
        acqDict['DoseOnCamera'] = customDict['DoseOnCamera']

    calcDose(acqDict)

    if DEBUG:
        for k, v in sorted(acqDict.items()):
            print("%s = %s" % (k, v))

    return acqDict


def calcDose(acqDict):
    """ Calculate dose rate per unbinned px per s. """
    numFr = int(acqDict['NumSubFrames'])
    dose_total = float(acqDict['Dose'])  # e/A^2
    exp = float(acqDict['ExposureTime'])  # s

    if acqDict['Mode'] == 'Super-resolution':
        pix = 2 * float(acqDict['PixelSpacing']) / int(acqDict['Binning'])  # A
    else:
        pix = float(acqDict['PixelSpacing']) / int(acqDict['Binning'])  # A

    if numFr:  # not 0
        dose_per_frame = dose_total / numFr  # e/A^2/frame
    else:
        dose_per_frame = 0
    dose_on_camera = dose_total * math.pow(pix, 2) / exp  # e/unbinned_px/s

    acqDict['DosePerFrame'] = round(dose_per_frame, 4)
    acqDict['DoseOnCamera'] = round(dose_on_camera, 2)
    acqDict['ExposureTime'] = round(exp, 2)
    acqDict['Dose'] = round(dose_total, 2)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        parseFiles(sys.argv[1])
        print()
    else:
        raise ValueError(f"Unrecognized input, please use: {os.path.basename(sys.argv[0])} filename")
