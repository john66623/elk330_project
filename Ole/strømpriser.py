from matplotlib.cm import tab10
import pandas as pd
from scipy.signal import find_peaks
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("/Users/olekristiantaksdal/repos/elk330_project/Ole/strompriser_NO2_juli_2026.csv",
    dayfirst= True,
    parse_dates= ["time_start"]
)

#Ordner opp i tidssoner og setter tidssone til lokal Norge-tid
df["time_start"] = (pd.to_datetime(df["time_start"]))
#, 
#    format="%Y%m%d:%H%M").dt.round("h")
#)

df["time_start"] = pd.to_datetime(df["time_start"],
    utc=True
)

df = df.set_index('time_start')
df = df.tz_convert("Europe/Oslo")
df = df.tz_localize(None)

print(df.head)
dag = "2026-07-01"

last = pd.read_csv("/Users/olekristiantaksdal/repos/elk330_project/Ole/lastprofil.csv", 
    dayfirst= True,
    parse_dates=["time"]
)

last["time"] = pd.to_datetime(last["time"],
    format= "%Y%m%d:%H%M"
)
last = last.set_index("time")
last = last.tz_localize(None)
#last["time"] = last["time"].dt.tz_convert("Europe/Oslo").dt.tz_localize(None)

print(last.head)

sol = pd.read_csv("/Users/olekristiantaksdal/repos/elk330_project/Ole/solstråling.csv",
    engine = "python",
    skiprows = 8,
    skipfooter = 10,
    parse_dates= ["time"],
    dayfirst= True
)
sol["time"] = (pd.to_datetime(sol["time"],
    format = "%Y%m%d:%H%M").dt.round("h")
)

sol = sol.set_index("time")
sol = sol.tz_localize(None)

sol.index = sol.index.map(
    lambda dato: dato.replace(year=2026)
)

print(sol.head)

døgn_pris = df.loc[dag]
døgn_sol = sol.loc[dag]
#døgn_last = last.loc[dag]
last["load_kW"] = last["load_kW"]*5
last.plot(
    y= "load_kW",
    figsize = (10,5)
)
plt.xlabel("Tid [timer]")
plt.ylabel("Innstråling [W/m²]")
plt.legend()
plt.grid()

døgn_pris.plot(
    y = "NOK_per_kWh",
    figsize=(10, 5)
)
plt.legend()
plt.grid()

døgn_sol.plot(
    y="G(i)",
    figsize = (10, 5)
)
#plt.show()

#print(last["load_kW"].sum())

'''
Analyse av strømpris og kjøp og salg og sånn
Kjøper når strømprisen er lav for å lade opp bil, og bruker bil til strømforsyning ved toppene,
evt selge strøm hvis forbruk er mindre enn generering fra solceller
'''

# Solcellespesifikasjoner
PSTC = 555
gamma_P = -0.0034
NOCT = 43
T_omg = 25
A = 100
n = 0.215
døgn_sol["Tcelle"] = T_omg + ((NOCT - 20)/800) * døgn_sol["G(i)"]
#døgn_sol["kW"] = (døgn_sol["G(i)"] * A * n)/1000
døgn_sol["kW"] = 30 * (døgn_sol["G(i)"]/1000) * (1 + gamma_P*(døgn_sol["Tcelle"]- 25))
døgn_sol["netto"] = døgn_sol["kW"].to_numpy() - last["load_kW"].to_numpy()
print(døgn_sol.head)

plt.figure(figsize = (12, 6))

plt.plot(
    døgn_sol.index,
    døgn_sol["kW"],
    label = "produksjon"
)
plt.plot(
    døgn_sol.index,
    last["load_kW"],
    label = "forbruk"
)
plt.plot(
    døgn_sol.index,
    døgn_sol["netto"],
    label = "netto"
)
plt.xlabel("Timer")
plt.ylabel("kW")
plt.title("aaaaaa")
plt.legend()
plt.grid(True)
plt.show()
