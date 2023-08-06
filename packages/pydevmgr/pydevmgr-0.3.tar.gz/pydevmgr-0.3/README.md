```
 ____            _                      ____          _ _               _   _              
|  _ \ __ _  ___| | ____ _  __ _  ___  |  _ \ ___  __| (_)_ __ ___  ___| |_(_) ___  _ __   
| |_) / _` |/ __| |/ / _` |/ _` |/ _ \ | |_) / _ \/ _` | | '__/ _ \/ __| __| |/ _ \| '_ \  
|  __/ (_| | (__|   < (_| | (_| |  __/ |  _ <  __/ (_| | | | |  __/ (__| |_| | (_) | | | | 
|_|   \__,_|\___|_|\_\__,_|\__, |\___| |_| \_\___|\__,_|_|_|  \___|\___|\__|_|\___/|_| |_| 
                           |___/                                                           
```


This is a redirection of the [pydevmgr_elt](https://github.com/efisoft-elt/pydevmgr_elt) packages (pydevmgr was the old name in v0.2). 

By installing this package one will install the following packages : 

- `pydevmgr_elt` : pydevmgr Classes to handle ELT devices. Which depend on: 
    - `pydevmgr_core` : Core package of pydevmgr 
    - `pydevmgr_ua` : Classes to handle UA communication within pydevmgr 


The documentation of pydevmgr_elt is [here](https://pydevmgr-elt.readthedocs.io/en/latest/pydevmgr_elt_manual.html)

# Install 

```bash
> pip install pydevmgr_elt 
```

# Basic usage 

```python 
from pydevmgr_elt import Motor, wait

motor1 = Motor(address="opc.tcp://192.168.1.11:4840",  prefix="MAIN.Motor001")

try:
    motor1.connect()
    wait( motor1.reset() )
    wait( motor1.init() )
    wait( motor1.enable()  )
    wait( motor1.move_abs(2.3, 0.5), lag=0.1)
    print( "Motor Pos",  motor1.stat.pos_actual.get() )
finally:
    motor1.disconnect()
    
```
