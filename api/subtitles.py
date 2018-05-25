"""
Modulo para encontrar subtitulos de Subdivx
"""
import os
from mimetypes import guess_extension, add_type
import rarfile
import zipfile
import requests
import re
from bs4 import BeautifulSoup

# Anadir extension .rar
add_type('application/x-rar-compressed', '.rar')


def get_video_info(files):
    """
    Function to obtain information about the video file
    :param files: An array of filenames
    :return: An array of dictionaries with video information
    """
    files_info = []
    regex = re.compile(r"(.*?)\.S?(\d{1,2})E?(\d{2})\.(.*)")
    for file in files:
        match = regex.match(file)
        info = {
            "full_name": file,
            "name": match.group(1),
            "year": '',
            "season": match.group(2),
            "episode": match.group(3),
            "quality": '',
            "format": '',
            "coder": '',
            "extension": '',
        }
        files_info.append(info)

    return files_info


def get_from_subdivx(name):
    """
    Function that returns the download link from SubDivx
    :param video_info: A dictionary with information of the video file
    :return:
    """

    # Buscar a través de Google
    google_query = name.lower().split(".")
    google_url = 'https://www.google.com/search?client=ubuntu&channel=fs&q=site%3Asubdivx.com+' + "+".join(google_query)
    google_response = requests.get(google_url)
    google_results = BeautifulSoup(google_response.content).find_all('div', attrs={"class": "g"})
    for result in google_results:
        result_text = result.find("span", attrs={"class": "st"}).text.lower().split(" ")
        match_count = len(set(google_query).intersection(result_text))
        if match_count > len(google_query) / 2:
            google_link = result.cite.text
            break
    else:
        return

    # Buscar dentro de subdivx
    subdivx_response = requests.get(google_link)
    subdivx_results = BeautifulSoup(subdivx_response.content)

    # Si es una pagina o resultado de busqueda
    page = subdivx_results.find("a", attrs={"class": "link1"})
    search_result = subdivx_results.find("div", attrs={"id": "buscador_detalle_sub_datos"})
    if page:
        download_link = page["href"]
    elif search_result:
        download_link = search_result.find_all("a")[-1]["href"]
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

    # Hacer carpeta
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)

    # Descargar el archivo
    response = requests.get(link, stream=True)
    extension = guess_extension(response.headers['Content-type'].split()[0].rstrip(";"))
    handle = open(file_path + extension, "wb")
    for chunk in response.iter_content(chunk_size=512):
        if chunk:
            handle.write(chunk)
    handle.close()

    # Descomprimir el archivo mas pesado
    if extension == '.rar':
        rar = rarfile.RarFile(file_path + extension)
        rar_list = rar.infolist()
        most_heavy = rar_list[0]
        for file in rar_list:
            if file.file_size > most_heavy.file_size:
                most_heavy = file
        rar.extract(most_heavy, folder_path)
    elif extension == '.zip':
        zip = zipfile.ZipFile(file_path + extension)
        zip_list = zip.infolist()
        most_heavy = zip_list[0]
        for file in zip_list:
            if file.file_size > most_heavy.file_size:
                most_heavy = file
        zip.extract(most_heavy, folder_path)
    else:
        return
    os.rename(folder_path + '/' + most_heavy.filename, file_path + '.srt')
    os.remove(file_path + extension)