"""
This file is for scraping and storing the transport data necessary to populate
our database of stops and routes
"""

import os
import pandas as pd
import requests
from urllib.request import urlopen
from zipfile import ZipFile

print("Downloading primary dataset.")
zipurl = 'https://transitfeeds.com/p/transport-for-ireland/782/latest/download'

# Download the file from the URL
print("Accessing zip.")
zipresp = urlopen(zipurl)
tempzip = open("/tmp/tempfile.zip", "wb")

# Write the contents of the downloaded file into the new file
tempzip.write(zipresp.read())

# Close the newly-created file
tempzip.close()
# Re-open the newly-created file with ZipFile()
zf = ZipFile("/tmp/tempfile.zip")

# Extract its contents into <extraction_path>
print("Writing dataset to path.")
zf.extractall(path='files/')

# close the ZipFile instance
zf.close()


# download our data from another source
print("Downloading supplement excel sheet.")
route_sequences = "https://www.transportforireland.ie/transitData/route_sequences_report_20210511_ALL.xlsx"
resp = requests.get(route_sequences)

# write excel file to data directory
print("Writing supplement excel sheet to path.")
output = open('files/route_seqs.xls', 'wb')
output.write(resp.content)
output.close()

print("Coverting excel sheet to csv.")
# convert file to csv
read_file = pd.read_excel("files/route_seqs.xls")

# Write the dataframe object into csv file
read_file.to_csv("files/route_seqs.csv",
                 index=None,
                 header=True)

print("Deleting redundant excel file")
os.remove("files/route_seqs.xls")
os.remove("files/agency.txt")
os.remove("files/calendar.txt")
os.remove("files/calendar_dates.txt")
os.remove("files/shapes.txt")
os.remove("files/routes.txt")
os.remove("files/trips.txt")

print("Finshed.")