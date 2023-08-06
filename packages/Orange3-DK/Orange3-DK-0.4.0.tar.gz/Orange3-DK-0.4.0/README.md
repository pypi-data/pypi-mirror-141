Orange3 DynamiKontrol Add-on
======================

Control DynamiKontrol motor modules on Orange3.

https://dk.m47rix.com

| DK Angle | DK Speed |
| --- | --- |
| <img src="https://dk.m47rix.com/static/assets/img/dynamikontrol/angle_07.png" width="400px"> | <img src="https://dk.m47rix.com/static/assets/img/dynamikontrol/speed_01.png" width="400px"> |

Installation
------------

```Orange3-DK```

### Step 1

Go to the menu `Options` - `Add-ons`.

![](doc/setup/setup_01.png)

### Step 2

Click `Add more...` button.

![](doc/setup/setup_02.png)

### Step 3

Type `Orange3-DK` and click `Add` button.

![](doc/setup/setup_03.png)

### Step 4

Check `DK` box and click `OK` to install the add-on.

![](doc/setup/setup_04.png)

### Step 5

Restart Orange3.

![](doc/setup/setup_05.png)

### Step 6

Enjoy!

![](doc/setup/setup_06.png)

Development
------------

To register this add-on with Orange, but keep the code in the development directory (do not copy it to 
Python's site-packages directory), run

    pip install -e .

Documentation / widget help can be built by running

    make html htmlhelp

from the doc directory.

Usage
-----

After the installation, the widget from this add-on is registered with Orange. To run Orange from the terminal,
use

    orange-canvas

or

    python -m Orange.canvas
