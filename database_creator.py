from pymongo import MongoClient
import argparse
from tqdm import tqdm
import subprocess

from data_preparation.parquet.parquet_to_json import parquet_to_json
import os


collectionNames=["name.basics","title.akas","title.basics","title.crew","title.episodes","title.principals"]
parquet_path = "data_preparation/parquet"

def importCollection(coll_name):
   
   #subprocess.call('C:\Windows\System32\powershell.exe Get-Process', shell=True)
   return subprocess.Popen(f'mongoimport --host="localhost" --port="27017" -d="unive-imdb" --collection="{coll_name}" --jsonArray --file="{parquet_path+"/"+coll_name}.json" --quiet', shell=True)

def createIndex(collectionName:str):
      
      client = MongoClient(host=db_url, port=db_port)
      db = client[db_name]
      
      try:
         if collectionName == "title.akas":
            db[collectionName].create_index([("nameLower", 1)])
         if collectionName == "title.principals":
            db[collectionName].create_index([("titleId", 1)])
      finally:
         client.close()

def mongoimport(collectionName:str=None):

   if collectionName is not None:
      with tqdm(total=1) as pbar:
         importCollection(collectionName).wait()
         pbar.update(1)
   else:
      processes=[]
      
      for collection in collectionNames:
         processes.append(importCollection(collection))
         createIndex(collection)
      
      with tqdm(total=6) as pbar:
         while True:
            
            finished=0
            for p in processes:
               if p.poll() is not None:
                  finished+=1
            
            pbar.update(finished-pbar.n)
            
            if finished==6:
               return

def mongodrop(collectionName:str=None):
   
   client = MongoClient(host=db_url, port=db_port)
   db = client[db_name]
   
   try:
      if collectionName is not None:
         db[collectionName].drop()
      else:
         client.drop_database("unive-imdb")
   finally:
      client.close()

if __name__ == "__main__":
   
   parser = argparse.ArgumentParser(description='Utility script to perform DB operations',formatter_class=argparse.RawTextHelpFormatter)
   
   optional=parser.add_argument_group('Optional arguments')
   optional.add_argument('-db_url', help='URL of the MongoDB server (default localhost)', action='store', type=str, default='localhost', metavar='db_url')
   optional.add_argument('-db_port', help='Port of the MongoDB server (default 27017)', action='store', type=int, default=27017, metavar='db_port')
   optional.add_argument('-db_name', help='Name of the MongoDB database (default unive-imdb)', action='store', type=str, default='unive-imdb', metavar='db_name')
   
   action_group=parser.add_argument_group('Action to perform (choose one)')
   action_group=action_group.add_mutually_exclusive_group(required=True)
   
   action_group.add_argument('--removeAll', help='Remove the entire DB', action='store_true')
   action_group.add_argument('--importAll', help='Create and populate the entire DB', action='store_true')
   
   action_group.add_argument('--removeC', help='Remove the specified DB collection. Allowed values are: \n-'+'\n-'.join(collectionNames),action='store', type=str, choices=collectionNames, metavar='collectionName')
   action_group.add_argument('--importC', help='Create and populate the specified DB collection Allowed values are: \n-'+'\n-'.join(collectionNames), action='store', type=str, choices=collectionNames, metavar='collectionName')
   
   args = parser.parse_args()
   
   global db_url
   global db_port
   global db_name
   
   db_url=args.db_url
   db_port=args.db_port
   db_name=args.db_name
   
   
   if args.removeAll:
      print("Removing the entire DB")
      mongodrop()
   if args.importAll:
      
      response = ""
      while response not in ["y","n"]:
         response = input("Do you want also to reload .json files? (y/n) ")
         
      if response == "y":
         print("Reloading .json files:")
         #print(os.getcwd()+"/"+parquet_path)
         parquet_to_json(directory=os.getcwd()+"/"+parquet_path)
         print("Done!\n")
      elif response == "n":
         print("Skipping .json files reload.\n")
         
      print("Importing the entire DB")
      mongodrop()
      mongoimport()
   if args.removeC:
      print("Removing collection: "+args.removeC)
      mongodrop(args.removeC)
   if args.importC:
      
      response = ""
      while response not in ["y","n"]:
         response = input("Do you want also to reload .json file? (y/n) ")
         
      if response == "y":
         print("Reloading .json file:")
         #print(os.getcwd()+"/"+parquet_path)
         parquet_to_json(target=args.importC, directory=os.getcwd()+"/"+parquet_path)
         print("Done!\n")
      elif response == "n":
         print("Skipping .json file reload.\n")
         
      print("Importing collection: "+args.importC)
      mongodrop(args.importC)
      mongoimport(args.importC)

   print("Done!")