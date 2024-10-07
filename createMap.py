import webbrowser
import requests
import folium
import folium.plugins
from folium import Map, TileLayer
#from pystac_client import Client
import branca
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from streamlit_folium import st_folium

STAC_API_URL = "https://earth.gov/ghgcenter/api/stac"
RASTER_API_URL = "https://earth.gov/ghgcenter/api/raster"

#collection_name = "gosat-based-ch4budget-yeargrid-v1"
collection_name = "lpjeosim-wetlandch4-monthgrid-v2"



collection = requests.get(f"{STAC_API_URL}/collections/{collection_name}").json()
print(collection)

def get_item_count(collection_id):
    count = 0
    items_url = f"{STAC_API_URL}/collections/{collection_id}/items"

    while True:
        response = requests.get(items_url)

        if not response.ok:
            print("error getting items")
            exit()

        stac = response.json()
        count += int(stac["context"].get("returned", 0))
        next = [link for link in stac["links"] if link["rel"] == "next"]

        if not next:
            break
        items_url = next[0]["href"]

    return count

number_of_items = get_item_count(collection_name)
items = requests.get(f"{STAC_API_URL}/collections/{collection_name}/items?limit={number_of_items}").json()["features"]
print(f"Found {len(items)} items")

print(items[0])

items = {item["properties"]["start_datetime"][:10]: item for item in items} 
asset_name = "prior-total"

rescale_values = {"max":items[list(items.keys())[0]]["assets"][asset_name]["raster:bands"][0]["histogram"]["max"], "min":items[list(items.keys())[0]]["assets"][asset_name]["raster:bands"][0]["histogram"]["min"]}

print(items.keys())

print("Available dates in items:")
for date in items.keys():
    print(date)

print("Available keys in items:", items.keys())


month = 10
day = 13


color_map = "rainbow" 
january_2019_tile = requests.get(
    f"{RASTER_API_URL}/collections/{items['2014-10-01']['collection']}/items/{items['2014-10-01']['id']}/tilejson.json?"
    f"&assets={asset_name}"
    f"&color_formula=gamma+r+1.05&colormap_name={color_map}"
    f"&rescale={rescale_values['min']},{rescale_values['max']}"
).json()

print(january_2019_tile)

map_ = folium.Map(location=(34, -118), zoom_start=6)


map_layer_2019 = TileLayer(
    tiles=january_2019_tile["tiles"][0],
    attr="GHG",
    opacity=0.7,
)
map_layer_2019.add_to(map_)

#print(map_)

map_.save("map.html")
webbrowser.open("map.html")


texas_aoi = {
    "type": "Feature",
    "properties": {},
    "geometry": {
        "coordinates": [
            [
                [-95, 29],
                [-95, 33],
                [-104, 33],
                [-104,29],
                [-95, 29]
            ]
        ],
        "type": "Polygon",
    },
}


aoi_map = Map(
    tiles="OpenStreetMap",
    location=[
        30,-100
    ],
    zoom_start=6,
)

folium.GeoJson(texas_aoi, name="Texas, USA").add_to(aoi_map)



aoi_map.save("map1.html")
#webbrowser.open("map1.html")


# Check total number of items available
items = requests.get(
    f"{STAC_API_URL}/collections/{collection_name}/items?limit=300"
).json()["features"]
print(f"Found {len(items)} items")

print(items[0])

def generate_stats(item, geojson):
    result = requests.post(
        f"{RASTER_API_URL}/cog/statistics",
        params={"url": item["assets"][asset_name]["href"]},
        json=geojson,
    ).json()
    return {
        **result["properties"],
        "datetime": item["properties"]["start_datetime"][:10],
    }

stats = [generate_stats(item, texas_aoi) for item in items]
print(stats[0])

def clean_stats(stats_json) -> pd.DataFrame:
    df = pd.json_normalize(stats_json)
    df.columns = [col.replace("statistics.b1.", "") for col in df.columns]
    df["date"] = pd.to_datetime(df["datetime"])
    return df


df = clean_stats(stats)
df.head(5)


tile_2016 = requests.get(
    f"{RASTER_API_URL}/collections/{items[0]['collection']}/items/{items[0]['id']}/tilejson.json?"
    f"&assets={asset_name}"
    f"&color_formula=gamma+r+1.05&colormap_name={color_map}"
    f"&rescale={rescale_values['min']},{rescale_values['max']}",
).json()
print(tile_2016)

# Use bbox initial zoom and map
# Set up a map located w/in event bounds

aoi_map_bbox = Map(
    tiles="OpenStreetMap",
    location=[
        30,-100
    ],
    zoom_start=8,
)

map_layer = TileLayer(
    tiles=tile_2016["tiles"][0],
    attr="GHG", opacity = 0.5
)

map_layer.add_to(aoi_map_bbox)

theMap = "map3.html"



aoi_map_bbox.save(theMap)
webbrowser.open(theMap)

st.title("Folium Map")


st_folium(aoi_map, width=2000, height=600)