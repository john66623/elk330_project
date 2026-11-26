
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ============================================================
# 1. LESING AV DATA
# ============================================================

# INVERTER: 15-minuttsmålingar, norsk lokaltid (Europe/Oslo)
# ELHUB: Timesmålingar, med eksplisitt tidssone

inverter = pd.read_csv(
    "elk330/elk330_project/Kristoffer/inverter_Juli26.csv",
    sep=";",
    skiprows=11
)

malepunkt = pd.read_csv(
    "elk330/elk330_project/Kristoffer/soldata/Måleverdiar_707057500066690314_COMBINED_jul.csv",
    sep=";"
)


# ============================================================
# 2. TIDSHANDTERING
# ============================================================

# Inverter: les som norsk lokaltid
inverter["Time period"] = pd.to_datetime(
    inverter["Time period"],
    format="%m/%d/%Y %I.%M %p"
)

# Endre årstal for kompatibilitet med PowerFactory
inverter["Time period"] = inverter["Time period"].map(
    lambda x: x.replace(year=2018)
)

# Elhub: konverter frå oppgitt tidssone til norsk lokaltid
malepunkt["Frå"] = (
    pd.to_datetime(malepunkt["Frå"], utc=True)
    .dt.tz_convert("Europe/Oslo")
    .dt.tz_localize(None)
)

malepunkt["Frå"] = malepunkt["Frå"].map(
    lambda x: x.replace(year=2018)
)


# ============================================================
# 3. BEARBEIDING AV ELHUB-DATA
# ============================================================

# Konverter desimalkomma til flyttal
malepunkt["Volum"] = (
    malepunkt["Volum"]
    .str.replace(",", ".", regex=False)
    .astype(float)
)

# Del opp forbruk og produksjon
malepunkt = malepunkt.pivot_table(
    index="Frå",
    columns="Målenamn",
    values="Volum",
    aggfunc="sum"
)

malepunkt = malepunkt.rename(columns={
    "KWH 60 Forbruk": "Import [kWh]",
    "KWH 60 Produksjon": "Eksport [kWh]"
})

malepunkt.index.name = "Tid"


# ============================================================
# 4. AGGREGERING AV INVERTERDATA
# ============================================================

inverter.set_index("Time period", inplace=True)

# Målingane er registrerte ved slutten av kvart 15-minuttsintervall.
# Fire målingar: 00:15, 00:30, 00:45 og 01:00
# representerer timen 00:00–01:00.

sol_time = inverter["Power [kW]"].resample(
    "h",
    closed="right",
    label="left"
).agg(["mean", "count"])

# Kontroller talet på målingar per time
print("Tal målingar per time:")
print(sol_time["count"].value_counts().sort_index())

# Behald berre komplette timar
sol_time = sol_time[sol_time["count"] == 4]

# Gjennomsnittleg effekt [kW] gjennom timen
# Numerisk lik energi [kWh] for ein timesperiode
sol_time["Solproduksjon [kWh]"] = sol_time["mean"] * 1.0

sol_time = sol_time[["Solproduksjon [kWh]"]]


# ============================================================
# 5. SLÅ SAMAN DATA OG REKNE UT FAKTISK LAST
# ============================================================

# Bruk berre tidspunkt som finst i begge datasetta
faktiskLast = sol_time.join(
    malepunkt,
    how="inner"
)

# Kontroller manglande måleverdiar
if faktiskLast.isna().any().any():
    raise ValueError(
        "Manglande verdiar etter samanslåing. "
        "Kontroller tidsstempel og Elhub-data."
    )

# Faktisk last = solproduksjon + import - eksport
faktiskLast["Faktisk last [kWh]"] = (
    faktiskLast["Solproduksjon [kWh]"]
    + faktiskLast["Import [kWh]"]
    - faktiskLast["Eksport [kWh]"]
)


# ============================================================
# 6. RESULTAT OG KONTROLL
# ============================================================

print("\nTidsperiode:")
print(f"Frå: {faktiskLast.index.min()}")
print(f"Til: {faktiskLast.index.max()}")

print("\nStatistikk for faktisk last:")
print(faktiskLast["Faktisk last [kWh]"].describe())

# Finn negative verdiar
negative = faktiskLast[
    faktiskLast["Faktisk last [kWh]"] < 0
]

print(f"\nTal negative timar: {len(negative)}")

if len(negative) > 0:
    print("\nNegative verdiar:")
    print(negative)


# ============================================================
# 7. PLOTTING
# ============================================================

fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 8), sharex=True)

# Øvste subplot: Faktisk last
faktiskLast["Faktisk last [kWh]"].plot(
    ax=ax1,
    color="tab:blue",
    grid=True
)
ax1.set_ylabel("Energi [kWh]")
ax1.set_title("Faktisk last på garden")

# Nedste subplot: Energibalansen
faktiskLast[
    ["Import [kWh]", "Eksport [kWh]", "Solproduksjon [kWh]"]
].plot(
    ax=ax2,
    grid=True
)
ax2.set_ylabel("Energi [kWh]")
ax2.set_xlabel("Tid")
ax2.set_title("Energibalanse")
ax2.legend()

plt.tight_layout()
plt.savefig('elk330/elk330_project/Kristoffer/lastprofil.pdf')
# ============================================================
# 8. EKSPORT TIL POWERFACTORY (VALFRITT)
# ============================================================

faktiskLast.to_csv(
    "elk330/elk330_project/Kristoffer/faktisk_last.csv",
    sep=";",
    decimal=".",
    index_label="Time period"
)
