1) 🏨 Hotelpreis-Prognose mit Machine Learning, Docker & Azure

Dieses Projekt wurde im Rahmen des Moduls Model Deployment & Maintenance (MDM) umgesetzt. Ziel ist es, Hotelpreise auf Basis von Bewertungen und Anzahl Rezensionen vorherzusagen – und das Modell anschließend in einem Docker-Container auf Azure zu deployen.

2) 💡 Projektidee

Viele Nutzer stellen sich bei der Hotelbuchung die Frage:  
„Was kostet ein gutes Hotel mit vielen Bewertungen?“

Um diese Frage zu beantworten, wurden:
- Hotel-Daten von Booking.com gescraped
- In MongoDB gespeichert und bereinigt
- Ein ML-Modell zur Preisprognose trainiert
- Und die Webanwendung via Docker auf Azure bereitgestellt

3) ⚙️ Lokales Setup

4) Voraussetzungen
- Python 3.13
- Docker installiert
- MongoDB Atlas oder lokal
- .env-Datei mit MONGO_URI

 4.1 Repository klonen

git clone https://github.com/hariis/Project1_MDM_JUSMAHAR.git
cd Project1_MDM_JUSMAHAR

 4.2 (Optional) Modell neu trainieren

python machinelearningmodel.py

→ Erstellt: hotel_price_prediction_model.pkl

 4.2 Container lokal starten

docker build --platform linux/amd64 -t hotel-app .
docker run -p 5000:5000 hotel-app

App im Browser öffnen: http://localhost:5000

 🌐 Live-Demo auf Azure

Diese Anwendung wurde vollständig dockerisiert und auf Azure App Service deployed.

5. Live-App:  
https://hotel-preis-app-jusmani.azurewebsites.net

Du kannst dort:
- Einen Score (1–10) und Review-Anzahl eingeben
- Den prognostizierten Hotelpreis in CHF anzeigen lassen

6. Modellinformationen

- Modelltyp: Polynomial Regression (Grad 2)
- Features: score, reviews_count
- Zielwert: price (CHF)
- Metriken:
  - R² Score: 
  - MSE: 
  - MedianAE

7. 📣 Autor

Haris Jusmani  
Modul: Model Deployment & Maintenance  
Dozent: Adrian Moser