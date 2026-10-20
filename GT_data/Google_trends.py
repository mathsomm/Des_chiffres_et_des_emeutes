
import pandas as pd
from trendspy import Trends
import matplotlib.pyplot as plt


class Google_Trends:

    def get_trends(self, mots, timeframe="today 5-y", geo="FR"):
        print("Récupération de trends pour: ", mots)
        tr = Trends()

        dfs = []
        for i in range(0, len(mots), 5):
            df = tr.interest_over_time(mots[i:i+4], timeframe=timeframe, geo=geo)
            dfs.append(df)

        df_tot = pd.concat(dfs, ignore_index=True)

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
            df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min()) * 100
        return df
    def add_average(self, df):
        df["mean"] = df.mean(axis=1)
        return df
    def plot(self, df, colonnes = None):
        if "Date" in df.columns:
            print("Date")
            df.set_index("Date", inplace=True)
        for col in df.columns:
            if colonnes is None or col in colonnes:
                plt.plot(df.index, df[col], label=col, linewidth=2)

        plt.title("Évolution de l'intérêt sur Google Trends", fontsize=14)
        plt.xlabel("Date")
        plt.ylabel("Intérêt (0 à 100)")
        plt.legend(title="Mots-clés", loc="upper left")
        plt.grid(True, linestyle="--", alpha=0.6)
        plt.show()

GT = Google_Trends()


#Remarque: mots sensibles aux majuscules (peu) et sg/pluriel (plus de variance, le sg a plus d'occurence)
# mais pas aux accents.
# On ne garde que des mots cohérents avec le contexte de l'étude et évite les mots à double sens

mots_contexte = ["Emeute", "violences urbaines"] #, "manifestation", "violence", 
mots_acteurs = ["casseurs"]
mots_actions = ["saccage", 'pillage']
mots_matériel = ["mortier", "LBD"]
mots_de_recherche = mots_contexte #+ mots_acteurs + mots_actions + mots_matériel
# problème avec les dates
df = GT.get_trends(mots_de_recherche, geo = "FR")
df = GT.normalisation(df)
df = GT.add_average(df)
GT.plot(df)
