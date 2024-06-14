import pandas as pd
from pymongo import MongoClient
import json

import argparse

from tqdm import tqdm

collectionNames=["name.basics","title.akas","title.basics","title.crew","title.episodes","title.principals"]

def importCollection(db, parquet_path, coll_name):
   
   """ Imports a csv file at path csv_name to a mongo colection
   returns: count of the documants in the new collection
   """
   
   coll = db[coll_name]
      
   with open(parquet_path) as f:
      payload = json.load(f)
   
   coll.insert_many(payload)

def mongoimport(collectionName:str=None):
   
   client = MongoClient(host=db_url, port=db_port)
   db = client[db_name]
   
   
   parquet_path = "data_preparation/parquet/"
   
   try:
      if collectionName is not None:
         importCollection(db, parquet_path+collectionName+".json", collectionName)
      else:
         for collectionName in tqdm(collectionNames):
            importCollection(db, parquet_path+collectionName+".json", collectionName)
   finally:
      client.close()
      
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
   
   
   class CustomFormatter(argparse.RawTextHelpFormatter, argparse.ArgumentDefaultsHelpFormatter):
      pass
   
   parser = argparse.ArgumentParser(description='Utility script to perform DB operations',formatter_class=CustomFormatter)
   
   db_connection=parser.add_argument_group('DB connection parameters')
   db_connection.add_argument('--db_url', help='URL of the MongoDB server', action='store', type=str, default='localhost', metavar='db_url')
   db_connection.add_argument('--db_port', help='Port of the MongoDB server', action='store', type=int, default=27017, metavar='db_port')
   db_connection.add_argument('--db_name', help='Name of the MongoDB database', action='store', type=str, default='unive-imb', metavar='db_name')
   
   action_group=parser.add_mutually_exclusive_group(required=True)
   
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