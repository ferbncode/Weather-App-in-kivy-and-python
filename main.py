from kivy.app import App #importing the app class so as 
						 #to run the damn application
from kivy.uix.boxlayout import BoxLayout #importing BoxLayout widget since i don't 
										 #want to create a dynamic class
from kivy.properties import ObjectProperty,ListProperty,NumericProperty,StringProperty #importing kivy properties 

from kivy.network.urlrequest import UrlRequest

import json

from kivy.uix.listview import ListItemButton


class WeatherApp(App):
	pass
class WeatherRoot(BoxLayout):
	'''this is the root widget which must have various configuration methods
	to decide how the screen looks.Other classes declared below will be children
	of the root class WeatherRoot in the kivy language file '''
	current_weather=ObjectProperty()

	def show_current_weather(self,location):
		self.clear_widgets()
		if location is None and self.current_weather is None:
			location=("New York","US")
		if location is not None:
			self.current_weather=CurrentLocation()
			self.current_weather.location=location
			self.current_weather.update_weather()
		self.add_widget(self.current_weather)
	def addlocation(self):
		self.clear_widgets()
		self.add_widget(AddLocationForm())
	def args_converter(self,index,data_item):
		city,country=data_item
		return {'location':(city,country)}

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
		print("finding location......")
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
		cities = [(d['name'], d['sys']['country']) for d in data['list']]
		self.search_results.item_strings=cities
		self.search_results.adapter.data.clear()
		self.search_results.adapter.data.extend(cities)
		self.search_results._trigger_reset_populate()
		print("function found_location searched")
		#this above line is just for the update the display when data changes
class LocationButton(ListItemButton):
	location=ListProperty()
class CoverPage(BoxLayout):
	pass
class CurrentLocation(BoxLayout):
	location=ListProperty()
	conditions=StringProperty()
	temp=NumericProperty()
	wind=NumericProperty()
	temp_max=NumericProperty()
	def update_weather(self):
		print("I am working")
		weather_template="http://api.openweathermap.org/data/2.5/"+"weather?q={}&units=metric"
		weather_url=weather_template.format(self.location[0])
		print("Dude i submitted the request")
		request2=UrlRequest(weather_url,on_success=self.weather_founded,on_failure=self.weather_failure,on_redirect=self.weather_redirect)
		print("I think i am going good")
	def weather_founded(self,request2,data2):
		print("Man i am working too")
		data2=json.loads(data2.decode()) if not isinstance(data2,dict) else data2
		self.conditions=data2['weather'][0]['description']
		self.temp=data2['main']['temp']
		print(self.temp)
		print(self.conditions)
		self.wind=data2['wind']['speed']
		self.temp_max=data2['main']['temp_max']
	def weather_failure(self,request2,data2):
		print("suyash i think its failing")
	def weather_redirect(self,request2,data2):
		print("Damn you")
if __name__=='__main__':
	WeatherApp().run()
#Refactoring the code means to change the code which makes no development.
#however helps the code to get more usable and more api compatible.
#Thus refactoring the code is a very important part.
2