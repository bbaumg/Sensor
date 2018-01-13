# Author:  Barrett Baumgartner
# 
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

import requests
import logging

THINGSPEAK_URL		= 'https://api.thingspeak.com/'

class thingspeak(object):
	def __init__(self, channel, apiKey, tsURL=THINGSPEAK_URL):
		"""
		Initalization "constructor" for the object.
		Initially populates the "fields" list.
		Defines the variables inside the object for holding most recent
			values for the update call
			
		"""
		logging.info("Instantiating a thingspeak object")
		self.tsRUL = tsURL			# URL for the thingspeak server
		logging.info("Thingspeak URL = " + str(self.tsRUL))
		self.apiKey = apiKey		# API Key for the Channel
		logging.info("API Key = " + str(self.apiKey))
		self.channel = channel		# Channel Number
		logging.info("Channel = " + str(self.channel))
		self.fields = dict()		# List of fields and their description
		logging.debug("List of fields as 'fields[]' = " + str(self.fields))
		self.field = dict()			# Fields and their most recent saved value
		logging.debug("List of field values as 'field[]' = " + str(self.field))
		#~ self.last = dict()
		#~ logging.debug("List of last written (non-null) values written" + str(self.last))
		
		try:
			results = requests.get(self.tsRUL)
			if results.ok != True:
				logging.error("The URL didn't return a 200")
				exit(1)
		except:
			logging.error("Error reaching the thingspeak URL = " + str(self.tsRUL))
			exit(1)
		self.fields = self.get_fields()
		logging.debug(self.fields)
		self.clear_field_values()
		logging.debug(self.field)
	
	def get_fields(self):
		"""Get the list of fields and their description and return them"""
		logging.debug("Beginning")
		options=dict(api_key = self.apiKey, results = 0)
		url = '{ts}channels/{id}/feeds.json'.format(
			ts=self.tsRUL,
			id=self.channel
		)
		try:
			results = requests.get(url, params=options)
			if results.ok != True:
				logging.error("The URL didn't return a 200")
				return
		except:
			logging.error("Error calling the thingspeak URL")
			return
		resultsJson = results.json()
		channelsJson = resultsJson['channel']
		fields = dict()
		for i in range(1,8):
			if 'field'+str(i) in channelsJson:
				fields['field'+str(i)] = channelsJson['field'+str(i)]
		return fields
	
	def get_last_channel(self):
		# ---------------------
		# WARNING:  Not working
		# ---------------------
		logging.debug("Beginning")
		options=dict(api_key = self.apiKey, results = 100)
		url = '{ts}channels/{id}/feeds.json'.format(
			ts=self.tsRUL,
			id=self.channel
		)
		results = requests.get(url, params=options)
		print(results.json())
		return
	
	def get_last_field(self, field):
		# ---------------------
		# WARNING:  Not working
		# ---------------------
		logging.debug("Getting last value for field = " + str(field))
		print(field[-1:])
		options=dict(api_key = self.apiKey, results = 100)
		url = '{ts}channels/{id}/fields/{fld}.json'.format(
			ts=self.tsRUL,
			id=self.channel,
			fld=field[-1:]
		)
		results = requests.get(url, params=options)
		resultsJson = results.json()
		channel = resultsJson['channel']
		feeds = resultsJson['feeds']
		lastEntry = channel['last_entry_id']
		print(lastEntry)
		return
	
	def post_update(self):
		"""POST an update to the channel for all fields with values"""
		logging.info("Beginning")
		options=dict(
			api_key = self.apiKey
		)
		counter = 0
		for key, value in self.field.items():
			if value != None:
				counter += 1
				options[key] = value
		if counter == 0:
			logging.error("There was nothing to update.  Check the field values")
			return
		url = '{ts}update'.format(
			ts=self.tsRUL,
		)
		logging.debug("Options = " + str(options))
		try:
			results = requests.post(url, params=options)
			if results.ok != True:
				logging.error("The update failed")
				return False
		except:
			logging.error("There was an error trying to update the values")
			return False
		self.clear_field_values()
		return True
		
	def clear_field_values(self):
		"""Clear out any saved values in the fields within the object"""
		logging.info("Clearing values in the field[] dictionary of the object")
		logging.debug("Before = " + str(self.field))
		for key, value in self.fields.items():
			self.field[str(key)] = None
		logging.debug("After = " + str(self.field))
		return
	
	def field_name(self, name):
		"""returns the name of field when description is passed in"""
		logging.info("Getting the field name " + str(name))
		try:
			fieldName = self.fields.keys()[self.fields.values().index(name)]
			logging.info("The field name for " + str(name) + " is " + str(fieldName))
			return fieldName
		except:
			logging.error(str(name)+ " Field Name was not found")
			return False
