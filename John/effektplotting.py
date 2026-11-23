# Kode for å plotte sammenlignede csv filer

import matplotlib.pyplot as plt
import pandas as pd

df_med_bat = pd.read_csv(
    "C:/Users/johnh/Documents/GitHub/elk330_project/John/csv_grid_med_bat_3dag_utensol.csv", 
    sep = ";", 
    decimal = ",",
    skiprows=1
)

df_uten_bat = pd.read_csv(
    "C:/Users/johnh/Documents/GitHub/elk330_project/John/csv_grid_uten_bat_3dag_utensol.csv", 
    sep = ";", 
    decimal = ",",
    skiprows=1
)

df_SOC = pd.read_csv(
    "C:/Users/johnh/Documents/GitHub/elk330_project/John/csv_grid_med_bat_3dag_utensol_SOC.csv", 
    sep = ";", 
    decimal = ",",
    skiprows=1
)


df_med_bat["Time"] = pd.to_datetime(
    df_med_bat["Time"], 
    format = "%Y.%m.%d %H:%M:%S"
)

df_uten_bat["Time"] = pd.to_datetime(
    df_uten_bat["Time"], 
    format = "%Y.%m.%d %H:%M:%S"
)

df_SOC["Time"] = pd.to_datetime(
    df_SOC["Time"], 
    format = "%Y.%m.%d %H:%M:%S"
)


df_med_bat = df_med_bat.set_index("Time")
df_uten_bat = df_uten_bat.set_index("Time")
df_SOC = df_SOC.set_index("Time")



#plt.plot(df_uten_bat, label = "Effekt uten batteri", color = "red", linestyle = "--")
#plt.plot(df_med_bat, label = "Effekt med batteri", color = "green")
#plt.legend()
#plt.axhline(y=0, color="black", linestyle="--")
#plt.title("Effekt fra eksternt nett med og uten batteri")
#plt.xlabel("Tid")
#plt.ylabel("Effekt")
#plt.grid(True)
#plt.show()

fig, ax1 = plt.subplots()

# Effekt på venstre akse
ax1.plot(df_uten_bat, label="Effekt uten batteri", color="tab:red", linestyle ="--")
ax1.plot(df_med_bat, label="Effekt med batteri", color="tab:green")
ax1.set_xlabel("Tid")
ax1.set_ylabel("Effekt [kW]")
ax1.grid(True)

# SOC på høyre akse
ax2 = ax1.twinx()
ax2.plot(df_SOC, label="SOC",
         color="tab:blue", linestyle="--", linewidth = 0.5)
ax2.set_ylabel("SOC [%]", color="tab:blue")
ax2.tick_params(axis="y", labelcolor="tab:blue")
ax2.set_ylim(0, 100)

# Felles tegnforklaring
linjer1, navn1 = ax1.get_legend_handles_labels()
linjer2, navn2 = ax2.get_legend_handles_labels()
ax1.legend(linjer1 + linjer2, navn1 + navn2)

fig.tight_layout()
plt.show()