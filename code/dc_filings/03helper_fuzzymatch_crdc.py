

########### Imports
from tabula import read_pdf
import os
import pandas as pd
import pickle
import re
import numpy as np
pd.set_option('display.float_format', lambda x: '%.3f' % x)
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"
from fuzzywuzzy import fuzz
from fuzzywuzzy import process

## profiling
import time


## fuzzy matches
def find_fuzzy_namematches(one_name: str, all_names: list, 
                           score_cutoff):
    
    ## extract matches above cutoff
    all_abovecutoff = process.extractBests(one_name, all_names, score_cutoff = score_cutoff,
                                          limit = 1)
    
    ## make into a dataframe (will thus only capture ones with matches)
    all_abovecutoff_df = pd.DataFrame(list(all_abovecutoff), columns = ['matched_name', 'score'])
    all_abovecutoff_df['original_name'] = one_name
    return(all_abovecutoff_df)


## Load data and get school names
filings_tosearch= pd.read_csv("../../intermediate_objects/filings_names_f22run.csv")  
cr_tosearchin = pd.read_csv("../../intermediate_objects/crdc_schoolnames_f22run.csv")  
cc_names = filings_tosearch.school_against_cleaned.tolist()
all_names= cr_tosearchin.name_tocompare_crdc.tolist()


## Fuzzy matching
print("starting fuzzy matching")
t0 = time.time()
fuzzymatch_results_list = [find_fuzzy_namematches(name, all_names, 80) 
                           for name in cc_names]
t1 = time.time()
print("Fuzzy matching took " + str(t1-t0) + " seconds to run")

## Concatenate results and write
fuzzymatch_results_df = pd.concat(fuzzymatch_results_list)
fuzzymatch_results_df.to_csv("../../intermediate_objects/filings_fuzzymatch_crdc_fall22.csv", index = False)

