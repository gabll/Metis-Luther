import urllib2
from bs4 import BeautifulSoup
import re
from urlparse import urljoin
import time
from pprint import pprint
import pickle
import sys
import numpy as np
import dateutil.parser
import math

#need to script all the movies of a genre in the last two years
#fix less than 1 hr - movie duration

class BOM_movie:
    
    def __init__(self, BOM_id):
        """Create soup data form if"""
        self.BOM_id = BOM_id
        self.soup = self._get_soup_from_id(BOM_id)
    
    DEFAULT_URL = 'http://www.boxofficemojo.com/movies/?id=%s.htm'

    def _get_soup_from_id (self, BOM_id):
        """Create a soup from a BOM id"""
        opener = urllib2.build_opener()
        opener.addheader = [('User-agent', "Mozilla/5.0")]
        url = self.DEFAULT_URL % BOM_id
        page = opener.open(url)
        time.sleep(1)
        soup = BeautifulSoup(page)
        return soup
    
    def _get_movie_value(self, field_name):
        """find value given the name"""
        obj = self.soup.find(text=re.compile(field_name))
        if not obj:
            return None
        if 'as' not in obj:
            next_sibling = obj.findNextSibling()
        else:
            next_sibling = obj.next.next
        if next_sibling:
            return next_sibling.text
        else:
            return None       

    def _to_date(self, datestring):
        if datestring and "N/A" not in datestring and "TBD" not in datestring:
            date = dateutil.parser.parse(datestring.strip())
            return date
        else:
            return None

    def _money_to_int(self, moneystring):
        if moneystring and "N/A" not in moneystring and "n/a" not in moneystring:
            if "million" not in moneystring:
                moneystring = moneystring.replace('$','').replace(',','').replace('million','').replace(u'\xa0','').replace('(Estimate)','').strip()
                return float(moneystring)
            else:
                moneystring = moneystring.replace('$','').replace(',','').replace('million','').replace(u'\xa0','').replace('(Estimate)','').strip()
                return float(moneystring)*1000000
        else: 
            return None

    def _runtime_to_minutes(self, runtimestring):
        if runtimestring and "N/A" not in runtimestring:
            runtime = runtimestring.strip().split()
            if len(runtime) > 1:
                minutes = int(runtime[0])*60 + int(runtime[2])
            else:
                minutes = int(runtime[0])
            return minutes
        else:
            return None
        
    def _get_title(self):
        """Return movie title from page title"""
        title_string = self.soup.find('title').text
        title = title_string.split('(')[0].strip()
        return title
    
    def _get_opening_income(self):
        """Return RAW opening income from soup. If multiple opening it takes the first (limited)."""
        tr_row = self.soup.find(text=re.compile('Opening'))
        if not tr_row:
            return None
        else:
            row = tr_row.next
            if hasattr(row, 'text'):
                return row.text.strip()
            else:
                return None
    
    def _get_opening_theaters(self):
        """Return num of theaters on opening from soup"""
        tr_row = self.soup.find(text=re.compile('Opening'))
        if not tr_row:
            return None
        else:
            row = tr_row.next.next.next.next.next.next.next
            if hasattr(row, 'text'):
                if "#" in row.text:
                    return int(row.text.split()[2].strip().replace(',',''))
                else:
                    return int(row.text.split()[0].strip().replace(',','').replace('(',''))
            else:
                return None
    
    def _get_people(self, key):
        """Return director or actors list from soup"""
        tr_row = self.soup.find(text=re.compile(key))
        if not tr_row:
            return None
        else:
            row = tr_row.next
            if hasattr(row, 'text'):
                return row.text
            else:
                return None

    def get_movie_data(self):
        """Create a dictionary with the main data of a movie"""       
        raw_release_date = self._get_movie_value('Release Date')
        release_date = self._to_date(raw_release_date)
        raw_domestic_total_gross = self._get_movie_value('Domestic Total')
        domestic_total_gross = self._money_to_int(raw_domestic_total_gross)
        raw_runtime = self._get_movie_value('Runtime')
        runtime = self._runtime_to_minutes(raw_runtime)
        title = self._get_title()
        rating = self._get_movie_value('MPAA Rating')
        raw_budget = self._get_movie_value('Production Budget:')
        budget = self._money_to_int(raw_budget)
        genre = self._get_movie_value('Genre:')
        raw_opening_income_wend = self._get_opening_income()
        opening_income_wend = self._money_to_int(raw_opening_income_wend)
        distributor = self._get_movie_value('Distributor:')
        opening_theaters = self._get_opening_theaters()
        director = self._get_people('Director')
        actors = self._get_people('Actor')
        headers = ['BOM_id',
                   'movie_title',
                   'domestic_total_gross',
                   'release_date',
                   'runtime_mins',
                   'rating',
                   'budget',
                   'genre',
                   'opening_income_wend',
                   'distributor',
                   'opening_theaters',
                   'director',
                   'actors']
        movie_dict = dict(zip(headers, [self.BOM_id,
                                        title,
                                        domestic_total_gross,
                                        release_date,
                                        runtime,
                                        rating,
                                        budget,
                                        genre,
                                        opening_income_wend,
                                        distributor,
                                        opening_theaters,
                                        director,
                                        actors]))
        return movie_dict