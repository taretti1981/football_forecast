import os
from src.aux_functions import *
import pandas as pd
import src.database_management as db_class

# read configuration
config = readConfig()

db = db_class.database_management()
db.get_connection()

# paramters
os.environ['KMP_DUPLICATE_LIB_OK']='True'
current_team_home = "fc-schalke-04"
current_team_visitor = "borussia-dortmund"

current_team_home_data = getData(db,current_team_home)
current_team_visitor_data = getData(db,current_team_visitor)
home_vs_visitor = getDataBetween(db,current_team_home,current_team_visitor)

db.close()

print("Done")