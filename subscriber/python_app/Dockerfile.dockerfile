# Plik Dockerfile dla usługi python_app
FROM python:3.10-slim

# Ustaw katalog roboczy w kontenerze
WORKDIR /app

# Skopiuj wymagania Pythona
COPY requirements.txt /app/requirements.txt

# Zainstaluj zależności
RUN pip install --no-cache-dir -r /app/requirements.txt

# Skopiuj pozostałe pliki aplikacji
COPY . /app

# Ustaw polecenie uruchomienia aplikacji
CMD ["python", "app.py"]