#!/usr/bin/env python

import argparse
import sys
import yaml
from numpy import random
import os

import matplotlib.pyplot as plt

try:
    from astropy import units as u
except ImportError:
    print('Astropy (https://www.astropy.org/) is required')
    sys.exit()
try:
    import setigen as stg
except ImportError:
    print('Setigen (https://setigen.readthedocs.io/en/main/) is required')
    sys.exit()

SHOW_PLOTS = False

def load_config(filename):
    """load config file for general frame characteristics. 
    """
    try:
        with open(filename, 'r') as f:
            config = yaml.safe_load(f)
            return config['frame'], config['signal']
    except:
        print('Could not load and/or apply configuration')


def gen_dataset(frame, signal, n, output):
    """Generate dataset of filterbank files containing test signals.
    """
    for i in range(n):
        signal_params = gen_params(signal)
        gen_fil(frame, signal_params, i, output)


def gen_params(param_ranges):
    """Generate a parameter dictionary for an individual injected signal.
    """
    signal_params = {}
    signal_params['type'] = param_ranges['type']
    signal_params['drift'] = random.uniform(
        param_ranges['drift_min'], 
        param_ranges['drift_max']
        )
    signal_params['level'] = random.uniform(
        param_ranges['level_min'], 
        param_ranges['level_max']
        )
    signal_params['width'] = random.uniform(
        param_ranges['width_min'], 
        param_ranges['width_max']
        )
    return signal_params


def gen_fil(frame_params, signal_params, n, output):
    """Generate and save a single filterbank file.
    """
    frame = stg.Frame(
        fchans=frame_params['fchans']*u.pixel,
        tchans=frame_params['tchans']*u.pixel, 
        df=frame_params['df']*u.Hz,
        dt=frame_params['dt']*u.s,
        fch1=frame_params['fch1']*u.MHz
    )
    frame.add_noise(
        x_mean=frame_params['noise_mean'],
        x_std=frame_params['noise_std'], 
        noise_type=frame_params['noise_type']
    )
    start_chan = int(random.uniform(0, frame_params['fchans']))
    print(f'Starting channel number: {start_chan}')
    frame.add_constant_signal(
        f_start=frame.get_frequency(start_chan),
        drift_rate=signal_params['drift']*u.Hz/u.s,
        level=frame.get_intensity(snr=signal_params['level']),
        width=signal_params['width']*u.Hz,
        f_profile_type=signal_params['type']
    )
    frame.save_fil(os.path.join(output, f'synthetic_{n}.fil'))
    if SHOW_PLOTS:
        fig = plt.figure(figsize=(10, 6))
        frame.plot()
        plt.show()

def main(config, output, n_files):
    """Generate the dataset.
    """
    if output is None:
        output = os.getcwd()
    frame, signal = load_config(config)
    gen_dataset(frame, signal, n_files, output)


def cli(args = sys.argv[0]):
    """CLI for data generation.
    """
    usage = '{} [options]'.format(args)
    description = 'Generate a synthetic test dataset with setigen'
    parser = argparse.ArgumentParser(usage = usage, 
                                     description = description)
    parser.add_argument('--config', 
                        type = str,
                        default = 'config.yml', 
                        help = 'Location of config file.')
    parser.add_argument('--output', 
                        type = str,
                        default = None, 
                        help = 'Location in which to write synthetic files.')
    parser.add_argument('-n', 
                        type = int,
                        default = 1, 
                        help = 'Number of synthetic files to generate.')
    if len(sys.argv[1:]) == 0:
        parser.print_help()
        parser.exit()
    args = parser.parse_args()
    main(config = args.config, 
         output = args.output,
         n_files = args.n,
         )


if __name__ == '__main__':
    cli()
