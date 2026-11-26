from matplotlib.cm import tab10
import pandas as pd
from scipy.signal import find_peaks
import numpy as np
import matplotlib.pyplot as plt

med_salg = "/Users/olekristiantaksdal/repos/elk330_project/Ole/resultater.csv"
uten_salg = "/Users/olekristiantaksdal/repos/elk330_project/Ole/resultater_uten_salg.csv"
år_med_salg = "/Users/olekristiantaksdal/repos/elk330_project/Ole/resultater_år.csv"
år_uten_salg = "/Users/olekristiantaksdal/repos/elk330_project/Ole/resultater_år_uten_salg.csv"
år_med_salg_soc30 = "/Users/olekristiantaksdal/repos/elk330_project/Ole/resultater_år_med_salg_socmin30.csv"
år_uten_salg_soc30 = "/Users/olekristiantaksdal/repos/elk330_project/Ole/resultater_år_uten_salg_socmin30.csv"
år_uten_PV = "/Users/olekristiantaksdal/repos/elk330_project/Ole/resultater_år_uten_PV_socmin30.csv"
år_maxdischarge_1mw = "/Users/olekristiantaksdal/repos/elk330_project/Ole/resultater_maxdischarge_1mw.csv"
år_maxdischarge_10kw = "/Users/olekristiantaksdal/repos/elk330_project/Ole/resultater_maxdischarge_10kw.csv"
ny_år_med_salg = '/Users/olekristiantaksdal/repos/elk330_project/Ole/resultater_med_salg_nyeste.csv'
ny_år_uten_salg = '/Users/olekristiantaksdal/repos/elk330_project/Ole/resultater_uten_salg_nyeste.csv'
ny_uten_pv = '/Users/olekristiantaksdal/repos/elk330_project/Ole/resultater_uten_PV_ny.csv'

valgt_fil = ny_uten_pv
år = pd.read_csv(valgt_fil,
    skiprows=1,
    dayfirst=True,
    parse_dates=["Time"]
)

år["Time"] = pd.to_datetime(år["Time"])
år = år[
    (år["Time"] >= "2018-01-01") &
    (år["Time"] < "2018-10-01")
]
år = år.set_index("Time")

df = pd.read_csv(uten_salg,
    skiprows= 1,
    dayfirst=True,
    parse_dates=["Time"]
)

dag = "2018-02-07"

df["Time"] = pd.to_datetime(df["Time"], format = "%Y-%m-%d %H:%M")

pris = pd.read_csv("/Users/olekristiantaksdal/repos/elk330_project/Ole/strompriser_NO2_2026.csv",
    dayfirst=True,
    parse_dates=["time_start"]
)

pris["time_start"] = pd.to_datetime(pris["time_start"], format = "%Y-%m-%d %H:%M")

pris["time_start"] = pris["time_start"].map(
    lambda x: x.replace(year=2018)
)
pris = pris.set_index("time_start")
df = df.set_index("Time")

# UTREGNINGER FOR DAG
dogn_pris = pris.loc[dag]
dogn_res = df.loc[dag]

effekt_dogn = dogn_res.iloc[:, 27]
nok_dogn = dogn_pris.iloc[:,0]

tot_pris_dogn = -(effekt_dogn * nok_dogn)

kostnad_dogn = pd.DataFrame({
    "Effekt_kW": effekt_dogn,
    "Pris_NOK_kWh": nok_dogn,
    "Totalpris_NOK": tot_pris_dogn
})

total_dogn = kostnad_dogn["Totalpris_NOK"].sum()

print("Total daglig fortjeneste:", total_dogn, "NOK")

# UTREGNINGER FOR ÅRSPROFIL
effekt = år.iloc[:, 27]
nok = pris.iloc[:, 0]

tot_pris = -(effekt * nok)

kostnad = pd.DataFrame({
    "Effekt_kW": effekt,
    "Pris_NOK_kWh": nok,
    "Totalpris_NOK": tot_pris
})

total = kostnad["Totalpris_NOK"].sum()

print("Total årlig fortjeneste", total, "NOK")

#print(år.head())
#print(df.head())

#FIGUR FOR DØGN
plt.figure()
plt.plot(
    kostnad_dogn.index,
    kostnad_dogn["Totalpris_NOK"],
    label = "Kostnad/gevinst"
)
plt.xlabel("Timer")
plt.ylabel("NOK")
plt.title("Fortjeneste i NOK per time")
plt.legend()
plt.grid(True)

plt.figure()
plt.plot(
    kostnad_dogn.index,
    kostnad_dogn["Effekt_kW"],
    label = "Effekt til/fra eksternt nett"
)
plt.xlabel("Timer")
plt.ylabel("Effekt kW")
plt.title("Effekt til/fra eksternt nett")
plt.legend()
plt.grid(True)

plt.figure()
plt.plot(
    kostnad_dogn.index,
    kostnad_dogn["Pris_NOK_kWh"],
    label = "Strømpris"
)
plt.xlabel("Timer")
plt.ylabel("NOK")
plt.title("Strømpris per time")
plt.legend()
plt.grid(True)

#FIGUR FOR ÅR
plt.figure()
plt.plot(
    kostnad.index,
    kostnad["Totalpris_NOK"],
    label = "Kostnad/gevinst"
)
plt.xlabel("Timer")
plt.ylabel("NOK")
plt.title("Fortjeneste i NOK per time")
plt.legend()
plt.grid(True)

plt.figure()
plt.plot(
    kostnad.index,
    kostnad["Effekt_kW"],
    label = "Effekt til/fra eksternt nett"
)
plt.xlabel("Timer")
plt.ylabel("Effekt kW")
plt.title("Effekt til/fra eksternt nett")
plt.legend()
plt.grid(True)

plt.figure()
plt.plot(
    kostnad.index,
    kostnad["Pris_NOK_kWh"],
    label = "Strømpris"
)
plt.xlabel("Timer")
plt.ylabel("NOK")
plt.title("Strømpris per time")
plt.legend()
plt.grid(True)
plt.show()