
from os import makedirs
from os.path import join
from concurrent.futures import ThreadPoolExecutor
from concurrent.futures import as_completed
from bs4 import BeautifulSoup
import requests, os
 
# decode downloaded html and extract all <a href=""> links
def get_urls_from_html():
    with open("supra.html") as fp:
        soup = BeautifulSoup(fp, "html.parser")
        data = {}
        table = soup.find("table")
        rows = table.find_all('tr')
        for idx, row in enumerate(rows):
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data[idx] = {"SC#" : cols[0], "filename" : cols[1]}
        return data

# save provided content to the local path
def save_file(path, data):
    # open the local file for writing
    with open(path, 'wb') as file:
        # write all provided data to the file
        file.write(data)
 
# download one file to a local directory
def download_url_to_file(url, link, path):
    #Join study/unique filename for outpath
    outpath = join(path, link['filename'])
    ########### Put the API here 
    r = requests.get(EXAMPLE_URL)
    # Download
    if os.path.exists(outpath):
        print(f'{outpath} Already exists - Skipping File', end=' --- ')
    else:
        with open(outpath, 'wb') as file:
            file.write(r.content)
            print(f'Starting Download of {outpath}', end=' --- ')
    return (link, path)

# download all files on the provided webpage to the provided path
def download_all_files(url, path):
    # download the html webpage
    #data = download_url(url)
    # create a local directory to save files
    makedirs(path, exist_ok=True)
    # parse html and retrieve all href urls listed
    links = get_urls_from_html()
    # report progress
    print("")
    print(f'Found {len(links)} links in study {PATH}')
    print("")
    # create the pool of worker threads
    with ThreadPoolExecutor(max_workers=1) as exe:
        # dispatch all download tasks to worker threads
        futures = [exe.submit(download_url_to_file, url, value, path) for link, value in links.items()]
        # report results as they become available
        for future in as_completed(futures):
            # retrieve result
            try:
                link, outpath = future.result()
                # check for a link that was skipped
            except Exception as exec:
                print(f'Exception raised for {link["filename"]} -> {exec}')
            else:
                print(f'Completed {link["filename"]} to {outpath}')


#####Example URL used to download a file
EXAMPLE_URL = "https://www.python.org/ftp/python/3.11.1/python-3.11.1-embed-amd64.zip"

# local directory to save all files on the html page
print("")
PATH = input("Enter the study you would like to download: ")

# url of html page that lists all files to download
URL = 'supra.html'
# download all files on the html webpage
download_all_files(URL, PATH)