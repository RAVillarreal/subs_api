""" Module for downloading subtitles from subdivx """

import os
import PTN
import rarfile
import zipfile
import requests
import re
from django.conf.settings import MEDIA_ROOT
from bs4 import BeautifulSoup
from mimetypes import guess_extension, add_type

# Add rar mimetype
add_type('application/x-rar-compressed', '.rar')

def get_video_info(file):
    """ Obtain information about the video file """

    info = PTN.parse(file)
    return info

def get_google_link(name, site):
    """ Get site link from google search """

    google_query = re.find_all(r'\w+', name.lower())
    google_url = 'https://www.google.com/search?client=ubuntu&channel=fs&q=site%3A{0}}+{1}'.format(site, "+".join(google_query))
    google_response = requests.get(google_url)
    google_results = BeautifulSoup(google_response.content).find_all('div', attrs={"class": "g"})
    for result in google_results:
        result_text = result.find("span", attrs={"class": "st"}).text.lower().split(" ")
        match_count = len(set(google_query).intersection(result_text))
        if match_count > len(google_query) / 2:
            google_link = result.cite.text

            return google_link
    else:
        return None


def get_from_subdivx(name):
    """ Function that returns the download link from SubDivx """

    google_link = get_google_link(name)
    subdivx_response = requests.get(google_link)
    subdivx_results = BeautifulSoup(subdivx_response.content)
    url_code = re.search(r"(?P<Search>X5X)|(?P<Page>X6X)", google_link)
    if url_code.group("Page"):
        download_link = subdivx_results.find("a", attrs={"class": "link1"})["href"]
    elif url_code.group("Search"):
        download_link = subdivx_results.find("div", attrs={"id": "buscador_detalle_sub_datos"}).find_all("a")[-1][
            "href"]
    else:
        return None

    return download_link

def extract_subtitle(file_path, extension):
    """ Extract the most heavy .srt file """



def get_zip_file(title):

    path
    shutil.make_archive(, 'zip', new_folder_path)
            shutil.rmtree(new_folder_path)

def download(file_name, link):
    """ Download and extract subtitle inside a temporary folder """

    folder = os.path.join(settings.MEDIA_ROOT, uuid4())
    os.makedirs(folder)
    file_path = os.path.join(folder_path, file_name)
    response = requests.get(link, stream=True)
    extension = guess_extension(response.headers['Content-type'].split()[0].rstrip(";"))
    handle = open(file_path + extension, "wb")
    for chunk in response.iter_content(chunk_size=512):
        if chunk:
            handle.write(chunk)
    handle.close()
    extract_subtitle(folder, extension)
    