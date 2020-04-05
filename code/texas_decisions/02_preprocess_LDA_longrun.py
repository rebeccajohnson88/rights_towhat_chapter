
# coding: utf-8

# In[1]:



## view all outputs
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
from nltk.tokenize import WordPunctTokenizer

## lda
from gensim import corpora
import gensim


# In[2]:


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


# # 0. Loading data
# 
# 
# **Task**: unzip the folder

# In[19]:


## store path to where the zip file
base_path = "/Users/raj2/Dropbox/dph_hearing_decisions/data/texas/" 

## unzip at that location if have not yet unzipped


# **Task**: to build the first part of your loop, extract two strings from the filenames (stored in hearing_filenames)
# 
# 1. The month
# 2. The year
# 
# Below provides some code for one file to get you started.

# In[4]:


## read in texas filings names
texas_wnces = pd.read_csv(base_path + "intermediate/texas_filings_wnces.csv")


# In[9]:


## clean the docket number
texas_wnces['clean_docket'] = texas_wnces['nan_docket_#'].astype(str).str.replace("\\s+", "")

## can then merge with frpl later


# In[16]:


## get list of pathna
path_hearings = base_path  + "hearings"
os.chdir(path_hearings)
hearing_filenames = glob.glob("*pdf*")



# **Task**: now that you've build the two building blocks-- a given hearing pdf's month and year-- iterate through the first five of the hearing pdfs, read it in, and store in a dictionary where the key is formatted as: "[nameofmonth]_[year]_i", where i is the element of the list (otherwise, python would overwrite the value each time two hearings have the same month/year)
# 
# Note: this takes some time to run due to the pdf conversion; so test the loop with the first five and in the next task, you'll read in data that already has it stored

# In[31]:


def read_hearing_pdf(one_path):
    text_hearing = convert_pdf_to_txt(one_path)
    extract_docket = re.sub(".*hearings/", "", one_path)
    return extract_docket, text_hearing


# In[32]:


## iterate through files and use pdf to text function to convert
## store in list
store_files = dict()
hearings_withpath = [path_hearings + "/" + one_filename for one_filename in hearing_filenames]



# In[25]:

print("starting loop")
for i in range(len(hearings_withpath)):
    one_path = hearings_withpath[i]
    print("Reading in the file: " + str(one_path))
    try:
        extract_docket, text_hearing = read_hearing_pdf(one_path)
        store_files[extract_docket] = text_hearing
    except:
        pass


store_files_df = pd.DataFrame(store_files, index=[0]).T


store_files_df.columns = ['text']
store_files_df['docket_num'] = store_files_df.index
store_files_df.to_pickle(base_path + "intermediate/hearings_raw.pkl")

print("end of script")
