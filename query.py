import os
import re 
import sqlite3

# This is the SQLite3 database storage class which provides basic functions for storing, deleting, searching, and reading tables
class Database:
	def __init__(self, dbName):
		try:
			self.sqliteConnection = sqlite3.connect(dbName) 
			self.cursor = self.sqliteConnection.cursor()
		except sqLite3.Error as error:
			print("Error while connecting to sqlite" , error)

	# Creates table using the query provided
	def tableCreation(self, query ):
		try:
			self.cursor.execute(query)
			self.sqliteConnection.commit()
		except sqlite3.Error as error:
			print("Table exists: ", error)

	# Inserts a table entry using the query and data provided
	def tableEntryInsert(self, query, tup):
		try:
			self.cursor.execute(query, tup)
			self.sqliteConnection.commit()
		except sqlite3.Error as error:
			print(query, tup)
			print("Failed to insert: ", error)
 
	# Search the table with the query provided and return the matching entry/entries 
	def tableSearch(self, query): 
		self.cursor.execute(query)
		result = self.cursor.fetchall()
		return result

	# Delete an entry from the table using the query provided
	def tableEntryDelete(self, query):
		try:  
			self.cursor.execute(query)
			self.sqliteConnection.commit()
		except sqlite3.Error as error:
			print("Failed to delete record from table: ", error)

# Query builder function which helps build a sqlite3 database query 
def QueryBuilder(TableName, QueryType, QueryTuple):

	# Build a query to delete a specified entry from the table 
	def _buildDeleteQuery(TableName, QueryTuple):
		# Build delete query
		delete_query = "DELETE from {0} where {1} = '{2}'".format(TableName, QueryTuple[0][0], QueryTuple[0][1])
		return delete_query
		
	# Build a select query to read the specified entries form the table
	def _buildSelectQuery(TableName, QueryTuple):
		# Build select query
		if QueryTuple == ():
			# When QueryTuple is empty, return all 
			select_query = "SELECT * FROM {0}".format(TableName)
		else:
			select_query = 'SELECT {0} FROM {1} WHERE {2} == "{3}"'.format(QueryTuple[0][0], TableName, QueryTuple[1][0], QueryTuple[1][1] )
		return select_query

	# Build insert query to add an entry to the table
	def _buildInsertQuery(TableName, QueryTuple):
		# Build insert query
		insert_query = 'INSERT INTO {0} {1} VALUES({2})'.format(TableName, QueryTuple, "?, "*(len(QueryTuple)-1)+"?")
		return insert_query

	# Build a query to create a table 
	def _buildCreateQuery(TableName, QueryTuple):
		# Build create query
		create_query = "CREATE TABLE {0} (".format(TableName)
		comma = ""  
		for item in QueryTuple:
			create_query += "{0} {1} {2} ".format(comma,item[0],item[1])
			comma = ","
		create_query += ")"
		return create_query

	# Invalid query type, pass to queryBuilder
	def _invalidQueryType(QueryType):
		print("Invalid query type. Type: ", QueryType) 
		return None
	
	# Valid query types and corresponding handlers
	queryBuilderFunctions = {"CREATE" : _buildCreateQuery, "INSERT" : _buildInsertQuery, "SELECT" : _buildSelectQuery, "DELETE" : _buildDeleteQuery} 

	# Invalid query type, return invalid query type handler
	if QueryType not in queryBuilderFunctions:
		return _invalidQueryType( QueryType )

	# Choose the handler for the query type and return
	function = queryBuilderFunctions[ QueryType ]
	return function(TableName, QueryTuple) 
