from kivy.app import App #importing the app class so as 
						 #to run the damn application
from kivy.uix.boxlayout import BoxLayout #importing BoxLayout widget since i don't 
										 #want to create a dynamic class
from kivy.properties import ObjectProperty #importing kivy properties 

from kivy.network.urlrequest import UrlRequest

import json

from kivy.uix.listview import ListItemButton

from kivy.factory import Factory

class WeatherApp(App):
	pass
class WeatherRoot(BoxLayout):
	'''this is the root widget which must have various configuration methods
	to decide how the screen looks.Other classes declared below will be children
	of the root class WeatherRoot in the kivy language file '''
	def show_current_weather(self,location):
		self.clear_widgets()
		current_weather=Factory.CurrentLocation()
		current_weather.location=location
		self.add_widget(current_weather)
	def addlocation(self):
		self.clear_widgets()
		self.add_widget(AddLocationForm())

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
		print("finding location")
		request=UrlRequest(search_url,self.found_location)
	def found_location(self,request,data):
		'''To notice in this method is the ListView can use different classes
		as the widget to be displayed .Two classes ListItemLabel and ListItemButton
		that behave normally only that they are containing info for tracking selection
		.Thus,its often a good idea to extend these classes
		{"employees":[
    	{"firstName":"John", "lastName":"Doe"},
    	{"firstName":"Anna", "lastName":"Smith"},
    	{"firstName":"Peter", "lastName":"Jones"}
		]}
		Above is an example of the json code and so is to be taken care of.
		json is lightweight data interchange format.It is self-describing 
		.It is a syntax for storing and exchanging data.Its an alternative of 
		XML.Again,XML is a markup language made only to describe data.HTML to
		display data.
		'''
		data=json.loads(data.decode()) if not isinstance(data,dict) else data
		cities = ["{} ({})".format(d['name'], d['sys']['country']) for d in data['list']]
		self.search_results.item_strings=cities
		self.search_results.adapter.data.clear()
		self.search_results.adapter.data.extend(cities)
		self.search_results._trigger_reset_populate()
		print("function found_location searched")
		#this above line is just for the update the display when data changes
class LocationButton(ListItemButton):
	pass

class CoverPage(BoxLayout):
	pass

if __name__=='__main__':
	WeatherApp().run()
