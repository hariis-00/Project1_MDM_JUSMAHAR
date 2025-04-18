from dotenv import load_dotenv
import os
from pymongo import MongoClient
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import OneHotEncoder
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import joblib
from sklearn.preprocessing import PolynomialFeatures
from sklearn.pipeline import make_pipeline
from sklearn.model_selection import cross_val_score
from sklearn.metrics import mean_squared_log_error
from sklearn.metrics import median_absolute_error
from azure.storage.blob import BlobClient
import datetime


load_dotenv()


mongo_uri = os.getenv('MONGO_URI')
client = MongoClient(mongo_uri)
db = client['Booking']
collection = db['Hotel']


documents = collection.find({})
df = pd.DataFrame(list(documents))

df['price'] = df['price'].replace(r'[^\d.]', '', regex=True).astype(float)
df['reviews count'] = df['reviews count'].str.replace(',', '').astype(int)
df['score'] = df['score'].astype(float)


X = df[['score', 'reviews count']].values
y = df['price'].values.astype(float)  


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)


model = make_pipeline(PolynomialFeatures(degree=2), LinearRegression())
model.fit(X_train, y_train)

# 📉 Auswertung
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
r2 = model.score(X_test, y_test)
msle = mean_squared_log_error(y_test, y_pred)
median_ae = median_absolute_error(y_test, y_pred)

print(f'Median Absolute Error: {median_ae}')
print(f'Mean Squared Logarithmic Error: {msle}')
print(f'Mean Squared Error: {mse}')
print(f'R^2 Score: {r2}')


for col in df.columns:
    if df[col].dtype == 'object' or isinstance(df[col].dtype, pd.CategoricalDtype):
        df = df.drop(col, axis=1)


corr = df.corr()
sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm')
plt.title('Korrelationsmatrix')
plt.show()

client.close()


joblib.dump(model, 'hotel_price_prediction_model.pkl')


sas_url = os.getenv('AZURE_STORAGE_SAS_URL')
timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M')
blob_name = f"hotel_model_{timestamp}.pkl"
full_blob_url = f"{sas_url.split('?')[0]}/{blob_name}?{sas_url.split('?')[1]}"

blob_client = BlobClient.from_blob_url(full_blob_url)
with open("hotel_price_prediction_model.pkl", "rb") as data:
    blob_client.upload_blob(data)
    print(f"✅ Modell erfolgreich nach Azure Blob hochgeladen als: {blob_name}")