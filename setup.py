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
        'tktk_convert.py',
        'tktk_image_info.py',
        'tktk_split.py',
        'tktk_ct_recons_to_rtk_system.py'
        ]
    )

