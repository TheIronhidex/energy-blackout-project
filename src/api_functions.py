import requests 
import json
from dotenv import load_dotenv
import pandas

def request_country_population(url_specific, country):
    '''GET the population of a country, following the API specifications.
    Besides the URL you need to input a string with the name of a country'''
    querystring = {"country_name":f"{country}"}
    headers = {
    'x-rapidapi-host': "world-population.p.rapidapi.com",
    'x-rapidapi-key': "77b6c620f2msh0fe1e1c1514b344p1dc977jsnaa1a3b5b6be9"
    }
    response = requests.request("GET", url_specific, headers=headers, params=querystring)
    return response

def request_country_names(url_countries):
    '''GET a list of the available countries at the APIs database'''
    headers = {
    'x-rapidapi-host': "world-population.p.rapidapi.com",
    'x-rapidapi-key': "77b6c620f2msh0fe1e1c1514b344p1dc977jsnaa1a3b5b6be9"
    }
    response = requests.request("GET", url_countries, headers=headers)
    return response

def request_world_population(url_world):
    '''GET the total population of the world'''
    headers = {
    'x-rapidapi-host': "world-population.p.rapidapi.com",
    'x-rapidapi-key': "77b6c620f2msh0fe1e1c1514b344p1dc977jsnaa1a3b5b6be9"
    }
    response = requests.request("GET", url_world, headers=headers)
    return response

def format_json(input):
    '''Just applies the .json format to data gotten from an API. This function was created
    because just applying the method like .json() over the data was giving problems. Using the
    function allows to overlap the problem'''
    return input.json()

def request_all_countries_population(url_specific, countries_list):
    '''This is a combination of the functions above (which have been used for test during the first stages). 
    It allows to input a list of countries (the one obtained with the API) and to obtain at once all the population data 
    for all the countries'''
    all_countries_list = []
    for country in countries_list:
        querystring = {"country_name":f"{country}"}
        headers = {
    'x-rapidapi-host': "world-population.p.rapidapi.com",
    'x-rapidapi-key': "77b6c620f2msh0fe1e1c1514b344p1dc977jsnaa1a3b5b6be9"
    }
        response = requests.request("GET", url_specific, headers=headers, params=querystring)
        alfa = format_json(response)
        beta = alfa.get('body')
        all_countries_list.append(beta)

    return all_countries_list



