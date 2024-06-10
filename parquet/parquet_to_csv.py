import pandas as pd
from os import walk

import os

from tqdm import tqdm

for (dirpath, dirnames, filenames) in walk(os.getcwd()):
    for filename in tqdm(filenames):
        if filename.endswith('.parquet'):
            df = pd.read_parquet(filename)
            df.to_csv(filename.replace('.parquet', '.csv'), index=False)
    break