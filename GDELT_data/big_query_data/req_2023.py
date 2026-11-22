'''
ce script est une requete googlecloud bigquery en passant par un compte de services
requete : données émeutes, en France, depuis janvier 2023
stockage : format parquet, via s3://vgounot/diffusion/

config :
    pip install google-cloud-bigquery db-dtypes
    nécessite une clé json associée à un compte de services : s3://vgounot/ (accès perso)

warning :
    BigQuery Storage module not found, fetch data with the REST endpoint instead
'''


def estimation_donnees_scannees(req):
    """
    estimation cout donnée scannée pour une requete sql donnée
    entrée :
    req, la requete à estimer
    sortie :
    le nombre d'octets scannés
    """
    cfg = bigquery.QueryJobConfig(
        dry_run=True,
        use_query_cache=False)
    job = client.query(req, job_config=cfg)
    estim = job.total_bytes_processed
    print(f"{estim / 1e9:.2f} Go lus")
    return estim


def requete(req, limite=10**11):
    '''
    requete via Google BigQuery si le volume de données scannées est acceptable
    entrée :
    req, la requete
    limite, la limite de données scannées
    '''
    scan = estimation_donnees_scannees(req)
    if scan < limite:
        df = client.query(req).to_dataframe()
        print(df.head())
        PATH = "vgounot/diffusion/2023_gcloud_emeutes2.parquet"
        with fs.open(PATH, "wb") as f:
            df.to_parquet(f, index=False)
        print(f"l'estimation des données scannées est acceptable \n le résultat est disponible au format parquet à l'adresse {PATH}")
    else:
        print(f"l'estimation des données scannées dépasse {limite} octets test")
