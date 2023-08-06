import itertools as it
import io 
import numpy as np
import argparse
Data = np.ndarray
import  matplotlib as mpl
mpl.rcParams['toolbar'] = 'None'
from matplotlib import pyplot as plt
from matplotlib.widgets import Slider, TextBox, Button


def main() -> None:
    '''This function is called when the script is explicitly executed'''
    # Parse Arguments given by the user
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--inputfile",    help="Input *.dat filename")
    parser.add_argument("-o", "--outputfile",   help="Output filename")
    args = parser.parse_args()
    if run(
            inputfile  = args.inputfile,
            outputfile = args.outputfile,
            ):
        parser.print_help()
    

def run(
        inputfile: str,
        outputfile:str,
        ):
    if not inputfile:
        return 1
    if not outputfile:
        outputfile = f'{inputfile}.acr.dat'
        print(f'No outputfile specified. Using {outputfile}.') 
    data = read(inputfile)
    data, values = correct_angle(data)
    print(values)
    if values:
        write(data, values, outputfile)


def read(
        filename: str,
        encoding: str = 'utf8',
        ):
    with open(filename, 'r') as file:
        lines = file.read()
    lines = lines.strip().split('\n')
    lines = it.dropwhile(lambda line: not '[Data]' in line, lines)
    next(lines)                 # [Data]
    columns = next(lines)       # columns header
    columns = columns.split(',')
    indexes, names = list(zip(*[
            (idx, name)
            for idx, name in enumerate(columns)
            if name in [
                'Temperature (K)', 
                'Magnetic Field (Oe)', 
                'Rotation Angle (deg)', 
                'DC Moment Fixed Ctr (emu)',
                'DC Moment Err Fixed Ctr (emu)',
                'DC Moment Free Ctr (emu)',
                'DC Moment Err Free Ctr (emu)',
                ] 
            ]))
    data = np.genfromtxt(
        io.StringIO('\n'.join(lines)), 
        comments = '#', 
        delimiter = ',', 
        deletechars = '',
        replace_space = ' ',
        #names = columns,
        names = names,
        usecols = indexes,
        encoding = encoding,
        )
    return data

def correct_angle(data: Data) -> Data:
    a = 'Rotation Angle (deg)'
    M = 'DC Moment Free Ctr (emu)'
    b = 'backlash (deg)'
    s = 'slip'
    p = 'phase (deg)'
    T = 'Temperature (K)'
    H = 'Magnetic Field (Oe)'
    d = {}
    d['figure_x'] = 12
    d['figure_y'] = 5
    d['padding_x'] = .5/d['figure_x']
    d['padding_y'] = .5/d['figure_y']
    d['polar_y'] = .8 
    d['polar_x'] = d['polar_y'] / d['figure_x'] * d['figure_y']
    d['boxes_x'] = d['polar_x']
    d['boxes_y'] = 1 - d['polar_y']
    d['kartesian_x'] = 1 - d['polar_x']
    d['kartesian_y'] = .9 
    d['buttons_x'] = .5 * d['kartesian_x']
    d['buttons_y'] = 1 - d['kartesian_y']
    d['text_x'] = .5 * d['kartesian_x']
    d['text_y'] = 1 - d['kartesian_y']

    fig = plt.figure('ACR – Angle Correction for Rotators',
            figsize=(12,5),
            )
    fig.canvas.toolbar_visible = False
    fig.text(d['boxes_x'], .5 * d['text_y'], f'\
            $T\in[\
            {data[T].min():.4g}\,$K$, {data[T].max():.4g}\,$K$]$ \
            $H\in[\
            {data[H].min():.4g}\,$Oe$, {data[H].max():.4g}\,$Oe$]$',
            ha='left',
            va='center',
            )
    ax1 = fig.add_axes((
        d['padding_x'],
        d['boxes_y'] +   d['padding_y'],
        d['polar_x'] - 2*d['padding_x'],
        d['polar_y'] - 2*d['padding_y']
        ), 
        projection='polar',
        )
    ax1.set_rlabel_position(90)
    ax1.set_rticks([])
    ax1.set_theta_zero_location("N")
    ax2 = fig.add_axes((
        d['polar_x'] + 2 * d['padding_x'],
        d['text_y'] + d['padding_y'],
        d['kartesian_x'] - 3 * d['padding_x'],
        d['kartesian_y'] - 2 * d['padding_y']
        ))
    ax2.set_xlim((0,360))
    ax2.set_xticks((0,30,45,60,90,120,135,150,180,210,225,240,270,300,315,330,360))
    ax2.grid(True, axis='x')
    ax2.set_xlabel(a)
    ax2.set_ylabel(M, rotation='vertical')
    sliders = {}
    boxes = {}
    values = {}
    for key, height, valinit, valmin, valmax in (
            (b, 3/3, 0, 0, 20,),
            (s, 2/3, 1, .9, 1.1,),
            (p, 1/3, 0, -90, 90,),
            ):
        fig.text(
                1/3 * d['boxes_x'],
                height * d['boxes_y'],
                key,
                ha='right',
                va='center',
                )
        sliders[key] = Slider(
                ax = fig.add_axes((
                    1/3 * d['boxes_x'] + .2 * d['padding_x'],
                    height * d['boxes_y'] - .2 * d['padding_y'],
                    1/3 * d['boxes_x'] - .4 * d['padding_x'],
                    .4 * d['padding_y']
                    )),
                label='',
                valinit=valinit,
                valmin=valmin,
                valmax=valmax,
                orientation='horizontal',
                )
        sliders[key].valtext.set_visible(False)
        boxes[key] = TextBox(
                ax = fig.add_axes((
                2/3 * d['boxes_x'] - .1 * d['padding_x'],
                height * d['boxes_y'] - .2 * d['padding_y'], 
                1/3 * d['boxes_x'] - .9 * d['padding_x'], 
                .4 * d['padding_y']
                    )),
                label='',
                initial=str(valinit),
                color='w',
                )
        boxes[key].ax.set_frame_on(False)
    reset_button = Button(
            ax = fig.add_axes((
                d['boxes_x'] + d['text_x'] + d['buttons_x']- 5.5 * d['padding_x'],
                .5 * d['buttons_y'] - .25 * d['padding_y'],
                2 * d['padding_x'],
                .5 * d['padding_y']
                )),
            label = 'Reset',
            color = 'w',
            )
    def reset_button_click(event):
        for slider in sliders.values():
            slider.reset()
    reset_button.on_clicked(reset_button_click)

    save_button = Button(
            ax = fig.add_axes((
                d['boxes_x'] + d['text_x'] + d['buttons_x'] - 3 * d['padding_x'],
                .5 * d['buttons_y'] - .25 * d['padding_y'],
                2 * d['padding_x'],
                .5 * d['padding_y']
                )),
            label = 'Save',
            color = 'w',
            )
    def save_button_click(event):
        global save
        save = True
        plt.close('all')
    save_button.on_clicked(save_button_click)


    def box_submit(expression):
        for key in boxes.keys():
            try: values[key] = float(boxes[key].text)
            except ValueError: 
                print('invalid input')
                return
            sliders[key].set_val(values[key])
        update(values)
    for box in boxes.values():
        box.on_submit(box_submit)

    def slider_changed(val):
        for key in sliders.keys():
            values[key] = sliders[key].val
            boxes[key].set_val(f'{values[key]:.8g}')
        update(values)
    for slider in sliders.values():
        slider.on_changed(slider_changed)

    def update(values):
        data = origdata.copy()
        data[a][mask_down] += values[b] 
        data[a]            += values[p] 
        data[a]            *= values[s] 
        data[a] %= 360
        line_up_1.set_xdata(data[a][mask_up]*2*np.pi/360)
        line_down_1.set_xdata(data[a][mask_down]*2*np.pi/360)
        line_up_2.set_xdata(data[a][mask_up])
        line_down_2.set_xdata(data[a][mask_down])
        plt.draw()
        return data

    origdata = data.copy()
    global save 
    save = False
    mask_up = np.diff(data[a], prepend=-np.inf) > 0
    mask_down = np.diff(data[a], prepend=-np.inf) < 0
    data[a] %= 360

    line_up_1,   = ax1.plot(data[a][mask_up]*2*np.pi/360, data[M][mask_up])
    line_down_1, = ax1.plot(data[a][mask_down]*2*np.pi/360, data[M][mask_down])
    line_up_2,   = ax2.plot(data[a][mask_up], data[M][mask_up])
    line_down_2, = ax2.plot(data[a][mask_down], data[M][mask_down])

    slider_changed(None)
    plt.show()
    if save:
        data = update(values)
        return (data, values)
    else: 
        return (data, {})



def write(
        data: np.ndarray,
        values: dict[str, float],
        outputfile: str,
        ):
    np.savetxt(outputfile, data,
            delimiter = ',',
            header = \
                    'ACR Output file\n' + \
                    ', '.join(map(lambda i : f'{i[0]} = {i[1]}', values.items())) + '\n' + \
                    ', '.join(data.dtype.names),
            )

if __name__=='__main__':
    main()
