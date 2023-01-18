import os, requests
from bs4 import BeautifulSoup

print(f'OS type -> {os.name}')

EXAMPLE_URL = "https://www.python.org/ftp/python/3.11.1/python-3.11.1-embed-amd64.zip"

### Take in the study ID
study_id = input("Enter a study_ID to download from SUPRA: ")


### Go to the SUPRA page and soup it
with open("supra.html") as fp:
    soup = BeautifulSoup(fp, "html.parser")

### parse the SUPRA site for the SC# and file name

data = {}
table = soup.find("table")
rows = table.find_all('tr')
for idx, row in enumerate(rows):
    cols = row.find_all('td')
    cols = [ele.text.strip() for ele in cols]
    data[idx] = {"SC#" : cols[0], "filename" : cols[1]}

### List the files that will be downloaded
print('')
print('####################')
print(f'The following files will be downloaded from study {study_id}')
print('####################')
print('')

for key, value in data.items():
    print(data[key]["filename"])

### Start downloading

for key, value in data.items():
    r = requests.get(EXAMPLE_URL)
    with open(value['filename'], 'wb') as file:
        file.write(r.content)
