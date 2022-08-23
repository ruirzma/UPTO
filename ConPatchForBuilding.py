import geopandas as gpd
import pandas as pd
from shapely import wkt
import osmnx as ox
import rdflib
from rdflib import RDF, Namespace, URIRef, Literal, OWL ,XSD
from rdflib.namespace import OWL, RDF, RDFS
import ast
from .utils import read_csv_to_gdf, add_contains_Tile_Street
from .utils import construct_UPTO_individual

cityName = "XXX"
receptive_radius = 500


tilePath = "%s_urban_tile_gdf_for_UPTO.csv" % cityName
buildingPath = "%s_building_gdf_for_UPTO.csv" % cityName
VGPath = "%s_vegetation_gdf_for_UPTO.csv" % cityName
StreetPath = "%s_street_gdf_for_UPTO.csv" % cityName

# Read the csv
urban_tile_gdf, building_gdf, VG_gdf, street_gdf = read_csv_to_gdf(tilePath, buildingPath, VGPath, StreetPath)

# projection
urban_tile_gdf_prj = ox.project_gdf(urban_tile_gdf)
street_gdf_prj = ox.project_gdf(street_gdf)
building_gdf_prj = ox.project_gdf(building_gdf)

# peripheral region for Patch generation (for Building)
peripheral_gdf_prj = building_gdf_prj 

# Build UrbanPatch DataFrame
urban_patch_gdf_prj = gpd.GeoDataFrame()
contains_tile_list = []
contains_street_list = []

for osmscID_i in building_gdf_prj["osmscID"]:
    # for each patch
    contains_tile_sublist,  contains_street_sublist = add_contains_Tile_Street(peripheral_gdf_prj,
                        urban_tile_gdf_prj, street_gdf_prj, osmscID_i, distance = receptive_radius)
    
    contains_tile_list.append(contains_tile_sublist)
    contains_street_list.append(contains_street_sublist)

# urban_patch_gdf_prj columns
urban_patch_gdf_prj["containsTile"] = contains_tile_list
urban_patch_gdf_prj["containsStreet"] = contains_street_list
urban_patch_gdf_prj["osmscID"] = ["UrbanPatch_" + str(i) for i in range(len(urban_patch_gdf_prj))]


construct_UPTO_individual(cityName, VG_gdf, building_gdf, street_gdf, urban_tile_gdf, urban_patch_gdf_prj)