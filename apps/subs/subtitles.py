"""
Modulo para encontrar subtitulos de Subdivx
"""
import os
import PTN
import rarfile
import zipfile
import requests
import re

from bs4 import BeautifulSoup
from mimetypes import guess_extension, add_type

# Add .rar extension
add_type('application/x-rar-compressed', '.rar')


def get_video_info(files):
    """
    Function to obtain information about the video files
    :param files: An array of filenames
    :return: An array of dictionaries with video information
    """

    files_info = []
    for file in files:
        info = PTN.parse(file)
        files_info.append(info)

    return files_info


def get_google_link(name):
    """ Function to get the entry link of google search """

    query = name.lower().split(".")
    url = 'https://www.google.com/search?client=ubuntu&channel=fs&q=site%3Asubdivx.com+' + "+".join(query)
    response = requests.get(url)
    results = BeautifulSoup(response.content).find_all('div', attrs={"class": "g"})
    for result in results:
        text = result.find("span", attrs={"class": "st"}).text.lower().split(" ")
        count = len(set(query).intersection(text))
        if count > len(query) / 2:
            link = result.cite.text
            return link


def get_from_subdivx(name):
    """ Get the download link from SubDivx """

    link = get_google_link(name)
    response = requests.get(link)
    results = BeautifulSoup(response.content)

    # If its a page or search result
    url_code = re.search(r"(?P<Search>X5X)|(?P<Page>X6X)", link)
    if url_code.group("Page"):
        download_link = results.find("a", attrs={"class": "link1"})["href"]
    elif url_code.group("Search"):
        download_link = results.find("div", attrs={"id": "buscador_detalle_sub_datos"}).find_all("a")[-1][
            "href"]
    else:
        return None

    return download_link


def download(file_name, link, folder_path):
    """
    Function for download and extract subtitle inside a temporary folder
    :param file_name:
    :param link: The url to download the subtitle
    :param folder_path: The folder to extract the .rar file
    """

    file_path = os.path.join(folder_path, file_name)

    # Download file
    response = requests.get(link, stream=True)
    extension = guess_extension(response.headers['Content-type'].split()[0].rstrip(";"))
    handle = open(file_path + extension, "wb")
    for chunk in response.iter_content(chunk_size=512):
        if chunk:
            handle.write(chunk)
    handle.close()

    # Extract the heaviest file
    if extension == '.rar':
        rar = rarfile.RarFile(file_path + extension)
        rar_list = rar.infolist()
        most_heavy = rar_list[0]
        for file in rar_list:
            if file.file_size > most_heavy.file_size:
                most_heavy = file
        rar.extract(most_heavy, folder_path)

    elif extension == '.zip':
        zip_obj = zipfile.ZipFile(file_path + extension)
        zip_list = zip_obj.infolist()
        most_heavy = zip_list[0]
        for file in zip_list:
            if file.file_size > most_heavy.file_size:
                most_heavy = file
        zip_obj.extract(most_heavy, folder_path)

    else:
        raise Exception(f'Unknown file extension: {extension}')

    os.rename(folder_path + '/' + most_heavy.filename, file_path + '.srt')
    os.remove(file_path + extension)
