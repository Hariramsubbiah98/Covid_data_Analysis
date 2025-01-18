import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from plotly.subplots import make_subplots as ms

def load_data(path):
    try:
        return pd.read_csv(path)
    except FileNotFoundError as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    covid_df = load_data("D:\\python_scripts\\project\\Data_analytical\\Covid_project\\DataSet\\covid_19_india.csv")
    vaccine_df = load_data("D:\\python_scripts\\project\\Data_analytical\\Covid_project\\DataSet\\covid_vaccine_statewise.csv")
    covid_df.drop(["Sno","ConfirmedIndianNational","ConfirmedForeignNational","Time"],inplace=True,axis=1)
    covid_df["Date"] = pd.to_datetime(covid_df["Date"], format='%Y-%m-%d')
    covid_df["Active_cases"] = covid_df["Confirmed"] - (covid_df["Cured"] - covid_df["Deaths"])
    statewise = pd.pivot_table(covid_df,values=["Confirmed","Cured","Deaths"],index="State/UnionTerritory",aggfunc="max")
    statewise["Recovery_rate"] = statewise["Cured"]*100/statewise["Confirmed"]
    statewise["mortality"] = statewise["Deaths"]*100/statewise["Confirmed"]
    statewise = statewise.sort_values(by="Confirmed",ascending=False)
    top_10_active_cases = (
        covid_df.groupby(by="State/UnionTerritory", as_index=False)
        .max()[["State/UnionTerritory", "Active_cases", "Date"]]
        .sort_values(by="Active_cases", ascending=False)
        .reset_index(drop=True)
    )
    top_10_deaths = (
        covid_df.groupby(by="State/UnionTerritory",as_index=False)
        .max()[["State/UnionTerritory","Deaths","Date"]]
        .sort_values(by=["Deaths"],ascending=False).reset_index()
    )
    vaccine_df.rename(columns={"Updated On":"Vaccine_Date"},inplace=True)
    vaccination = vaccine_df.drop(columns=["Sputnik V (Doses Administered)","AEFI","18-44 Years (Doses Administered)","45-60 Years (Doses Administered)","60+ Years (Doses Administered)"],axis=1)
    vaccine_states = vaccine_df[vaccine_df.State!="India"]
    vaccine_states.rename(columns={"Total Individuals Vaccinated":"Total"},inplace=True)
    max_vacc = vaccine_states.groupby("State")["Total"].sum().to_frame("Total")
    max_vacc = max_vacc.sort_values("Total", ascending=False).tail(5)
    plt.figure(figsize=(10,6))
    plt.title("Top 5 Vaccinated States",size=20)
    plt.title("Top 5 Vaccinated States", size=20)
    sns.barplot(
        data=max_vacc.reset_index(),  
        x="State", 
        y="Total", 
        linewidth=2, 
        edgecolor="black", 
        palette="viridis"  
    )
    plt.xlabel("States")
    plt.ylabel("Vaccination")
    plt.xticks(rotation=45)
    plt.show()