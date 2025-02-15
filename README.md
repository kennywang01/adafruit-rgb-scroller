# adafruit-rgb-scroller
Personal project for scrolling text on 64x32 adafruit rgb matrix.

Runs on Raspberrypi Zero.

To set up, run the following:

```shell
sudo pip install -r requirements.txt
cd python
sudo apt-get update && sudo apt-get install python2.7-dev python-pillow -y
make build-python
sudo make install-python
```

To run `main.py`, run:
```shell
sudo python main.py --led-gpio-mapping adafruit-hat --led-rows 32 --led-cols 64
```

Do not attempt to run in virtual environment, must run with root permissions.
