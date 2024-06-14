import pandas as pd
from os import walk

import os

from tqdm import tqdm

for (dirpath, dirnames, filenames) in walk(os.getcwd()):
    for filename in (pbar :=tqdm([val for val in filenames if val.endswith('.parquet')])):
        pbar.set_description(f"Processing '{filename}'")
        df = pd.read_parquet(filename)
        df.to_csv(filename.replace('.parquet', '.tsv'), sep="\t", index= True if ("title.akas" not in filename or "title.principal" not in filename) else False)
        tqdm.write(f"'{filename}': Done!")
    break