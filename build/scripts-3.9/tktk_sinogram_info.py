#!/export/home/tkaprelian/Software/miniconda3/bin/python

import itk
import click
import numpy as np

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-s', 'sino', help='input sinogram')
def sinogram_info(sino):
    print(f'Informations about the sinogram {sino}')
    print('*' * 25)
    img = itk.imread(sino)

    array = itk.array_view_from_image(img)

    print(f'Size : {array.shape}')
    print(f'Spacing : {img.GetSpacing()}')
    print(f'Origin : {img.GetOrigin()}')
    print('*'*25)

    counts_per_proj = np.sum(array, axis = (1,2))
    print(counts_per_proj.shape)
    print(f'Total counts : {counts_per_proj.sum()}')

    print(f'Mean total count over all projections : {np.mean(counts_per_proj)}')
    print(f'Min total count over all projections : {np.min(counts_per_proj)}')
    print(f'Max total count over all projections : {np.max(counts_per_proj)}')


if __name__ == '__main__':
    sinogram_info()
