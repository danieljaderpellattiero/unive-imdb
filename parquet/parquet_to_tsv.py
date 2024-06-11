import pandas as pd
from os import walk

import os

from tqdm import tqdm

for (dirpath, dirnames, filenames) in walk(os.getcwd()):
    for filename in (pbar :=tqdm([val for val in filenames if val.endswith('.parquet')])):
        pbar.set_description(f"Processing '{filename}'")
        df = pd.read_parquet(filename)
        df.to_csv(filename.replace('.parquet', '.tsv'), sep="\t", index= True if ("name.basics" in filename or "title.basics" in filename or "title.episodes" in filename) else False)
        tqdm.write(f"'{filename}': Done!")
    break