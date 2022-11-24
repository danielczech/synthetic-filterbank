## synthetic-filterbank

Generate a set of synthetic filterbank files containing narrowband drifting 
signals, using setigen (see https://setigen.readthedocs.io and 
https://github.com/bbrzycki/setigen).

General frame parameters and signal characteristics can be specified in 
`config.yml`.  

Injected signal characteristics are drawn from a uniform distribution of 
values between the min and max values set in `config.yml`.

```
usage: generate_data.py [options]

Generate a synthetic test dataset with setigen

optional arguments:
  -h, --help       show this help message and exit
  --config CONFIG  Location of config file.
  --output OUTPUT  Location in which to write synthetic files.
  -n N             Number of synthetic files to generate.

```

### Requirements:

```
setigen >= 2.3.2
PyYAML >= 5.3.1
astropy >= 4.2
```
