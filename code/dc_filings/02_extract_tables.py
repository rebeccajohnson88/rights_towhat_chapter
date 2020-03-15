


############ Imports ###################

from tabula import read_pdf
import os
import pandas as pd
import pickle


############ Code ###############

print("Starting read")
dc_pdf = read_pdf("../data/dc/raw_filings/dc_ocr.pdf", pages = "all")
print("End read")


print("Storing")
pickle.dump(dc_pdf, open("../data/dc/intermediate/dc_rawtables.p", "wb")) 