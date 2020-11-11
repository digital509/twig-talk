# twig-talk
Twig-Talk is a Python module for communicating via serial with a Nelson Irrigation TD200 Twig Controller.

## Depencies
* serial
* re


## Usage
Import the module and initialize class object with connected port. For instance, the UART on the Raspberry Pi's GPIO is /dev/ttyAMA0 in this case.
```python
>>> from twigtalk import TwigController
>>> tc = TwigController("/dev/ttyAMA0')
```

Get the ID of the TD200 Twig Controller
```python
>>> tc.controller
'F1234567'
```

Get IDs of all connected Twigs
```python
>>> tc.twigs
['D123456','D123457']
```
Get the status of a Twig
```python
>>> tc.twig_status('D123456')
{'id': 'D123456', 'voltage': 2.7, 'rssi': 51, 'status': '8000', 'valve1_state': 0, 'valve1_message': 'Open Circuit Detected', 'valve2_state': 0, 'valve2_message': 'Open Circuit Detected', 'valve3_state': 0, 'valve3_message': 'Open Circuit Detected', 'valve4_state': 0, 'valve4_message': 'Open Circuit Detected'}
```
