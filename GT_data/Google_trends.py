
import pandas as pd
from trendspy import Trends
import matplotlib.pyplot as plt


class Google_Trends:

    def get_trends(self, mots, timeframe="today 5-y", geo="FR"):
        print("Récupération de trends pour: ", mots)
        tr = Trends()

        locations = tr.geo(find='courbevoie', language='fr')
        print("Lieu:", locations)


        df = tr.interest_over_time(mots, timeframe=timeframe, geo=geo)
        if not df.empty:
            df = df.drop(columns=["isPartial"])
        return df
    
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
    
    def plot(self, df):
        if "Date" in df.columns:
            df.set_index("Date", inplace=True)
        for col in df.columns:
            plt.plot(df.index, df[col], label=col, linewidth=2)

        plt.title("Évolution de l'intérêt sur Google Trends", fontsize=14)
        plt.xlabel("Date")
        plt.ylabel("Intérêt (0 à 100)")
        plt.legend(title="Mots-clés", loc="upper left")
        plt.grid(True, linestyle="--", alpha=0.6)
        

        plt.show()

GT = Google_Trends()
df = GT.get_trends(["Emeute", "mortier", 'manifestation'], geo = "FR")
df = GT.normalisation(df)
GT.plot(df)
