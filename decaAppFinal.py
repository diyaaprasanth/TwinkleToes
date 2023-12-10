import datetime
import kivy
kivy.require('2.1.0') # replace with your current kivy version !

from kivy.app import App
from kivy.uix.label import Label
from kivy.lang import Builder
from kivy.config import Config
from kivy.core.window import Window
from kivy.uix.boxlayout import BoxLayout
from query import Database, QueryBuilder

# Name of database file
dbName = 'Db'

# Removes database if it already exists since we want to start fresh
#if os.path.exists(dbName):
#	os.remove(dbName)

# Instantiate Database
db = Database(dbName)

labels = (("name_id", "INTEGER PRIMARY KEY"), ('full_name', "TEXT NOT NULL"), ("date", "TEXT NOT NULL"))
# Build a create query
tableName = "DecaAttendance"
createQuery = QueryBuilder(tableName, "CREATE", labels)
db.tableCreation(createQuery)

Window.size = (1000,1300)

class LblTxt(BoxLayout):
	from kivy.properties import ObjectProperty
	firstName_input = ObjectProperty(None)
	lastName_input = ObjectProperty(None)
	code_input = ObjectProperty(None)

	def submit_form(self):
		firstName = self.firstName_input.text
		lastName = self.lastName_input.text
		code = self.code_input.text

		# Perform actions with the submitted data (e.g., save to a database)
		# Now search for an existing entry in each table
		name = (firstName.strip() + '' +  lastName.strip()).strip
		timeDate = datetime.datetime.now()
		insertQuery = QueryBuilder("DecaAttendance", "INSERT", ("full_name", "date"))
		tup = (name, timeDate)
		import pdb; pdb.set_trace()
		if code == "1234":
			db.tableEntryInsert(insertQuery, tup)
		else: 
			print("Wrong code. Try again.")

class MyApp(App):

	def build(self):
		self.root = Builder.load_file('simpleForm.kv')
		return self.root


if __name__ == '__main__':
	app = MyApp()
	MyApp().run()
