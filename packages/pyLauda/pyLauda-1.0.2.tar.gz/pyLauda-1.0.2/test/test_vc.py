import unittest
from pyLauda.variocool import Variocool
from serial import SerialException
import time

class VariocoolTest(unittest.TestCase):

    DEV = '/dev/ttyUSB0'

    def test_device_init(self):
        dev = Variocool(self.DEV)
        self.assertEqual(dev.device.port, self.DEV)
        dev.test()
        

    def test_get_temperature(self):
        dev = Variocool(self.DEV)
        T1 = dev.temperature
        self.assertEqual(type(T1), float)
        self.assertTrue(T1>-20 and T1<100)
        T2 = dev.temperature
        self.assertTrue(abs(T1-T2) < 1)

    def test_get_SetTemperature(self):
        dev = Variocool(self.DEV)
        set_T1 = dev.temperature
        self.assertEqual(type(set_T1), float)
        set_T2 = dev.temperature
        self.assertEqual(set_T1, set_T2)

    def test_set_SetTemperature(self):
        dev = Variocool(self.DEV)
        # Get old SetTemperature
        set_T1 = dev.temperature
        self.assertEqual(type(set_T1), float)

        # Increase set temperature by 1K
        dev.temperature = set_T1 + 1
        set_T2 = dev.temperature

        self.assertEqual(type(set_T2), float)
        self.assertEqual(set_T2 - 1, set_T1)

	# Go back to old temperature
        dev.temperature = set_T2 - 1
        set_T3 = dev.temperature

        self.assertEqual(type(set_T3), float)
        self.assertEqual(set_T3, set_T1)

