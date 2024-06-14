import pandas as pd
from os import walk

import os

import ast

import argparse

from tqdm import tqdm

tqdm.pandas(leave=False)

def parquet_to_json(target=None):
    
    for (_, _, filenames) in walk(os.getcwd()):
            
        for filename in (pbar :=tqdm([filename for filename in filenames if filename.endswith('.parquet') and (target is None or target in filename)])):
            
            pbar.set_description(f"Processing '{filename}'")
            df = pd.read_parquet(filename)
            
            if "name.basics" in filename:
                df["professions"]=df["professions"].progress_apply(lambda x: ast.literal_eval(x))
            
            if "title.basics" in filename or "title.episodes" in filename:
                df["genres"]=df["genres"].progress_apply(lambda x: ast.literal_eval(x))
                
            if "title.crew" in filename:
                df["directors"]=df["directors"].progress_apply(lambda x: ast.literal_eval(x))
                df["writers"]=df["writers"].progress_apply(lambda x: ast.literal_eval(x))
            
            if "title.principals" in filename:
                df["characters"]=df["characters"].progress_apply(lambda x: ast.literal_eval(x))
                
            if ("title.akas" in filename or "title.principal" in filename):
                df=df.reset_index(drop=True)
            else:
                df=df.reset_index()

            df.to_json(filename.replace('.parquet', '.json'), orient='records', indent=4)
            tqdm.write(f"'{filename}': Done!")
        break

if __name__ == "__main__":
    
    parser=argparse.ArgumentParser(description="Converts parquet files to json files")
    
    parser.add_argument("--target", type=str, default=None, help="Specify a target file to convert (Default: Concert all files)", metavar="target",choices=["name.basics","title.akas","title.basics","title.crew","title.episodes","title.principals"])
    
    args=parser.parse_args()
    parquet_to_json(args.target)