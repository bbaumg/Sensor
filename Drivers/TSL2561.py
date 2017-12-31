# Author:  Barrett Baumgartner
# 
# Driver for getting light data from the TSL2561 chip.
#
# Based on work done by 
#	http://www.raspberryconnect.com/hardware-add-ons/item/324-tsl2561-luminosity-sensor-ir-and-visible-light
# and
# 	https://github.com/ControlEverythingCommunity/TSL2561/blob/master/Python/TSL2561.py
# 
# Thanks to Adafruit for the datasheet on the chip
# 	https://cdn-shop.adafruit.com/datasheets/TSL2561.pdf
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

# ----------------------------------------------------------------------
# Example Usage (START)
# ----------------------------------------------------------------------

#~ import time
#~ from TSL2561 import TSL2561

#~ while True:
	#~ chip = TSL2561()      #Alternate TSL2561(address=0x##, gain=0x##)
	#~ print(chip.read_channel0())
	#~ print(chip.read_channel1())
	#~ print(chip.calculate_lux(chip.read_channel0()))
	#~ print(chip.get_visible_lux())
	#~ print(chip.get_full_lux())
	#~ print(chip.get_ir_lux())
	#~ chip.power_off
	#~ time.sleep(1)

# ----------------------------------------------------------------------
# Example Usage (END)
# ----------------------------------------------------------------------

import smbus
import time

TSL2561_ADDRESS			= 0x39 # Default Address (Default = 0x39)
TSL2561_CMD				= 0x80 # execute a command
TSL2561_CHANNEL_0		= 0x0C # address for channel 0
TSL2561_CHANNEL_1		= 0x0E # address for channel 1
TSL2561_POWER_ON		= 0x03 # power on 
TSL2561_POWER_OFF		= 0x00 # power off
TSL2561_GAIN_LOW_SHORT	= 0x00 # Gain at 1x and exposure at 13.7ms
TSL2561_GAIN_LOW_MED	= 0x01 # Gain at 1x and exposure at 100ms
TSL2561_GAIN_LOW_LONG	= 0x02 # Gain at 1x and exposure at 402ms
TSL2561_GAIN_LOW_MAN	= 0x03 # Gain x1 and Manual exposure
TSL2561_GAIN_HIGH_SHORT	= 0x10 # Gain x16 low light and exposure at 13.7ms
TSL2561_GAIN_HIGH_MED	= 0x11 # Gain x16 low light and exposure at 100ms
TSL2561_GAIN_HIGH_LONG	= 0x12 # Gain x16 low light and exposure at 402ms
TSL2561_GAIN_HIGH_MAN	= 0x13 # Gain x16 low light and Manual exposure
TSL2561_MAN_START		= 0x1F # Start Manual Exposure
TSL2561_MAN_END			= 0x1E # Stop Manual Exposure

class TSL2561(object):
	""" Base class for reading data from the lux chip """
	def __init__(self, address=TSL2561_ADDRESS, gain=TSL2561_GAIN_LOW_LONG, bus=None, **kwargs):
		""" Setup the bus, connect to it, and attempt to read from the device"""
		global TSL2561_ADDRESS
		if address != TSL2561_ADDRESS:
			TSL2561_ADDRESS = address
		if bus is None:
			import smbus
		self._bus = smbus.SMBus(1)
		try:
			self._bus.read_byte(TSL2561_ADDRESS)
		except:
			print("ERROR: " + str(__file__.split('/')[-1:][0]) +": The device could not be found on the bus = " + str(hex(address)))
			exit()
		# Now turn on the lux sensor & set the gain/exposure desired.
		self.power_on(gain=gain)
		
	def power_on(self, gain):
		"""  The There are two channels to the chip and both need to be turned on
		and set with an a gain level and exposure time"""
		# Turn on channel 0
		self._bus.write_byte_data(TSL2561_ADDRESS, TSL2561_CHANNEL_0 | TSL2561_CMD, TSL2561_POWER_ON)
		self._bus.write_byte_data(TSL2561_ADDRESS, TSL2561_CHANNEL_0 | TSL2561_CMD, gain)
		# Turn on channel 1
		self._bus.write_byte_data(TSL2561_ADDRESS, TSL2561_CHANNEL_1 | TSL2561_CMD, TSL2561_POWER_ON)
		self._bus.write_byte_data(TSL2561_ADDRESS, TSL2561_CHANNEL_1 | TSL2561_CMD, gain)
	
	def power_off(self):
		"""  Power the chip off when done"""
		self._bus.write_byte_data(TSL2561_ADDRESS, TSL2561_CHANNEL_0 | TSL2561_CMD, TSL2561_POWER_OFF)
		self._bus.write_byte_data(TSL2561_ADDRESS, TSL2561_CHANNEL_1 | TSL2561_CMD, TSL2561_POWER_OFF)
	
	def read_channel(self, channel):
		""" function to read the data from the channel in its raw form """
		result = self._bus.read_i2c_block_data(TSL2561_ADDRESS, channel | TSL2561_CMD, 2)
		return result

	def read_channel0(self):
		""" statically call channel 0 (Full Spectrum Light)"""
		result = self.read_channel(TSL2561_CHANNEL_0)
		return result

	def read_channel1(self):
		""" statically call channel 1 (IR Only Light)"""
		result = self.read_channel(TSL2561_CHANNEL_1)
		return result
	
	def calculate_lux(self, reading):
		""" calculation to get the single digit value for lux from the chip"""
		lux = reading[1] * 256 + reading[0]
		return lux
	
	def get_visible_lux(self):
		""" process to get visible lux which is (full spectrum - ir)"""
		ch0 = self.calculate_lux(self.read_channel0())
		ch1 = self.calculate_lux(self.read_channel1())
		lux = ch0 - ch1
		return lux
	
	def get_ir_lux(self):
		""" get and return just the IR channel"""
		lux = self.calculate_lux(self.read_channel1())
		return lux
	
	def get_full_lux(self):
		""" get and return the full spectrum channel"""
		lux = self.calculate_lux(self.read_channel0())
		return lux
	
