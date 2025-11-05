#!/usr/bin/env python3

import setuptools

install_requires = [
        "itk",
        "numpy",
        "click"
        ]

setuptools.setup(
    name="TKTK",
    version="0.1",
    author="Theo Kaprelian",
    author_email="theo.kaprelian@creatis.insa-lyon.fr",
    description="Easy to use ToolKit for Toolkits (basic itk, rtk ... scripts)",
    url="",
    packages=setuptools.find_packages(),
    install_requires=install_requires,
    include_package_data=True,
    scripts=[
        'tktk_ct_to_attmap.py',
        'tktk_multiply_itk_image.py',
        'tktk_resample_itk_image.py',
        'tktk_sum_itk_images.py',
        'tktk_total_count_itk_image.py',
        'tktk_sinogram_info.py',
        'tktk_img_plot.py',
        'tktk_threshold.py',
        'tktk_center_image.py',
        'tktk_rename_itk_image.py',
        'tktk_scatter_correction_dew.py',
        'tktk_scatter_correction_tew.py',
        'tktk_convert.py',
        'tktk_image_info.py',
        'tktk_split.py',
        'tktk_ct_recons_to_rtk_system.py',
        'tktk_merge.py',
        'tktk_normalize.py',
        'tktk_conv2d_params.py',
        'tktk_center_difference.py',
        'tktk_get_volume_from_labels.py',
        'tktk_activity_decay.py',
        'tktk_decay_correction.py',
        'tktk_make_src_from_labels.py',
        'tktk_3d_fwhm.py',
        'tktk_combine_masks.py',
        'tktk_unit_converter.py',
        'tktk_convert_dtypes.py',
        'tktk_pad.py',
        'tktk_plot_activity_per_organs.py',
        'tktk_make_geom_from_dicom.py',
        'tktk_add_projs.py',
        'tktk_merge_projs.py',
        'tktk_make_psf.py',
        'tktk_convolve.py',
        "tktk_tumour_delineation_threshold.py",
        'tktk_merge_4d.py',
        'tktk_get_ct_infos_from_dicoms.py',
        'tktk_segmentation_confidence_connected.py',
        'tktk_combine_labels.py',
        "tktk_fft3d.py",
        "tktk_copy_information_itk.py",
        "tktk_region_growing_delineation.py"
        ]
    )

