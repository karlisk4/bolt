import requests
import pandas
import numpy as np
prev_date = ""

def pdf_create(bolt_list):
    i=1
    prev_date = ""
    for elem in bolt_list:
        try:
            response = requests.get(elem[0])
        except:
            print("Could not request file")
        if response.status_code == 200:
            date = elem[1]
            if date[:11] == prev_date:
                    i=i+1
            else:
                    i=1            
            new_name = str(date[2:4]) + str(date[5:7]) + str(date[8:10]) + "_bolt" + str(i) + ".pdf"
            with open(new_name, "wb") as raw_pdf:
                raw_pdf.write(response.content)
            prev_date=date[:11]

def read_data_csv(file):
    csv_data = pandas.read_csv(file,header=0)
    invoice_list = csv_data[["Date", "Invoice"]]
    return invoice_list

bolt = []
bolt_series = []
file = "rides.csv"
bolt_series = read_data_csv(file)
bolt = bolt_series.to_numpy()
bolt = np.flip(bolt)
pdf_create(bolt)