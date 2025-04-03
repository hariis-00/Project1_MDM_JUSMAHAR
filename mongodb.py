import pandas as pd
from pymongo import MongoClient
import json


csv_file_path = 'hotels_list.csv' 
json_file_path = 'data.json' 


df = pd.read_csv(csv_file_path)
df['score'] = df['score'].str.extract('(\d+\.\d+)').astype(float)

df.to_json(json_file_path, orient='records', lines=True)




mongodb_url = "mongodb+srv://admin:12345@cluster0.uvofxqx.mongodb.net/"
client = MongoClient(mongodb_url)
db = client['Booking']
collection = db['Hotel']


with open(json_file_path, 'r') as file:
    data = [json.loads(line) for line in file]


collection.insert_many(data)

print(f"Es wurden {len(data)} Datensätze erfolgreich in MongoDB importiert.")


client.close()


