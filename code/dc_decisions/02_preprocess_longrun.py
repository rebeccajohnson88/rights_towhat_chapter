

############### Imports


import warnings
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
warnings.filterwarnings("ignore")

## pdf reading
import zipfile
import os
import glob
import pdfminer
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from sklearn.feature_extraction.text import CountVectorizer
import re
import string
import io

## dataframe
import pandas as pd
import numpy as np  


## preprocessing
import nltk
from nltk.corpus import stopwords
stop_words = set(stopwords.words('english'))
from sklearn.feature_extraction.text import CountVectorizer


## add punctuation and some application-specific words
## to stopword list
from nltk.stem.porter import *
porter = PorterStemmer()

## lda
from gensim import corpora
import gensim


## workhorse function
def convert_pdf_to_txt(path):
    rsrcmgr = PDFResourceManager()
    retstr = io.StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages,
                                  password=password,
                                  caching=caching,
                                  check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text

def read_hearing_pdf(one_path):
    text_hearing = convert_pdf_to_txt(one_path)
    extract_month = re.search(month_pattern, one_path).group(1)
    extract_year = re.search(year_pattern, one_path).group(1)
    key_name_stem = extract_month + "_" + extract_year 
    return key_name_stem, text_hearing

## base path
## store path to where the zip file
base_path = "/Users/raj2/Dropbox/dph_hearing_decisions/data/dc/" 

## get list of pathna
path_hearings = base_path  + "hearings"
os.chdir(path_hearings)
hearing_filenames = glob.glob("*HOD*")
#print(hearing_filenames)
## example with month
one_file = "HOD%20April%202018%20%281%29.pdf"
month_one_file = re.search('HOD%20(.+?)%20', one_file)
month_one_file.group(1)

## iterate over all months to make sure it works
month_pattern = 'HOD%20(.+?)%20'
month_all_files = [re.search(month_pattern, one_file).group(1) for one_file in hearing_filenames]

## extend to year and iterate to make sure it works
year_pattern = "%20.*%20(.+?)%20%28"
year_all_files = [re.search(year_pattern, one_file).group(1) for one_file in hearing_filenames]


## iterate through files and use pdf to text function to convert
## store in list
store_files = dict()
hearings_withpath = [path_hearings + "/" + one_filename for one_filename in hearing_filenames]
for i in range(len(hearings_withpath)):
    one_path = hearings_withpath[i]
    print("Reading in the file: " + str(one_path))
    try:
        key_name_stem, text_hearing = read_hearing_pdf(one_path)
        key_name = key_name_stem + "_" + str(i)
        store_files[key_name] = text_hearing
    except:
        pass

store_files_df = pd.DataFrame(store_files, index=[0]).T
store_files_df.columns = ['text']
store_files_df['month_and_year'] = store_files_df.index
store_files_df.to_pickle("/Users/raj2/Dropbox/dph_hearing_decisions/data/dc/intermediate/hearings_raw.pkl")


