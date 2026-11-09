from matplotlib.cm import tab10
import pandas as pd
from scipy.signal import find_peaks
import numpy as np
import matplotlib.pyplot as plt

med_salg = "/Users/olekristiantaksdal/repos/elk330_project/Ole/resultater.csv"
uten_salg = "/Users/olekristiantaksdal/repos/elk330_project/Ole/resultater_uten_salg.csv"

df = pd.read_csv(uten_salg,
    skiprows= 1,
    dayfirst=True,
    parse_dates=["Time"]
)

df["Time"] = pd.to_datetime(df["Time"], format = "%Y-%m-%d %H:%M")


pris = pd.read_csv("/Users/olekristiantaksdal/repos/elk330_project/Ole/strompriser_NO2_2026.csv",
    dayfirst=True,
    parse_dates=["time_start"]
)

dag = "2018-02-07"

pris["time_start"] = pd.to_datetime(pris["time_start"], format = "%Y-%m-%d %H:%M")

pris["time_start"] = pris["time_start"].map(
    lambda x: x.replace(year=2018)
)
pris = pris.set_index("time_start")
df = df.set_index("Time")
dogn_pris = pris.loc[dag]
dogn_res = df.loc[dag]

effekt = dogn_res.iloc[:, 27]

nok = dogn_pris.iloc[:,0]

tot_pris = -(effekt * nok)

kostnad = pd.DataFrame({
    "Effekt_kW": effekt,
    "Pris_NOK_kWh": nok,
    "Totalpris_NOK": tot_pris
})

total_dogn = kostnad["Totalpris_NOK"].sum()

print("Total daglig fortjeneste:", total_dogn, "NOK")

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