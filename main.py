from kivy.app import App #importing the app class so as 
						 #to run the damn application
from kivy.uix.boxlayout import BoxLayout #importing BoxLayout widget since i don't 
										 #want to create a dynamic class
from kivy.properties import ObjectProperty #importing kivy properties 

from kivy.network.urlrequest import UrlRequest

import json

class WeatherApp(App):
	pass
class WeatherRoot(BoxLayout):
	'''this is the root widget which must have various configuration methods
	to decide how the screen looks.Other classes declared below will be children
	of the root class WeatherRoot in the kivy language file '''
	pass
class AddLocationForm(BoxLayout):
	'''this class inherits from the BoxLayout widget of the kivy language
	and contains the logic related to the location form,however the design part 
	lies with kivy file.The basic mockup in the mind is that of textinput,two buttons,
	and a listview widget containing all the places the man has already searched for'''
	search_input=ObjectProperty()
	search_results=ObjectProperty()
	def search_location(self):
		print(self.search_input.text)
		search_template="http://api.openweathermap.org/data/2.5/" + "find?q={}&type=like"
		search_url=search_template.format(self.search_input.text)
		print("human2")
		request=UrlRequest(search_url,self.found_location)
	def found_location(self,request,data):
		'''To notice in this method is the ListView can use different classes
		as the widget to be displayed .Two classes ListItemLabel and ListItemButton
		that behave normally only that they are containing info for tracking selection
		.Thus,its often a good idea to extend these classes'''
		data=json.loads(data.decode()) if not isinstance(data,dict) else data
		cities = ["{} ({})".format(d['name'], d['sys']['country']) for d in data['list']]
		self.search_results.item_strings=cities
		self.search_results.adapter.data.clear()
		self.search_results.adapter.data.extend(cities)
		self.search_results._trigger_reset_populate()
		print("human")
		#this above line is just for the update the display when data changes

if __name__=='__main__':
	WeatherApp().run()
