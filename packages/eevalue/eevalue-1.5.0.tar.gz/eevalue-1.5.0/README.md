# EEValues
[![Test and package](https://github.com/Duckle29/EEValue/actions/workflows/python-package.yml/badge.svg)](https://github.com/Duckle29/EEValue/actions/workflows/python-package.yml)
A simple class for dealing with engieering values

Will print with Si prefix, and has an easy method to get the closest E-series value.

```python
>>> from eevalue import EEValue as EEV
>>> R = EEV(18.91)
>>> R.E(48, "ceil")
19.6
>>> EEV(17950.10).E(192,"floor")
17.8 k
```

