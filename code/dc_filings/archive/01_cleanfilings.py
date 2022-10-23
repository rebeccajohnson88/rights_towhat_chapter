

################# Imports and functions

from tabula import read_pdf
import os
import pandas as pd
import pickle
import re

from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"



def process_one_table(one_table):
    first_row = one_table.iloc[0, ].astype(str).str.upper()
    try:
        case_no_index = [i for i, e in enumerate(first_row) if re.search("CASE NUM", e)][0]
    except:
        case_no_index = 0
    try:
        home_school_index = [i for i, e in enumerate(first_row) if re.search("STUDENT HOM", e)][0]
    except:
        home_school_index = 0
    try:
        attending_school_index  = [i for i, e in enumerate(first_row) if re.search("STUDENT ATTEN", e)][0]
    except:
        attending_school_index = 0
    try:
        casetype_index  = first_row.tolist().index("CASE TYPE")
    except:
        casetype_index = 0
    try:
        dcps_index = [i for i, e in enumerate(first_row) if re.search("AGAINST DCP", e)][0]
    except:
        dcps_index = 0

    ## construct new df
    new_df = pd.DataFrame({'case_no': one_table.iloc[1:, case_no_index],
                          'home_school': one_table.iloc[1:, home_school_index],
                          'attending_school': one_table.iloc[1:, attending_school_index],
                          'casetype': one_table.iloc[1:, casetype_index],
                          'dcps_school_against': one_table.iloc[1:, dcps_index]})

    return(new_df)





############### Read raw tables
dc_filings = pickle.load(open("../data/dc/intermediate/dc_rawtables.p", "rb"))

## process the tables
print("starting processing")
processed_filings = [process_one_table(filing) for filing in dc_filings]
print("ending processing")
processed_all = pd.concat(processed_filings)



## fill and deduplicate
processed_filled = processed_all.fillna(method = "pad")
processed_dedup = processed_filled.drop_duplicates()

## write 
processed_dedup.to_csv("../data/dc/intermediate/processed_filings.csv", index = False)
