import pandas as pd
import sqlite3

all_routes = pd.read_csv("data/route_seqs.csv")
db_routes = all_routes[all_routes['Operator'] == "DB"]
db_routes = db_routes.drop(["Operator",
                            "FlagData",
                            "CarouselType"], axis=1)
db_routes.rename(columns={'ShapeId': 'id',
                          'AtcoCode': 'StopID',
                          'PlateCode': 'StopNum',
                          'ShortCommonName_en': 'Name',
                          'ShortCommonName_ga': 'Ainm'}, inplace=True)

db = sqlite3.connect("db.sqlite3")
db_routes.to_sql("bus_routes_busroute", db, if_exists="replace", index=False)
