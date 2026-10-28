import urllib.request
import json
import csv
from datetime import date, timedelta, datetime

# Innstillinger
startdato = date(2026, 1, 1)
sluttdato = date(2026, 10, 1)
prisomraade = "NO2"

filnavn = "strompriser_NO2_2026.csv"

# Samle alle prisene her
alle_priser = []

dato = startdato

while dato <= sluttdato:  # Endret til <= så du også får med selve sluttdatoen

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

    try:
        with urllib.request.urlopen(req, timeout=20) as respons:
            priser = json.loads(respons.read().decode("utf-8"))
            alle_priser.extend(priser)
    except Exception as e:
        print(f"Kunne ikke hente data for {dato}: {e}")

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
        # Henter ISO-strengen fra API-et (f.eks. "2026-01-01T00:00:00+01:00")
        original_tid = pris["time_start"]
        
        # Formaterer tidspunktet til et renere format (f.eks. "2026-01-01 00:00")
        dt = datetime.fromisoformat(original_tid)
        tidspunkt_formatert = dt.strftime("%Y-%m-%d %H:%M")

        skriver.writerow({
            "time_start": tidspunkt_formatert,
            "NOK_per_kWh": pris["NOK_per_kWh"]
        })

print(f"\nCSV-fil lagret: {filnavn}")
print(f"Antall timer hentet: {len(alle_priser)}")