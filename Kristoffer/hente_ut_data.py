import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

#Lesing fra fil
#
# INVERTER : kvart 5. minutt
# målepunkt: kvar time
inverter = pd.read_csv('elk330/elk330_project/Kristoffer/inverter_Juli26.csv',sep = ";", skiprows = 11)
inverter["Time period"] = pd.to_datetime(
    inverter["Time period"],
    format="%m/%d/%Y %I.%M %p",
    utc=True)


malepunkt = pd.read_csv("elk330/elk330_project/Kristoffer/soldata/Måleverdiar_707057500066690314_COMBINED_jul.csv",sep = ";")
malepunkt["Frå"] = pd.to_datetime(
    malepunkt["Frå"],
    format="%Y-%m-%dT%H:%M:%S%z",
    utc=True)
malepunkt["Til"] = pd.to_datetime(
    malepunkt["Til"],
    format="%Y-%m-%dT%H:%M:%S%z",
    utc=True)

inverter["Time period"] = inverter["Time period"].map(lambda x: x.replace(year=2018))
malepunkt["Frå"] = malepunkt["Frå"].map(lambda x: x.replace(year=2018))
malepunkt["Til"] = malepunkt["Til"].map(lambda x: x.replace(year=2018))
malepunkt.set_index("Frå", inplace=True)
malepunkt["Volum"] = malepunkt["Volum"].str.replace(",", ".", regex=False).astype(float)

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
dag = False


inverter.set_index("Time period", inplace=True)
inverter_time = inverter["Power [kW]"].resample("h").mean().to_frame()
   # print(f"inverter indeks 1: {inverter_time.index[1]}")
   # print(f"malepunkt: {malepunkt.loc[inverter_time.index[1]:inverter_time.index[-1]]}")
malepunkt_uke = malepunkt.loc[inverter_time.index[0]:inverter_time.index[-1]]
print(malepunkt_uke)
print(f"hei{inverter.resample("h").count()}")
faktiskLast = pd.DataFrame()
faktiskLast.index = inverter_time.index
faktiskLast["Last"] = inverter_time["Power [kW]"] + malepunkt_uke["Import [kWh]"]-malepunkt_uke["Eksport [kWh]"]

#inverter_time.plot()
faktiskLast.plot()
plt.show()
