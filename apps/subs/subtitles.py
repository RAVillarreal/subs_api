""" Module for downloading subtitles from subdivx """

import os
import PTN
import rarfile
import zipfile
import requests
import re
import shutil
from bs4 import BeautifulSoup
from mimetypes import guess_extension, add_type

# Add rar mimetype
add_type('application/x-rar-compressed', '.rar')

def get_video_info(file):
    """ Obtain information about the video file """

    info = PTN.parse(file)
    return info

def get_google_link(query, site):
    """ Get site link from google search """

    google_query = re.findall(r'\w+', query.lower())
    google_url = 'https://www.google.com/search?client=ubuntu&channel=fs&q=site%3A{0}+{1}'.format(site, "+".join(google_query))
    google_response = requests.get(google_url)
    google_results = BeautifulSoup(google_response.content).find_all('div', attrs={"class": "g"})
    for result in google_results:
        print(result.prettify())
        result_text = result.find("span", attrs={"class": "st"}).text.lower().split(" ")
        match_count = len(set(google_query).intersection(result_text))
        if match_count > len(google_query) / 2:
            google_link = result.cite.text

            return google_link
    else:
        return None


def get_from_subdivx(query):
    """ Returns the subtitle download link from SubDivx """

    google_link = get_google_link(query, 'subdivx.com')
    if google_link:
        subdivx_response = requests.get(google_link)
        subdivx_results = BeautifulSoup(subdivx_response.content)
        code = re.search(r"(?P<Search>X5X)|(?P<Page>X6X)", google_link)
        if code:
            if code.group("Page"):
                download_link = subdivx_results.find("a", attrs={"class": "link1"})["href"]
            elif code.group("Search"):
                download_link = subdivx_results.find("div", attrs={"id": "buscador_detalle_sub_datos"}).find_all("a")[-1][
                    "href"]
            else:
                return None

            return download_link

    return None

def extract_subtitle(file_path, extension):
    """ Extract the most heavy .srt file """

    if extension == '.rar':
        compressed = rarfile.RarFile(file_path)
    elif extension == '.zip':
        compressed = zipfile.ZipFile(file_path)
    else:
        return None

    compressed_list = compressed.infolist()
    subtitle = compressed_list[0]
    for member in compressed_list:
        if member.file_size > subtitle.file_size and member.endswith('srt'):
            subtitle = member
    compressed.extract(subtitle)
    os.remove(file_path)

def download(file_name, link, download_folder):
    """ Download and extract subtitle inside a temporary folder """

    file_path = os.path.join(download_folder, file_name)
    if not os.path.exist(download_folder):
        os.makedirs(download_folder)
    response = requests.get(link, stream=True)
    extension = guess_extension(response.headers['Content-type'].split()[0].rstrip(";"))
    handle = open(file_path + extension, "wb")
    for chunk in response.iter_content(chunk_size=512):
        if chunk:
            handle.write(chunk)
    handle.close()
    extract_subtitle(file_path, extension)
 
def get_zip_file(folder_path):
    """ Compress the subtitles folder and return the download link """

    if os.path.exists(folder_path):
        zip = shutil.make_archive(folder_path, 'zip')
        zip = zipfile.ZipFile(zip)
        os.rmtree(folder_path)
        return zip.getinfo()

    return None