import requests
import time

# class GDELT:

#     def get_data(self, query, mode, structure, timespan, maxrecords):
#         r = requests.get(
#             "https://api.gdeltproject.org/api/v2/doc/doc",
#             params={
#                 "query": query,
#                 "mode": mode,
#                 "format": structure,
#                 "timespan": timespan,
#                 "maxrecords": maxrecords,
#             },
#             timeout=30,
#         )
#         r.headers.get("Retry-After")
#         r.raise_for_status()
#         for a in r.json().get("articles", []):
#             print(a["seendate"], a["domain"], "—", a["title"])


class GDELT:
    URL = "https://api.gdeltproject.org/api/v2/doc/doc"

    def get_data(self, query, mode, structure, timespan, maxrecords, max_retries=5):
        params = {
            "query": query,
            "mode": mode,
            "format": structure,
            "timespan": timespan,
            "maxrecords": maxrecords,
        }

        for attempt in range(max_retries):
            r = requests.get(self.URL, params=params, timeout=300)

            if r.status_code == 429:
                retry_after = r.headers.get("Retry-After")
                print(retry_after)
                try:
                    wait = int(retry_after)            # délai en secondes
                except (TypeError, ValueError):
                    wait = 20 * (attempt + 1)           # repli si absent ou illisible
                print(f"429 (Retry-After={retry_after!r}), attente {wait}s "
                      f"[{attempt + 1}/{max_retries}]")
                time.sleep(wait)
                continue

            r.raise_for_status()
            articles = r.json().get("articles", [])
            for a in articles:
                print(a["seendate"], a["domain"], "—", a["title"])
            return articles

        raise RuntimeError(f"Toujours limité après {max_retries} tentatives")

gd = GDELT()
data = gd.get_data(
    query="sourcelang:french",
    mode="ArtList",
    structure="json",
    timespan="7d",
    maxrecords=5,
    )
