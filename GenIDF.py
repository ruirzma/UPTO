from geomeppy import IDF
import pandas as pd
import geopandas as gpd
from shapely import wkt
import rdflib 
from rdflib import RDF, Namespace, URIRef, Literal, OWL ,XSD


iddfile = r'C:\EnergyPlusV9-0-1\Energy+.idd'
idffile = r'C:\EnergyPlusV9-0-1\ExampleFiles\Minimal.idf'
IDF.setiddname(iddfile)
idf = IDF(idffile)


# Load TTL dataset
graph = rdflib.Graph()
graph.parse("sample_data.ttl", format="turtle")
names = Namespace("http://www.urbanpatchtopologyontology.org/upto#")


# URIRef
UrbanTile_Num_URI = URIRef(names["UrbanTile_0"])
containsBuilding = URIRef(names["containsBuilding"])
hasTileNeighbor = URIRef(names["hasTileNeighbor"])
hasGeometry = URIRef(names["hasGeometry"])
hasHeight = URIRef(names["hasHeight"])

# Get the internal building in the target UrbanTile
target_Building_list = list(graph.objects(subject= UrbanTile_Num_URI, predicate= containsBuilding))

# Add these buildings in the IDF
for target_Building_URI in target_Building_list:

    geom = wkt.loads(str(list(graph.objects(subject= target_Building_URI, predicate= hasGeometry))[0]))
    height = float(str(list(graph.objects(subject= target_Building_URI, predicate= hasHeight))[0]))
    idf.add_block(name = 'Building' + str(str(target_Building_URI)[47:]),coordinates = list(geom.exterior.coords) ,num_stories = 1,height = height)

# default construction settings
idf.set_default_constructions()

# intersect and match function
idf.intersect_match()

# Set WWR
idf.set_wwr(wwr = 0.5)

# Add surrounding surfaces in the IDF
def build_shading_buildings(polygon_coordinates, height, bldg_ID):    
    for shading_num in range(len(polygon_coordinates)):
        if shading_num < len(polygon_coordinates)-1:
            idf.newidfobject('SHADING:BUILDING:DETAILED'.upper())
            SHADING_BUILDING_DETAILED = idf.idfobjects['SHADING:BUILDING:DETAILED'.upper()][-1]
            SHADING_BUILDING_DETAILED.Name = 'SHADING Bldg'+ str(bldg_ID) + 'Sur' +str(shading_num)
            SHADING_BUILDING_DETAILED.Number_of_Vertices = 4

            SHADING_BUILDING_DETAILED.Vertex_1_Xcoordinate = polygon_coordinates[shading_num][0]
            SHADING_BUILDING_DETAILED.Vertex_1_Ycoordinate = polygon_coordinates[shading_num][1]
            SHADING_BUILDING_DETAILED.Vertex_1_Zcoordinate = 0

            SHADING_BUILDING_DETAILED.Vertex_2_Xcoordinate = polygon_coordinates[shading_num +1][0]
            SHADING_BUILDING_DETAILED.Vertex_2_Ycoordinate = polygon_coordinates[shading_num +1][1]
            SHADING_BUILDING_DETAILED.Vertex_2_Zcoordinate = 0

            SHADING_BUILDING_DETAILED.Vertex_3_Xcoordinate = polygon_coordinates[shading_num +1][0]
            SHADING_BUILDING_DETAILED.Vertex_3_Ycoordinate = polygon_coordinates[shading_num +1][1]
            SHADING_BUILDING_DETAILED.Vertex_3_Zcoordinate = height

            SHADING_BUILDING_DETAILED.Vertex_4_Xcoordinate = polygon_coordinates[shading_num][0]
            SHADING_BUILDING_DETAILED.Vertex_4_Ycoordinate = polygon_coordinates[shading_num][1]
            SHADING_BUILDING_DETAILED.Vertex_4_Zcoordinate =height

        # if lost the last edge
        if shading_num == len(polygon_coordinates)-1 and shading_num == 3 :
            idf.newidfobject('SHADING:BUILDING:DETAILED'.upper())
            SHADING_BUILDING_DETAILED = idf.idfobjects['SHADING:BUILDING:DETAILED'.upper()][-1]
            SHADING_BUILDING_DETAILED.Name = 'SHADING Bldg'+ str(bldg_ID) + 'Sur' +str(shading_num)
            SHADING_BUILDING_DETAILED.Number_of_Vertices = 4

            SHADING_BUILDING_DETAILED.Vertex_1_Xcoordinate = polygon_coordinates[shading_num][0]
            SHADING_BUILDING_DETAILED.Vertex_1_Ycoordinate = polygon_coordinates[shading_num][1]
            SHADING_BUILDING_DETAILED.Vertex_1_Zcoordinate = 0

            SHADING_BUILDING_DETAILED.Vertex_2_Xcoordinate = polygon_coordinates[0][0]
            SHADING_BUILDING_DETAILED.Vertex_2_Ycoordinate = polygon_coordinates[0][1]
            SHADING_BUILDING_DETAILED.Vertex_2_Zcoordinate = 0

            SHADING_BUILDING_DETAILED.Vertex_3_Xcoordinate = polygon_coordinates[0][0]
            SHADING_BUILDING_DETAILED.Vertex_3_Ycoordinate = polygon_coordinates[0][1]
            SHADING_BUILDING_DETAILED.Vertex_3_Zcoordinate = height

            SHADING_BUILDING_DETAILED.Vertex_4_Xcoordinate = polygon_coordinates[shading_num][0]
            SHADING_BUILDING_DETAILED.Vertex_4_Ycoordinate = polygon_coordinates[shading_num][1]
            SHADING_BUILDING_DETAILED.Vertex_4_Zcoordinate = height
            
# Get the TileNeighbor
TileNeighbor_list  = list(graph.objects(subject= UrbanTile_Num_URI, predicate= hasTileNeighbor))
for TileNeighbor_URI in TileNeighbor_list:

    shading_Building_list = list(graph.objects(subject= TileNeighbor_URI, predicate= containsBuilding))

    for shading_Building_URI in shading_Building_list:

        geom = wkt.loads(str(list(graph.objects(subject= shading_Building_URI, predicate= hasGeometry))[0]))
        height = float(str(list(graph.objects(subject= shading_Building_URI, predicate= hasHeight))[0]))
        
        build_shading_buildings(polygon_coordinates = list(geom.exterior.coords), height = height, bldg_ID = str(shading_Building_URI)[47:])
        
# Weather file
idf.epw = "XXX_TMY3.epw"   

# Run
idf.run()

# Save the IDF file
idf.save('XXX.idf')

# More IDF settings can be found in Geomeppy Doc. 
# https://geomeppy.readthedocs.io/en/latest/