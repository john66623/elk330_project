fdkwokdow
das as pd
import numpy as np
import matplotlib.pyplot as plt

#Lesing fra fil
#
# INVERTER : kvart 5. minutt
# målepunkt: kvar time
inverter = pd.read_csv('elk330/elk330_project/Kristoffer/soldata/Energy and power - PV - Day - Tjerand Nybø - 2025-07-02.csv',sep = ";", skiprows = 11)
inverter["Time period"] = pd.to_datetime( "2026-07-02 " + inverter["Time period"], format="%Y-%m-%d %I.%M %p", utc=True)
malepunkt = pd.read_csv("elk330/elk330_project/Kristoffer/soldata/Måleverdiar_707057500066690314_COMBINED_jul.csv",sep = ";")
malepunkt["Frå"] = pd.to_datetime(malepunkt["Frå"], format="%Y-%m-%dT%H:%M:%S%z", utc=True)
malepunkt["Til"] = pd.to_datetime(malepunkt["Til"], format="%Y-%m-%dT%H:%M:%S%z", utc=True)

malepunkt.set_index("Frå", inplace=True)
malepunkt_dag = malepunkt.loc["2026-07-02"]

malepunkt_dag["Volum"] = malepunkt_dag["Volum"].str.replace(",", ".", regex=False).astype(float)
print(len(malepunkt_dag["Volum"]))
print(malepunkt_dag)
effekter = []
for i in range(0,len(inverter["Time period"]),12):
    effekter_time = 0
    for j in range(12):
        effekter_time += inverter["Power [kW]"].iloc[i+j]
    effekter_time = effekter_time/12
    effekter.append(round(effekter_time,2))

timer = np.arange(24)

plt.plot(timer, effekter, label="inverter")
plt.plot(timer, malepunkt_dag["Volum"].iloc[0:24], label="Målepunkt")
plt.plot(timer, malepunkt_dag["Volum"].iloc[0:24]+effekter, label="faktisk last")
plt.legend()
plt.xlabel("Timer [H]")
plt.ylabel("Effekt [kW]")
plt.grid()
plt.show()
