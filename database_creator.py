import pandas as pd
from pymongo import MongoClient, ASCENDING
import json

import argparse

from tqdm.contrib.concurrent import process_map

import gc


collectionNames=["name.basics","title.akas","title.basics","title.crew","title.episodes","title.principals"]
parquet_path = "data_preparation/parquet/"

def importCollection(coll_name):
   
   """ Imports a csv file at path csv_name to a mongo colection
   returns: count of the documants in the new collection
   """
   
   client = MongoClient(host=db_url, port=db_port)
   db = client[db_name]
   
   coll = db[coll_name]
   
   with open(parquet_path+coll_name+".json") as f:
      payload = json.load(f)
   
   try:
      coll.insert_many(payload, ordered=False)
      del payload
      gc.collect()
      
      if "title.akas" in coll_name:
         coll.create_index([("nameLower",ASCENDING)], background=True)
      
      if "title.principals" in coll_name:
         coll.create_index([("titleId",ASCENDING)], background=True)
   finally:
      client.close()

def mongoimport(collectionName:str=None):

   if collectionName is not None:
      importCollection(parquet_path+collectionName+".json", collectionName)
   else:
      process_map(importCollection, collectionNames, max_workers=workers)
      
def mongodrop(collectionName:str=None):
   
   client = MongoClient(host=db_url, port=db_port)
   db = client[db_name]
   
   try:
      if collectionName is not None:
         db[collectionName].drop()
      else:
         client.drop_database("unive-imb")
   finally:
      client.close()

if __name__ == "__main__":
   
   parser = argparse.ArgumentParser(description='Utility script to perform DB operations',formatter_class=argparse.RawTextHelpFormatter)
   
   optional=parser.add_argument_group('Optional arguments')
   optional.add_argument('-workers', help='Number of workers to use for the import (default 1)', action='store', type=int, default=1, metavar='workers', choices=range(1,6+1))
   optional.add_argument('-db_url', help='URL of the MongoDB server (default localhost)', action='store', type=str, default='localhost', metavar='db_url')
   optional.add_argument('-db_port', help='Port of the MongoDB server (default 27017)', action='store', type=int, default=27017, metavar='db_port')
   optional.add_argument('-db_name', help='Name of the MongoDB database (default unive-imb)', action='store', type=str, default='unive-imb', metavar='db_name')
   
   action_group=parser.add_argument_group('Action to perform (choose one)')
   action_group=action_group.add_mutually_exclusive_group(required=True)
   
   action_group.add_argument('--removeAll', help='Remove the entire DB', action='store_true')
   action_group.add_argument('--importAll', help='Create and populate the entire DB', action='store_true')
   
   action_group.add_argument('--removeC', help='Remove the specified DB collection. Allowed values are: \n-'+'\n-'.join(collectionNames),action='store', type=str, choices=collectionNames, metavar='collectionName')
   action_group.add_argument('--importC', help='Create and populate the specified DB collection Allowed values are: \n-'+'\n-'.join(collectionNames), action='store', type=str, choices=collectionNames, metavar='collectionName')
   
   args = parser.parse_args()
   
   global workers
   global db_url
   global db_port
   global db_name
   
   workers=args.workers
   db_url=args.db_url
   db_port=args.db_port
   db_name=args.db_name
   
   if args.removeAll:
      print("Removing the entire DB")
      mongodrop()
   if args.importAll:
      print("Importing the entire DB")
      mongodrop()
      mongoimport()
   if args.removeC:
      print("Removing collection: "+args.removeC)
      mongodrop(args.removeC)
   if args.importC:
      print("Importing collection: "+args.importC)
      mongodrop(args.importC)
      mongoimport(args.importC)