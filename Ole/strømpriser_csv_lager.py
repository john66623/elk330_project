
import urllib.request
import json
import csv
from datetime import date, timedelta, datetime

# Innstillinger
startdato = date(2026, 7, 1)
sluttdato = date(2026, 8, 1)
prisomraade = "NO2"

filnavn = "strompriser_NO2_juli_2026.csv"

# Samle alle prisene her
alle_priser = []

dato = startdato

while dato < sluttdato:

    url = (
        f"https://www.hvakosterstrommen.no/api/v1/prices/"
        f"{dato.year}/{dato.month:02d}-{dato.day:02d}_"
        f"{prisomraade}.json"
    )

    print(f"Henter priser for {dato}...")

    req = urllib.request.Request(
        url,
        headers={"User-Agent": "Mozilla/5.0"}
    )

    with urllib.request.urlopen(req, timeout=20) as respons:
        priser = json.loads(respons.read().decode("utf-8"))

    alle_priser.extend(priser)

    dato += timedelta(days=1)

# Lag CSV-filen
with open(filnavn, "w", newline="", encoding="utf-8") as fil:

    kolonner = [
    "time_start",
    "NOK_per_kWh"
    ]

    skriver = csv.DictWriter(fil, fieldnames=kolonner)
    skriver.writeheader()

    for pris in alle_priser:
     skriver.writerow({
    "time_start": tidspunkt_formatert,
    "NOK_per_kWh": pris["NOK_per_kWh"]
})

print(f"\nCSV-fil lagret: {filnavn}")
print(f"Antall timer hentet: {len(alle_priser)}")