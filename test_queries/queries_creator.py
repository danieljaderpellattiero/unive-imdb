from surrealdb import Surreal
from random import choices

from copy import deepcopy
from tqdm import tqdm

@profile
async def main()->list[dict]:
    
    async with Surreal("ws://localhost:8000/rpc") as db:
        
        await db.use("imb", "imb")
        await db.signin({"user": "whoami", "pass": "root"})
        
        movies:list[dict] = await db.select('title_ratings')
        
        movies = data_augmentation(movies)
        
        #weights + sample with replacement
        weights = [movie.get('numVotes') for movie in movies]
        to_query = choices(movies, weights = weights, k = 10000)
        
        #print(sum(x['numVotes'] for x in to_query)/len(to_query)) #for weighting testing
        
        ids = [movie.get('id') for movie in to_query]
        
        print(ids)
            
    return ids

def data_augmentation(movies:list[dict])->list[dict]:
    for _ in tqdm(range(14), desc="data augmentation", leave=True):
        movies+=deepcopy(movies)
    
    print("Num movies: ",len(movies))
    print("------\n")
    
    return movies

if __name__ == "__main__":
    import asyncio

    movies = asyncio.run(main())
    
