
import requests
import folium
from folium import Map, Marker, Popup, TileLayer
import pandas as pd
import numpy as np
import streamlit as st
from streamlit_folium import st_folium

STAC_API_URL = "https://earth.gov/ghgcenter/api/stac"
RASTER_API_URL = "https://earth.gov/ghgcenter/api/raster"
collection_name = "lpjeosim-wetlandch4-monthgrid-v2"

collection = requests.get(f"{STAC_API_URL}/collections/{collection_name}").json()
print(collection)

def get_item_count(collection_id):
    count = 0
    items_url = f"{STAC_API_URL}/collections/{collection_id}/items"

    while True:
        response = requests.get(items_url)

        if not response.ok:
            print("Error getting items")
            exit()

        stac = response.json()
        count += int(stac["context"].get("returned", 0))
        next = [link for link in stac["links"] if link["rel"] == "next"]

        if not next:
            break
        items_url = next[0]["href"]

    return count

# Get the number of items in the collection
number_of_items = get_item_count(collection_name)
items = requests.get(f"{STAC_API_URL}/collections/{collection_name}/items?limit={number_of_items}").json()["features"]
print(f"Found {len(items)} items")

# Convert items into a dictionary with date keys
items_dict = {item["properties"]["start_datetime"][:10]: item for item in items}
print("Available dates in items:", items_dict.keys())



def makeMap(year, month, transparency, color):    
    # Use a specific date (change as needed)
    specific_date = f"{year}-{month}-01"  # Example date
    if specific_date in items_dict:
        asset_name = "ensemble-mean-ch4-wetlands-emissions"

        rescale_values = {
            "max": items_dict[specific_date]["assets"][asset_name]["raster:bands"][0]["histogram"]["max"],
            "min": items_dict[specific_date]["assets"][asset_name]["raster:bands"][0]["histogram"]["min"]
        }

        ensemble_tile = requests.get(
            f"{RASTER_API_URL}/collections/{items_dict[specific_date]['collection']}/items/{items_dict[specific_date]['id']}/tilejson.json?"
            f"&assets={asset_name}"
            f"&color_formula=gamma+r+1.05&colormap_name={color}"  
            f"&color_formula=gamma+r+1.05&rescale={rescale_values['min']},{rescale_values['max']}"
            f"&resolution=high"
        ).json()

        print(ensemble_tile)


        map_ = folium.Map(location=(34, -118), zoom_start=6)

        map_layer = TileLayer(
            tiles=ensemble_tile["tiles"][0],
            attr="GHG",
            opacity=transparency,
            name="CH4 Emissions Layer",  
            show=True
        )
        map_layer.add_to(map_)


        map_.save("ensemble_mean_map.html")
        #webbrowser.open("ensemble_mean_map.html")

        theMap = "ensemble_mean_map.html"
        return theMap
    
#webbrowser.open(makeMap(2022,10))
