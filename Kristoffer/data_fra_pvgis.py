import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def solar_power(G, P_wp, T_air=None,
                gamma=-0.004, NOCT=45):
    """
    Reknar ut solcelleeffekt frå solinnstråling.

    Parameters
    ----------
    G : array
        Solinnstråling [W/m²]
    P_wp : float
        Installert effekt [kWp]
    T_air : array, optional
        Lufttemperatur [°C]
    gamma : float
        Temperaturkoeffisient [1/°C]
    NOCT : float
        Nominal Operating Cell Temperature [°C]

    Returns
    -------
    P : array
        Produsert effekt [kW]
    """

    # Effekt utan temperaturkorreksjon
    P = P_wp * (G / 1000)

    # Temperaturkorreksjon dersom temperaturdata finst
    if T_air is not None:
        T_cell = T_air + ((NOCT - 20) / 800) * G
        P *= (1 + gamma * (T_cell - 25))

    # Ingen negativ produksjon
    P = np.maximum(P, 0)
    P = np.minimum(P, 15)

    return P

df = pd.read_csv('elk330\elk330_project\Kristoffer\soldata\Oving6\data\Timeseries_59.735_6.756_SA3_36deg_0deg_2018_2018.csv', skiprows = 8, skipfooter=9)
df["time"] = pd.to_datetime(df["time"], format="%Y%m%d:%H%M", utc=True)

malepunkt = pd.read_csv("elk330/elk330_project/Kristoffer/soldata/Måleverdiar_707057500066690314_COMBINED_jul.csv",sep = ";")
malepunkt["Frå"] = pd.to_datetime(
    malepunkt["Frå"],
    format="%Y-%m-%dT%H:%M:%S%z",
    utc=True)
malepunkt["Til"] = pd.to_datetime(
    malepunkt["Til"],
    format="%Y-%m-%dT%H:%M:%S%z",
    utc=True)

malepunkt["Frå"] = malepunkt["Frå"].map(lambda x: x.replace(year=2018))
malepunkt["Til"] = malepunkt["Til"].map(lambda x: x.replace(year=2018))
malepunkt.set_index("Frå", inplace=True)

#innstalert effekt
#
P_wp = 15

P_solar = solar_power(G=df["G(i)"], P_wp=P_wp)

inverter = pd.DataFrame({
    "P_solar": P_solar.to_numpy()
}, index=df["time"])


malepunkt["Volum"] = malepunkt["Volum"].str.replace(",", ".", regex=False).astype(float)

malepunkt = malepunkt.drop(columns=["Til", "Registreringstidspunkt"])
malepunkt = malepunkt.groupby(level=0)["Volum"].sum().to_frame()
print(malepunkt)
# Hent juli 2018
malepunkt_Juli = malepunkt.loc["2018-07"]
inverter_Juli = inverter.loc["2018-07"]

faktiskLast = pd.DataFrame({
    "Målepunkt": malepunkt_Juli["Volum"],
    "Solproduksjon": inverter_Juli["P_solar"]
})

faktiskLast["Last"] = (
    faktiskLast["Målepunkt"] + faktiskLast["Solproduksjon"]
)
