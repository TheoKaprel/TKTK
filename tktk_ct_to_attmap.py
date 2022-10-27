#!/usr/bin/env python3

import itk
import click
import numpy as np
import sys


CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])
@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('--ct', help = 'Input ct image in Hounsfield Units (HU)', required = True)
@click.option('-o', '--output', 'output_attmap_fn', required = True, help = "Output attenuation map filename")
@click.option('--rn','radionuclide', help = 'Radionuclide : Tc99m, Lu77', default = 'Tc99m')
def convert_ct_to_attmap(ct, output_attmap_fn, radionuclide):
    """

    Converts a CT (HU) into an attenuation map (in mm^-1)

    """

    ### ctCoeff = attenuation coefficients for water and bone for mean energy of the X-ray used for CT in mm-1
    ctCoeff = 1/10 * np.array([0.2068007,0.57384408])

    ### spectCoeff = attenuation coefficients for air, water and bone for all targeted energies of the SPECT in mm-1
    # Values from : https://physics.nist.gov/PhysRefData/XrayMassCoef/tab4.html
    if radionuclide.lower()=='tc99m':
        # One Energy peak : 140.5 keV
        spectCoeff = 1/10 * np.array([0.0001668,0.15459051,0.28497715])
        weightPeak = [1]
    elif radionuclide.lower()=='lu77':
        # Two Energy peaks:  112.95 keV (weight=0.062) and 208.37 keV (weight=0.104)
        spectCoeff = 1/10 * np.array([0.00017856, 0.16529103, 0.31934538, 0.00014657, 0.13597229, 0.24070651])
        weightPeak = [0.062, 0.104]


    ctImage = itk.imread(ct)

    if ctImage.GetImageDimension() != 3:
        print("Image dimension (" + str(ctImage.GetImageDimension()) + ") is not 3")
        sys.exit(1)
    if ctCoeff is None:
        print("ctCoeff is mandatory")
        sys.exit(1)
    elif len(ctCoeff) != 2:
        print("ctCoeff size (" + str(len(ctCoeff)) + ") is not 2")
        sys.exit(1)
    if weightPeak is None:
        weightPeak = [1]
    nbPeak = len(weightPeak)
    if spectCoeff is None:
        print("spectCoeff is mandatory")
        sys.exit(1)
    elif len(spectCoeff) != 3 * nbPeak:
        print("ctCoeff size (" + str(len(spectCoeff)) + ") is not 3*nbPeak (" + str(3 * nbPeak) + ")")
        sys.exit(1)


    ctArray = itk.array_from_image(ctImage)
    ctPositiveValueIndex = np.where(ctArray > 0)
    ctNegativeValueIndex = np.where(ctArray < 0)
    attenuation = np.zeros(ctArray.shape)
    for i in range(nbPeak):
        attenuationTemp = np.zeros(ctArray.shape)
        attenuationTemp[ctNegativeValueIndex] = spectCoeff[3*i+1] + (spectCoeff[3*i+1] - spectCoeff[3*i])/1000.0 *ctArray[ctNegativeValueIndex]
        attenuationTemp[ctPositiveValueIndex] = spectCoeff[3*i+1] + ctCoeff[0]/(ctCoeff[1]-ctCoeff[0])*(spectCoeff[3*i+2] - spectCoeff[3*i+1])/1000.0 *ctArray[ctPositiveValueIndex]
        attenuation = attenuation + weightPeak[i]*attenuationTemp
    attenuation[attenuation < 0] = 0
    attenuationImage = itk.image_from_array(attenuation)
    attenuationImage.CopyInformation(ctImage)

    itk.imwrite(attenuationImage, output_attmap_fn)
    print(f'Output attenuation map in {output_attmap_fn}')


if __name__=='__main__':
    convert_ct_to_attmap()
