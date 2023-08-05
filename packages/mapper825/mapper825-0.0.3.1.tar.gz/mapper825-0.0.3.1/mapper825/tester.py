import os
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import plotly.express as px
import geopandas as gpd
from __init__ import mapper, all_aglos
import winsound

pd.set_option('display.max_columns', 500)

gdf = gpd.read_file(r"C:\Users\ofici\Downloads\base_icpag_full_etapas_qgis\base_icpag_full_etapas_qgis\base_icpag_full_etapas_qgis.shp")

for aglo in all_aglos():
    mapper(
        gdf,
        'etap_24_0',
        r'maps_out',
        footnote='Datos basados en la EPH de San justo primo',
        aglo=aglo,
        subfolder=aglo
    )

winsound.MessageBeep()
