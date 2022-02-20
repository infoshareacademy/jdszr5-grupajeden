# Imports
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import missingno as msno
import scikitplot as skplt
from sklearn.impute import SimpleImputer
import ipywidgets as widgets
from IPython.display import display, clear_output

# Importing data
df = pd.read_csv("household_power_consumption.txt", sep = ";", low_memory=False)

# Renaming columns
df.columns = ["Date", "Time", "Active_power", "Reactive_power", 
              "Voltage", "Intensity", "Kitchen", "Laundry", "Heater"]

# Conversions
columns_float = df.columns.drop(["Date","Time"])
df[columns_float] = df[columns_float].apply(pd.to_numeric, errors="coerce")

df["Date_time"] = pd.to_datetime(df["Date"] + df["Time"], format="%d/%m/%Y%H:%M:%S")
df = df.drop(columns=["Date", "Time"])

# Removal of incomplete months
df = df[df.Date_time < pd.to_datetime("2010-11-01")]
df = df[df.Date_time >= pd.to_datetime("2007-01-01")]

# Index reset
df = df.reset_index(drop=True)

# Creating df with NaNs
df_nan = df.copy(deep=True)

# Imputing most frequent values
imputer = SimpleImputer(missing_values=np.nan, strategy="most_frequent")

df["Active_power"] = imputer.fit_transform(df[["Active_power"]])
df["Reactive_power"] = imputer.fit_transform(df[["Reactive_power"]])
df["Voltage"] = imputer.fit_transform(df[["Voltage"]])
df["Intensity"] = imputer.fit_transform(df[["Intensity"]])
df["Kitchen"] = imputer.fit_transform(df[["Kitchen"]])
df["Laundry"] = imputer.fit_transform(df[["Laundry"]])
df["Heater"] = imputer.fit_transform(df[["Heater"]])

# Watts to killowats
df["Kitchen"] = df["Kitchen"].div(1000)
df["Laundry"] = df["Laundry"].div(1000)
df["Heater"] = df["Heater"].div(1000)

# Changing minutes into hours
df = df.resample("D", on="Date_time").agg({"Active_power": "sum", 
                                           "Reactive_power": "sum",
                                           "Voltage": "mean",
                                           "Intensity": "mean",
                                           "Kitchen": "sum",
                                           "Laundry": "sum",
                                           "Heater": "sum"}).reset_index()

# Summing up energy consumption
sum_of_energy = df["Kitchen"]+df["Laundry"]+df["Heater"]
df["Sum_of_energy"] = sum_of_energy

# Adding new columns
df["Hour"] = df.Date_time.dt.hour
df["Day"] = df.Date_time.dt.day
df["Day_of_year"] = df.Date_time.dt.dayofyear
df["Weekday"] = df.Date_time.dt.weekday
df["Month"] = df.Date_time.dt.month
df["Year"] = df.Date_time.dt.year
df["Weekend"] = df["Weekday"].apply(lambda x: 0 if x <5 else 1)

seasons = [4, 4, 1, 1, 1, 2, 2, 2, 3, 3, 3, 4]
months_to_seasons = dict(zip(range(1,13), seasons))
df["Season"] = df.Month.map(months_to_seasons)

# Adding energy costs
def add_avg_cost(row):
    if row["Year"] == 2007:
        if row["Month"] == 1:
            return 10.06
        elif row["Month"] == 2:
            return 9.89
        elif row["Month"] == 3:
            return 10.27
        elif row["Month"] == 4:
            return 10.63
        elif row["Month"] == 5:
            return 10.77
        elif row["Month"] == 6:
            return 11.09
        elif row["Month"] == 7:
            return 11.07
        elif row["Month"] == 8:
            return 11.07
        elif row["Month"] == 9:
            return 10.96
        elif row["Month"] == 10:
            return 10.82
        elif row["Month"] == 11:
            return 10.70
        elif row["Month"] == 12:
            return 10.33
    elif row["Year"] == 2008:
        if row["Month"] == 1:
            return 10.14
        elif row["Month"] == 2:
            return 10.16
        elif row["Month"] == 3:
            return 10.45
        elif row["Month"] == 4:
            return 10.93
        elif row["Month"] == 5:
            return 11.40
        elif row["Month"] == 6:
            return 11.77
        elif row["Month"] == 7:
            return 12.07
        elif row["Month"] == 8:
            return 12.09
        elif row["Month"] == 9:
            return 11.92
        elif row["Month"] == 10:
            return 11.81
        elif row["Month"] == 11:
            return 11.42
        elif row["Month"] == 12:
            return 10.86
    elif row["Year"] == 2009:
        if row["Month"] == 1:
            return 10.98
        elif row["Month"] == 2:
            return 11.18
        elif row["Month"] == 3:
            return 11.28
        elif row["Month"] == 4:
            return 11.50
        elif row["Month"] == 5:
            return 11.78
        elif row["Month"] == 6:
            return 11.81
        elif row["Month"] == 7:
            return 11.85
        elif row["Month"] == 8:
            return 11.94
        elif row["Month"] == 9:
            return 11.96
        elif row["Month"] == 10:
            return 11.65
        elif row["Month"] == 11:
            return 11.26
        elif row["Month"] == 12:
            return 10.90
    elif row["Year"] == 2010:
        if row["Month"] == 1:
            return 10.89
        elif row["Month"] == 2:
            return 11.11
        elif row["Month"] == 3:
            return 11.11
        elif row["Month"] == 4:
            return 11.71
        elif row["Month"] == 5:
            return 11.91
        elif row["Month"] == 6:
            return 11.91
        elif row["Month"] == 7:
            return 12.04
        elif row["Month"] == 8:
            return 12.03
        elif row["Month"] == 9:
            return 11.95
        elif row["Month"] == 10:
            return 11.86
        
df["Avg_cost"] = df.apply(lambda row: add_avg_cost(row), axis=1)

# Adding daily energy cost
df["Sum_cost"] = df["Sum_of_energy"] * df["Avg_cost"]

# Creating new data frame with date as an index
df_date = df.copy(deep=True)
df_date.index = df_date["Date_time"]
df_date = df_date.drop(columns=["Date_time", "Hour", "Day", "Day_of_year", 
                       "Weekday", "Month", "Year", "Weekend", "Season", "Avg_cost"])

def main():
    with out:
        clear_output()
        show_widget_visual()
    display(out)

# Buttons output
out = widgets.Output()

# Visual widget function
def show_widget_visual():
    display(my_choice_widget_visual, handler_out_visual)
    
# Visual choice function
def my_choice_handler_visual(widget_value):
    if widget_value == "...":
        pass
    elif widget_value == "Matryca Nanów":
        nan_matrix = msno.matrix(df_nan)
    elif widget_value == "Heatmapa korelacji":
        correlation_matrix = np.round(df.corr(), 3)
        sns.set(rc={"figure.figsize":(18,14)})
        color_map = sns.diverging_palette(240, 10, n=10)
        heatmap = sns.heatmap(correlation_matrix, cmap=color_map, annot=True, square=True);
    elif widget_value == "Wykresy wszystkich zmiennych":
        fig, ax = plt.subplots(figsize = (20,24))
        for i in range(len(df_date.columns)):
            plt.subplot(len(df_date.columns),1,i+1)
            name = df_date.columns[i]
            plt.plot(df_date[name])
            plt.title(name,y = 0,loc = "left")
            plt.yticks([])
        fig.tight_layout()
        plt.show()
    elif widget_value == "Dzienne zużycie prądu":
        df_date.Sum_of_energy.resample("D").sum().plot(figsize=(20,6),title="Dzienne zużycie prądu:", fontsize=15)
        plt.xlabel("Zakres dat", fontsize=17)
        plt.ylabel("Zużycie prądu", fontsize=17)
        plt.tight_layout()
        plt.show() 
    elif widget_value == "Miesięczne zużycie prądu":
        df_date.Sum_of_energy.resample("M").sum().plot(kind="bar", figsize=(12,6),
                                                       title="Miesięczne zużycie prądu:")
        plt.xlabel("Zakres dat", fontsize=17)
        plt.ylabel("Zużycie prądu", fontsize=17)
        plt.tight_layout()
        plt.show()
    elif widget_value == "Kwartalne zużycie prądu":
        df_date.Sum_of_energy.resample("Q").sum().plot(kind="bar", figsize=(12,6),
                                                       title="Kwartalne zużycie prądu:")
        plt.xlabel("Zakres dat", fontsize=17)
        plt.ylabel("Zużycie prądu", fontsize=17)
        plt.tight_layout()
        plt.show()
    elif widget_value == "Zużycie prądu rok do roku":
        years = ["2007", "2008", "2009", "2010"]
        fig, ax = plt.subplots(figsize = (28,28))
        for i in range(len(years)):
            plt.subplot(len(df_date.columns),1, i+1)
            year = years[i]
            sum_of_energy_data = df_date[str(year)]["Sum_of_energy"]
            plt.plot(sum_of_energy_data)
        plt.show()
    elif widget_value == "Zużycie oraz koszt na przestrzeni lat":
        plt.figure(figsize=(15,5))
        plt.title("Zużycie prądu na przestrzeni lat:", y=1.015)
        sns.barplot(x="Month", y="Sum_of_energy", hue="Year", data=df)
        plt.xlabel("Zakres dat", fontsize=15)
        plt.ylabel("Zużycie prądu", fontsize=15)
        plt.legend(loc="lower right")
        plt.show()

        plt.figure(figsize=(15,5))
        plt.title("Koszt prądu na przestrzeni lat:", y=1.015)
        sns.barplot(x="Month", y="Sum_cost", hue="Year", data=df)
        plt.xlabel("Zakres dat", fontsize=15)
        plt.ylabel("Koszt prądu", fontsize=15)
        plt.legend(loc="lower right")
        plt.show()
        
my_choice_widget_visual = widgets.Dropdown(options=["...", \
                                                    "Matryca Nanów", "Heatmapa korelacji", 
                                                    "Wykresy wszystkich zmiennych",
                                                    "Dzienne zużycie prądu",
                                                    "Miesięczne zużycie prądu",
                                                    "Kwartalne zużycie prądu",
                                                    "Zużycie prądu rok do roku",
                                                    "Zużycie oraz koszt na przestrzeni lat"])
handler_out_visual = widgets.interactive_output(my_choice_handler_visual, \
                                                {"widget_value": my_choice_widget_visual})

main()