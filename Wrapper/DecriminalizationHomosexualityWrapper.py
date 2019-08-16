# coding: utf-8
'''
Created on 29 jul. 2019

@author: ingov
'''
#We use requests to get the wikipedia page for the lgtb rights for every country
import requests
#We use BeautifulSoup to parse the HTML of those pages
from bs4 import BeautifulSoup
#We use configparser to read the file countries_names.ini and with it, get the right
#names of countries to compose the URL for the lgtb rights pages in Wikipedia for each country
import configparser
#we use os to get the current path so we can browse to the files in the project we need
import os

def getRightCountryName(country):
    """
    @param country: Name of the country we are iterating in our json
    @return: A string that completes the correct URL to scrap in wikipedia for that country.
    These pages are the lgtb rights for each country that wikipedia has
    """
    #We initialize the var we will return
    countryName = ""
    #We use the library configparser, to parse the file countries_names.ini to get the right
    #name of some countries for the URL for wikipedia
    config = configparser.ConfigParser()
    config.optionxform = str
    #We read the file countries_name.ini
    config.read(os.getcwd()+"\..\Wrapper\countries_names.ini")
    #We get the content of the section COUNTRIES for that file and turn it into a dictionary
    #if the country we are iterating is in that file, we get the right name for the URL
    #for the lgtb rights page in wikipedia
    if country in dict(config.items("COUNTRIES")).keys():
        countryName = config["COUNTRIES"][country]
    else:
        #Else, the turn the spaces between the words in the name for into _
        countryName = country.replace(" ","_")
    #We return the variable countryName that contains the right part of the URL for the wikipedia
    #page
    return countryName

def getHTMLFromWikipedia(country):
    """
    @param country: Country we are iterating
    @return: The granted request for the page wikipedia has with information about lgtb rights and
    issues in that country 
    """
    URL = "https://en.wikipedia.org/wiki/LGBT_rights_in_"+country
    print("Getting: "+URL)
    r = requests.get(URL)
    return r

def parseStringHTML(tableSlide):
    """
    @param tableSlide: This parameter is the HTML code of the table that is displayed in the
    right side of every normalized page that wikipedia has for the lgtb rights and issues for 
    each country (it is a beautifulsoup object)
    @return: A string that parses that table, giving the links to other wikipedia pages
    the right prefix so we can use them and removing the anchors to the same page
    """
    #We turn our parameter into string
    tableStr = str(tableSlide[0])
    #Using replace, we give the URL for the link the right prefix, so we can use it from our
    #map
    tableStr = tableStr.replace('href="','href="https://en.wikipedia.org')
    #We remove every external string for anchors to the page we are scraping
    tableStr = tableStr.replace('see below','')
    tableStr = tableStr.replace("(<",'<')
    tableStr = tableStr.replace(">)",'>')
    #After all this changes we return the string with the HMTL modified
    return tableStr

def parseBeautifulHTML(r):
    """
    @param r: The granted request we got using the function getHTMLFromWikipedia previously defined
    @return: If there is a table in the left side of the page, we return a modified version of it
    without images or anchors and with the link correctly modified so they work on our html file
    If there is no table, we return an empty string
    """
    #We generate a beautfulsoup html parser using the property text of our request object
    soup = BeautifulSoup(r.text, 'html.parser')
    #We find all table object that have the css class infofox vcard (which is the class for
    #the right table)
    tableSlide = soup.find_all("table", ("class","infobox vcard"))
    #If we found at least one
    if(len(tableSlide)>0):
        #We get all the row for that table
        trSlide = tableSlide[0].find_all("tr")
        #If our table has more than one
        if len(trSlide)>1 and (trSlide[1] is not None):
            #We remove the second row, which will be the one containing the image and text
            #explaining the location of the country (which we don't need)
            trSlide[1].decompose()
        else:
            #If not, we just remove the images
            tableSlide.img.decompose()
        trSlide = tableSlide[0].find_all("sup")
        for sup in trSlide:
            #We remove all sup tags in the HTMl
            sup.decompose()
        #We call to the method parseStringHTML defined previously, so we get a string with
        #the HTML with the links pointing to the correct URLs and without anchors
        tableStr = parseStringHTML(tableSlide)
        #We return this string
        return tableStr
    else:
        #If there is no table, we return an empty string
        return ""
    
def getWikiInfo(series):
    """
    @param series: This contains a series with the information for a country taken from our
    dataframe, the name of the country will be in column 0
    @return: An string with the HTMl code for the table in the right part of the page, without
    images or anchors and with the links prepared to work outside wikipedia
    """
    #We get the country from the series
    country = series[0]
    #We get the right name to complete the URL for the normalized page wikipedia has for
    #the lgtb rights and issues facing that country is facing
    country = getRightCountryName(country)
    #We get the HTML code for that page
    r = getHTMLFromWikipedia(country)
    #We return the parsed HTML code for that page in a string. We only keep the HTML code
    #for the table in the right side (if it exists) but without images or anchors and the
    #links now work outside wikipedia
    return parseBeautifulHTML(r)