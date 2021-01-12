# twig-talk
Twig-Talk is a Python module for communicating via serial with a Nelson Irrigation TD200 Twig Controller.

## Depencies
* serial
* re


## Usage
Import the module and initialize class object with connected port. For instance, the UART on the Raspberry Pi's GPIO is /dev/ttyAMA0 in this case.
```python
>>> from twigtalk import TwigController
>>> tc = TwigController('/dev/ttyAMA0')
```

Get the ID of the TD200 Twig Controller
```python
>>> tc.controller
'F1234567'
```

Get IDs of all connected Twigs
```python
>>> tc.twigs
['D123450','D123450']
```
Get the status of a Twig
```python
>>> tc.twig_status('D123450')
{'id': 'D123456', 'voltage': 2.7, 'rssi': 51, 'status': '8000', 'valve1_state': 0, 'valve1_message': 'Open Circuit Detected', 'valve2_state': 0, 'valve2_message': 'Open Circuit Detected', 'valve3_state': 0, 'valve3_message': 'Open Circuit Detected', 'valve4_state': 0, 'valve4_message': 'Open Circuit Detected'}
```
Controlling Valves
```python
>>> # Twig valves are accessed by changing the last digit of the Twig ID
>>> # If Twig ID is D123450, valve one would be accessed by changing the '0'
>>> # in the last digit to 1, 2, 3 or 4 for a four valve Twig.
>>> # tc.set_valve(valveID, state) State is 0 for off or 1 for on.
>>> tc.set_valve('D123451', 1)
