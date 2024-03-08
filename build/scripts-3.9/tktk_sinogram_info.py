#!python

import itk
import click
import numpy as np
import matplotlib.pyplot as plt

CONTEXT_SETTINGS = dict(help_option_names=['-h', '--help'])


@click.command(context_settings=CONTEXT_SETTINGS)
@click.option('-s', 'lsino',multiple=True, help='input sinogram')
@click.option('--plot', is_flag=True, default = False, help='plot evolution of total number of counts per angle')
def sinogram_info(lsino, plot):
    if plot:
        fig, ax = plt.subplots()

    for sino in lsino:
        print(f'Informations about the sinogram {sino}')
        print('*' * 25)
        img = itk.imread(sino)

        array = itk.array_view_from_image(img)

        print(f'Size : {array.shape}')
        print(f'Spacing : {img.GetSpacing()}')
        print(f'Origin : {img.GetOrigin()}')
        print('*'*25)
        print(f'array shape : {array.shape}')
        counts_per_proj = np.sum(array, axis = (1,2))
        print(counts_per_proj.shape)
        print(f'Total counts : {counts_per_proj.sum()}')

        print(f'Mean total count over all projections : {np.mean(counts_per_proj)}')
        print(f'Min total count over all projections : {np.min(counts_per_proj)}')
        print(f'Max total count over all projections : {np.max(counts_per_proj)}')

        if plot:
            ax.plot(counts_per_proj, label=sino)



    ax.set_xlabel('proj num')
    ax.set_ylabel('total counts')
    plt.legend()
    plt.show()


if __name__ == '__main__':
    sinogram_info()
