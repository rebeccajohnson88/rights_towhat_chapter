

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
cc_tosearch= pd.read_csv("/Users/raj2/Dropbox/dph_hearing_decisions/data/dc/intermediate/commoncore_tomatch.csv")  
cr_tosearchin = pd.read_csv("/Users/raj2/Dropbox/dph_hearing_decisions/data/dc/intermediate/ccd_pool.csv")  
cc_names = cc_tosearch.nces_name.tolist()
all_names= cr_tosearchin.nces_name.tolist()


## Fuzzy matching
print("starting fuzzy matching")
t0 = time.time()
fuzzymatch_results_list = [find_fuzzy_namematches(name, all_names, 90) 
                           for name in cc_names]
t1 = time.time()
print("Fuzzy matching took " + str(t1-t0) + " seconds to run")

## Concatenate results and write
fuzzymatch_results_df = pd.concat(fuzzymatch_results_list)
fuzzymatch_results_df.to_csv("/Users/raj2/Dropbox/dph_hearing_decisions/data/dc/intermediate/nces_civilrightsdf_fuzzymatch.csv")

