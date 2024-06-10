from surrealdb import Surreal
from random import choices

from copy import deepcopy
from tqdm import tqdm

#@profile
async def main()->list[dict]:
    
    async with Surreal("ws://localhost:8000/rpc") as db:
        
        await db.use("imb", "imb")
        await db.signin({"user": "whoami", "pass": "root"})
        
        movies:list[dict] = await db.select('title_ratings')
        
        movies = data_augmentation(movies)
    
    return movies

async def prova_inserimento(movies:list[dict]):
    
    for movie in tqdm(movies):
        del movie['id']
    
    async with Surreal("ws://localhost:8000/rpc") as db:
        
        await db.use("imb", "imb")
        await db.signin({"user": "whoami", "pass": "root"})
        
        movies_chunked = [movies[i:i+14000] for i in range(0, len(movies), 14000)]
        await db.query(sql=f"create prova")
        
        for chunk in tqdm(movies_chunked):
            #print(len(f"create prova; INSERT INTO prova {chunk}")) #16777216
            bho=await db.query(sql=f"INSERT INTO prova {chunk}")
            #print(bho)
        
        #movies:list[dict] = await db.select('prova')
        
        #print(len(movies))

def data_augmentation(movies:list[dict])->list[dict]:
    for _ in tqdm(range(14), desc="data augmentation", leave=True):
        movies+=deepcopy(movies)
    
    print("Num movies: ",len(movies))
    print("------\n")
    
    return movies

def sample_movies(movies:list[dict])->list[dict]:
    weights = [movie.get('numVotes') for movie in movies]
    to_query = choices(movies, weights = weights, k = 10000)
    
    #print(sum(x['numVotes'] for x in to_query)/len(to_query)) #for weighting testing
        
    #ids = [movie.get('id') for movie in to_query]
    
    #print(ids)
    
    return to_query

if __name__ == "__main__":
    import asyncio

    movies = asyncio.run(main())
    
    asyncio.run(prova_inserimento(movies))
    
    #sample_movies(movies)
