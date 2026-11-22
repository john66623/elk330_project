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

if(dag):
    malepunkt_dag = malepunkt.loc["2018-07-02"]

    malepunkt_dag["Volum"] = malepunkt_dag["Volum"].str.replace(",", ".", regex=False).astype(float)

    #Finn snitteffekt for kvar time, gjort om frå 5-min-interval
    effekter = [round(inverter["Power [kW]"].iloc[i:i+12].mean(), 2) for i in range(0, len(inverter["Time period"]), 12)]

    timer = np.arange(24)

    #Skriv data til csv-fil
    nyInv = pd.DataFrame()
    nyInv["Time"] = timer
    nyInv.set_index("Time", inplace=True)
    nyInv["Effekt"] = effekter

    faktiskLast = pd.DataFrame()
    faktiskLast.index = malepunkt.loc["2018-07-02"].iloc[0:24].index
    faktiskLast["Last"] = malepunkt_dag["Volum"].iloc[0:24]+effekter


    nyInv.to_csv("elk330/elk330_project/Kristoffer/inverter_dag.csv")
    malepunkt_dag.to_csv("elk330/elk330_project/Kristoffer/malepunkt_dag.csv")
    faktiskLast.to_csv("elk330/elk330_project/Kristoffer/sumLast_dag.csv")

    plt.plot(timer, effekter, label="inverter")
    plt.plot(timer, malepunkt_dag["Volum"].iloc[0:24], label="Målepunkt")
    plt.plot(timer, malepunkt_dag["Volum"].iloc[0:24]+effekter, label="faktisk last")
    plt.legend()
    plt.xlabel("Timer [H]")
    plt.ylabel("Effekt [kW]")
    plt.title("Forbruk på Nybø")
    plt.grid()
    #plt.show()


    #Lage filer med max output
    #

    max_effekt = max(effekter)
    print(f"max_effekt: {max_effekt}")

    max_df = pd.DataFrame()
    max_df["Time"] = timer
    max_df.index = malepunkt.loc["2018-07-02"].iloc[0:24].index
    max_df["Stråling [G]"] = 1035

    max_df.to_csv("elk330/elk330_project/Kristoffer/maxStraling_dag.csv")
else:
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
