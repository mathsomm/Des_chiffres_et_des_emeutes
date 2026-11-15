import pandas as pd
from trendspy import Trends, BatchPeriod
import matplotlib.pyplot as plt

class Google_Trends:
    def __init__(self):
        self.data = []
        self.time_period = ""

    def get_trends(self, mots, timeframe="today 5-y", geo="FR"):        
        tr = Trends()

        dfs = []
        for i in range(0, len(mots), 4):
            df = tr.interest_over_time(mots[i:i+4], timeframe=timeframe, geo=geo)
            df = df.reset_index()
            
            dfs.append(df)

        df_tot = pd.concat(dfs, axis=1)
        df_tot = df_tot.rename(columns={"time [UTC]": "Time"})

        if not df_tot.empty:
            df_tot = df_tot.drop(columns=["isPartial"])
        return df_tot
    
    def get_trends_geo(self, mot, timeframe="today 5-y", geo="FR"):
        # City-level data for California
        tr = Trends()
        city_df = tr.interest_by_region(
            mot,
            geo=geo,
            resolution='CITY', 
            timeframe=timeframe
        )
        
        return city_df

    def normalisation(self, df):
        
        for col in df.columns:
            if col == "Time" or col == "isPartial": continue
            df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min()) * 100
        return df

    def add_average(self, df):
        df["mean"] = df.mean(axis=1, numeric_only=True)        
        return df
        
    def plot(self, df, colonnes=None):

        for col in df.columns:
            if col == "Time" or col == "isPartial": continue
            if colonnes is None or col in colonnes:
                plt.plot(df["Time"], df[col], label=col, linewidth=2)

        plt.title("Évolution de l'intérêt sur Google Trends", fontsize=14)
        plt.xlabel("Date")
        plt.ylabel("Intérêt (0 à 100)")
        plt.legend(title="Mots-clés", loc="upper left")
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.show()

    def get_data(self, mots, date="today 5-y"):
        print("Récupération de trends pour: ", mots)

        Trends(request_delay=1.5)
        df = self.get_trends(mots, geo="FR", timeframe=date)
        print("data récupérées")
        df = self.normalisation(df)
        df = self.add_average(df)

        self.data = df
        self.time_period = date
        return df[["mean", "Time"]]



#Remarque: mots sensibles aux majuscules (peu) et sg/pluriel (plus de variance, le sg a plus d'occurence)
# mais pas aux accents.
# On ne garde que des mots cohérents avec le contexte de l'étude et évite les mots à double sens

