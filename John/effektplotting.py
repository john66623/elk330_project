# Kode for å plotte sammenlignede csv filer

import matplotlib.pyplot as plt
import pandas as pd

df_med_bat = pd.read_csv(
    "C:/Users/johnh/Documents/GitHub/elk330_project/John/csv_grid_med_bat_3dag.csv", 
    sep = ";", 
    decimal = ","
)

df_uten_bat = pd.read_csv(
    "C:/Users/johnh/Documents/GitHub/elk330_project/John/csv_grid_uten_bat_3dag.csv", 
    sep = ";", 
    decimal = ","
)



df_med_bat["Time"] = pd.to_datetime(
    df_med_bat["Time"], 
    format = "%Y.%m.%d %H:%M:%S"
)

df_uten_bat["Time"] = pd.to_datetime(
    df_uten_bat["Time"], 
    format = "%Y.%m.%d %H:%M:%S"
)



df_med_bat = df_med_bat.set_index("Time")
df_uten_bat = df_uten_bat.set_index("Time")



plt.plot(df_med_bat, label = "Effekt med batteri", color = "green")
plt.plot(df_uten_bat, label = "Effekt uten batteri", color = "red")
plt.legend()
plt.axhline(y=0, color="black", linestyle="--")
plt.title("Effekt fra eksternt nett med og uten batteri")
plt.xlabel("Tid")
plt.ylabel("Effekt")
plt.grid(True)
plt.show()