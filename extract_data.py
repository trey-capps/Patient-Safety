import wget
import os
from zipfile import ZipFile

class GetUnzip:
    
    def __init__(self, year):
        self.year = year
        self.device_url = f"https://www.accessdata.fda.gov/MAUDE/ftparea/device{self.year}.zip"
        self.text_url = f"https://www.accessdata.fda.gov/MAUDE/ftparea/foitext{self.year}.zip"
        self.device_name = f"device{self.year}.zip"
        self.text_name = f"foitext{self.year}.zip"

    def wget(self, url):
        wget.download(url)
        
    def unzip(self, file_name):
        with ZipFile(file_name, 'r') as deviceFile:
            deviceFile.extractall()
            
    def delete_zip(self, file_name):
        if os.path.exists(file_name):
            os.remove(file_name)
        else:
            print("The file does not exist")
            
    def extract_device(self):
        print(f"Extracting device data for {self.year}...")
        self.wget(self.device_url)
        print("Extracted Device Data")
        self.unzip(self.device_name)
        print("Unzipped Device Data")
        self.delete_zip(self.device_name)
        print("Removed Device Zip File")
    
    def extract_text(self):
        print(f"Extracting text data for {self.year}...")
        self.wget(self.text_url)
        print("Extracted Text Data")
        self.unzip(self.text_name)
        print("Unzipped Text Data")
        self.delete_zip(self.text_name)
        print("Removed Text Zip File")


if __name__ == "__main__":
    extract16 = GetUnzip(2016)
    extract16.extract_device()
    extract16.extract_text()

    extract17 = GetUnzip(2017)
    extract17.extract_device()
    extract17.extract_text()

    extract18 = GetUnzip(2018)
    extract18.extract_device()
    extract18.extract_text()

    extract19 = GetUnzip(2019)
    extract19.extract_device()
    extract19.extract_text()

    extract20 = GetUnzip(2020)
    extract20.extract_device()
    extract20.extract_text()

    extract21 = GetUnzip(2021)
    extract21.extract_device()
    extract21.extract_text()