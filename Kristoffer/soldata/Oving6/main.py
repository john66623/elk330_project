from matplotlib.cm import tab10
import pandas as pd
from scipy.signal import find_peaks
import numpy as np
import matplotlib.pyplot as plt

# Om skriving til bildefil!
#
# Berre tilpass filplassering, fungerar jo berre på min maskin no.
# Bruk chat ellerno for å fiksa
#


def gauss_curve(t: np.ndarray, a :float, mu :float, sigma :float) -> np.ndarray: return a * np.exp(-(t - mu)**2 / (2 * sigma**2))
'''
t = np.linspace(0, 24, 100)
A = 800
mu = 12
sigma = 2.5
g = gauss_curve(t, A, mu, sigma)

plt.plot(t, g)
plt.xlabel('Tid (t)')
plt.ylabel('G(t)')
plt.title('Gauss-kurve for solstråling G(t)')

#skriv til fil
plt.savefig('elk330/elk330_project/Kristoffer/soldata/Oving6/gauss_curve_sol.png')
'''
#Del 2
#Hent ut data , vel dag

from pathlib import Path
import pandas as pd

filsti = Path(__file__).resolve().parent / "data" / "Timeseries_59.735_6.756_SA3_36deg_0deg_2018_2018.csv"

df = pd.read_csv(
    filsti,
    skiprows=8,
    skipfooter=9,
    engine="python"
)

df["time"] = pd.to_datetime(
    df["time"],
    format="%Y%m%d:%H%M",
    utc=True
)

df["time"] = pd.to_datetime(
    df["time"],
    format="%Y%m%d:%H%M")

solDag = df[df["time"].dt.dayofyear == 182].copy()

solDag["time"] = solDag["time"].dt.round("h")

solDag = solDag[["time", "G(i)"]]

solDag.to_csv("solDag_2018.csv", index=False, sep=";", decimal=",")
#new figure
#
'''
plt.figure()
t_dag = np.linspace(0, 23, len(solDag))
print(df.dtypes)
plt.plot(t_dag, solDag["G(i)"])
plt.plot(t, gauss_curve(t, solDag["G(i)"].max(), find_peaks(solDag["G(i)"])[0][0], 2.5))

plt.xlabel('Tid (t)')
plt.ylabel('G(i)')
plt.title('Solstråling G(i)')

#Skriv til fil
plt.savefig('elk330/elk330_project/Kristoffer/soldata/Oving6/solstråling.png')
#print all paramaters
print(f"Max: {solDag['G(i)'].max()}, Peak: {find_peaks(solDag['G(i)'])[0][0]}, Std: {solDag['G(i)'].std()}")
'''