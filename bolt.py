import requests
import PyPDF2
import re
import os
import pandas

prev_date = ""
def pdf_parse(URL):
    i=0
    prev_date = ""
    for link in URL:
        try:
            response = requests.get(link)
        except:
            print("Could not request file")
        
        if response.status_code == 200:
            with open("bolt.pdf", "wb") as raw_pdf:
                raw_pdf.write(response.content)

            with open("bolt.pdf","rb") as f:
                pdf_file=PyPDF2.PdfReader(f, "rb")
                page1=pdf_file.pages[0]
                text1=page1.extract_text()

                date_pdf = re.search('Datums: (.*)', text1)
                date_str = date_pdf.group(1)
                
                new_name = ""
                if date_str == prev_date:
                    i=i+1
                else:
                    i=1

                prev_date = date_str

                new_name = str(date_str[8:10]) + str(date_str[3:5]) + str(date_str[0:2]) + "_bolt" + str(i) + ".pdf"
                with open(new_name, "wb") as new_file:
                    new_file.write(response.content)
                prev_date = date_str
                os.remove("bolt.pdf")
        else:
            print("Could not find the file requested. Error code: " + str(response.status_code))

def read_data_csv(file):
    csv_data = pandas.read_csv(file,header=0)
    invoice_list = csv_data.get("Invoice")
    return invoice_list

bolt = []
bolt_series = []
file = "rides.csv"
bolt_series = read_data_csv(file)
bolt = bolt_series.tolist()
bolt.reverse()
pdf_parse(bolt)