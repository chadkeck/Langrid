#!/usr/bin/env python

from BeautifulSoup import BeautifulSoup
import sys
from pprint import pprint

class Alphabetical( object ):
	def __init__( self ):
		f = open( 'List_of_programming_languages', 'r' )
		html = f.read()
		self.soup = BeautifulSoup( html )

	def get_main_language_structure( self ):
		languages = {}
		list_items = self.soup.findAll( 'li' )
		for list_item in list_items:
			if not list_item.a: continue
			wiki_url = list_item.a['href']
			language = list_item.a.string
			if not language: continue

			c = wiki_url.count( 'action=edit' )
			has_info = True
			if c != 0:
				has_info = False

			languages[language] = {}
			languages[language]['url'] = wiki_url
			languages[language]['has_info'] = has_info
			languages[language]['categories'] = []
		return languages



class Timeline( object ):
	def __init__( self ):
		f = open( 'Timeline_of_programming_languages', 'r' )
		html = f.read()
		self.soup = BeautifulSoup( html )

	def get_language_text( self, td_tag ):
		if( td_tag.string ):
			return td_tag.string

		if( td_tag.a.string ):
			return td_tag.a.string

		return "?"

	def get_language_years( self ):
		ret = {}
		tables = self.soup.findAll( 'table', { "class": "wikitable sortable" } )
		for table in tables:
			#print table
			rows = table.findAll( 'tr' )
			for row in rows:
				columns = row.findAll( 'td' )
				if( len( columns ) > 2 ):
					language_year = columns[0].string
					language_name = self.get_language_text( columns[1] ).encode( 'ascii', 'ignore' )
					ret[language_name] = language_year

		return ret



class Categories( object ):
	def __init__( self ):
		f = open( 'List_of_programming_languages_by_category', 'r' )
		html = f.read()
		self.soup = BeautifulSoup( html )
		self.errors = []

	def get_categories( self ):
		d = []
		categories = self.soup.findAll( 'span', { "class": "mw-headline" } )
		for category in categories:
			cat = {}
			cat['category'] = category.string
			cat['language_urls'] = []

			language_list = category.findNext( 'ul' )
			languages = language_list.findAll( 'li' )
			try:
				for language in languages:
					#language_name = name_from_tag( language )
					if language.a:
						cat['language_urls'].append( language.a['href'] )
					else:
						self.errors.append( language )


			except AttributeError, err:
				print "ERROR [%s]: %s" % (language_name, err.message)
				pass
			except TypeError, err:
				print "ERROR [%s]: Type error" % (language_name)
				pass
			except UnicodeEncodeError, err:
				print "ERROR [%s] Unicode error" % (language_name)
				pass
			
			d.append( cat )

		return d

	def get_parse_errors( self ):
		return self.errors


if __name__ == '__main__':
	a = Alphabetical()
	languages = a.get_main_language_structure()

	t = Timeline()
	years = t.get_language_years()

	for language_name in languages.keys():
		year = years.get( language_name, '' )
		if language_name in languages:
			languages[language_name]['year'] = year
		else:
			raise Exception( "Error: found a language from the years processing that the alphabetical didn't find: %s" % (language_name) )
		#print '%s %s' %(language_name, year)

	#pprint( languages )

	cat = Categories()
	categories = cat.get_categories()
	for category_obj in categories:
		category_name = category_obj['category']
		language_urls = category_obj['language_urls']
		for url in language_urls:
			for language in languages:
				if languages[language]['url'] == url:
					languages[language]['categories'].append( category_name )

	pprint( languages )
