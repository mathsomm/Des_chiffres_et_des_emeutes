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
            dfs.append(df)

        df_tot = pd.concat(dfs, axis=1)
        df_tot = df_tot.reset_index().rename(columns={"time [UTC]": "Time"})

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
        self.data = df
        return df

    def add_average(self, df):
        df["mean"] = df.mean(axis=1, numeric_only=True)
        self.data = df
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

        Trends(request_delay=2.5)
        df = self.get_trends(mots, geo="FR", timeframe=date)
        print("data récupérées")
        df = self.normalisation(df)
        df = self.add_average(df)

        self.data = df
        self.time_period = date
        return df[["mean", "Time"]]
    ############### COMPARER GT et GDELT #################
    def comparer_GDELT(self, df_gdelt, aggregation_periode = "3D", afficher=False):
        df_gdelt['observed_at'] = pd.to_datetime(df_gdelt['observed_at']).dt.tz_localize(None)

        # Pour aggréger par x jours ( mettre "xD" en periode ou 'W-SUN' pour une semaine)

        df_gdelt_weekly = (
            df_gdelt
            .resample(str(aggregation_periode), on='observed_at')
            .size()
            .reset_index(name='nb_emeutes')
        )


        if afficher: self.comparer_GDELT_plot(df_gdelt_weekly)
        return df_gdelt_weekly


    def comparer_GDELT_plot(self, df_gdelt):
        df_trends = self.data
        fig, ax1 = plt.subplots(figsize=(12, 6))

        # Courbe 1 axe de gauche
        color1 = 'tab:blue'
        ax1.set_xlabel('Time')
        ax1.set_ylabel('Mentions GDELT', color=color1, fontweight='bold')
        line1 = ax1.plot(df_gdelt['Time'], df_gdelt['nb_emeutes'], color=color1, label='Mentions GDELT', linewidth=2)
        ax1.tick_params(axis='y', labelcolor=color1)

        ax2 = ax1.twinx()

        color2 = 'tab:red'
        ax2.set_ylabel('Indice Google Trends (0-100)', color=color2, fontweight='bold')
        line2 = ax2.plot(df_trends['Time'], df_trends['mean'], color=color2, linestyle='--', label='Google Trends', linewidth=2)
        ax2.tick_params(axis='y', labelcolor=color2)

        # Légendes
        lines = line1 + line2
        labels = [l.get_label() for l in lines]
        ax1.legend(lines, labels, loc='upper left')

        plt.title('Évolution comparée : Mentions GDELT vs Recherches Google Trends')
        ax1.grid(True, alpha=0.3)
        fig.tight_layout()  # Évite que le label de droite soit coupé
        plt.savefig("ComparaisonGtrendDGELT.png")
        plt.show()




#Remarque: mots sensibles aux majuscules (peu) et sg/pluriel (plus de variance, le sg a plus d'occurence)
# mais pas aux accents.
# On ne garde que des mots cohérents avec le contexte de l'étude et évite les mots à double sens

