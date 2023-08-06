## Install package

```bash
pip3 install .
```

## Build documentation

```bash
python setup.py build-sphinx
```

## Basic Usage

```python
from pyManson.mansonClass import manson
device_type = 'hcs'
port = '/dev/ttyUSB1'
channel = 1
hcs = manson(device_type,port,channel)
hcs.set_volts(1)
hcs.begin_session()
hcs.output_on()
for V in range(1,10):
	hcs.set_volts(V)
        time.sleep(dt)
hcs.output_off()
hcs.end_session()

```

## Tests

```python
python3 ./pyManson/examples/example.py
```

### Contributor

- Robin Barta

## Documentation:

``` bash
doc/
```
