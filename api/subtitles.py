"""
Modulo para encontrar subtitulos de Subdivx
"""

import requests
import urllib
import re
from bs4 import BeautifulSoup

def get_from_subdivx(file_name):
    """
    Function that returns the download link from SubDivx
    :param file_path:
    :return:
    """

    # Buscar a través de Google
    file_name = 'mr.robot.s03e09.720p.hdtv.x264-avs'
    google_query = file_name.split(".")
    google_url = 'https://www.google.com/search?client=ubuntu&channel=fs&q=site%3Asubdivx.com+' + "+".join(google_query)
    google_response = requests.get(google_url)
    google_results = BeautifulSoup(google_response.content).find_all('div', attrs={"class": "g"})
    for result in google_results:
        result_text = result.find("span", attrs={"class": "st"}).text.split(" ")
        match_count = len(set(google_query).intersection(result_text))
        if match_count > len(google_query) / 2:
            google_link = result.cite.text

    #Buscar dentro de subdivx
    subdivx_response = requests.get(google_link)
    subdivx_results = BeautifulSoup(subdivx_response.content)
    #Si es una pagina o resultado de busqueda
    if subdivx_results.find("a", attrs={"class": "link1"}):
        download=requests.get(subdivx_results.link1.href)