# Construct UrbanPatch individuals for UrbanTile objects when changing the receptive radius
import geopandas as gpd
import pandas as pd
from shapely import wkt
import osmnx as ox
import rdflib
from rdflib import RDF, Namespace, URIRef, Literal, OWL ,XSD
from rdflib.namespace import OWL, RDF, RDFS
import ast

names = Namespace("http://www.urbanpatchtopologyontology.org/upto#")
# URIRef
Building = URIRef(names["Building"])
Vegetation = URIRef(names["Vegetation"])
Street = URIRef(names["Street"])
UrbanTile = URIRef(names["UrbanTile"])
UrbanPatch = URIRef(names["UrbanPatch"])
# UrbanPatch
containsTile = URIRef(names["containsTile"])
containsStreet = URIRef(names["containsStreet"])
hasAvgBuildingHeight  = URIRef(names["hasAvgBuildingHeight"])
hasBuildingDensity = URIRef(names["hasBuildingDensity"])
hasVegetationDensity =  URIRef(names["hasVegetationDensity"])
hasVerticalToHorizontalRatio = URIRef(names["hasVerticalToHorizontalRatio"])
# UrbanTile
containsBuilding = URIRef(names["containsBuilding"])
containsVegetation = URIRef(names["containsVegetation"])
withinPatch = URIRef(names["withinPatch"])
hasTileNeighbor = URIRef(names["hasTileNeighbor"])
hasStreetNeighbor = URIRef(names["hasStreetNeighbor"])
hasGeometry = URIRef(names["hasGeometry"])
hasArea = URIRef(names["hasArea"])
hasPerimeter = URIRef(names["hasPerimeter"])
# Building
withinTile = URIRef(names["withinTile"])
hasHeight = URIRef(names["hasHeight"])
hasBuildingType = URIRef(names["hasBuildingType"])


def read_csv_to_gdf(tilePath, buildingPath, VGPath, StreetPath):

    urban_tile_df = pd.read_csv(tilePath)
    urban_tile_df['geometry'] = urban_tile_df['geometry'].apply(wkt.loads)
    urban_tile_gdf = gpd.GeoDataFrame(urban_tile_df, crs = "epsg:4326")

    building_df = pd.read_csv(buildingPath)
    building_df['geometry'] = building_df['geometry'].apply(wkt.loads)
    building_gdf = gpd.GeoDataFrame(building_df, crs = "epsg:4326")

    VG_df = pd.read_csv(VGPath)
    VG_df['geometry'] = VG_df['geometry'].apply(wkt.loads)
    VG_gdf = gpd.GeoDataFrame(VG_df, crs = "epsg:4326")

    street_df = pd.read_csv(StreetPath)
    street_df['geometry'] = street_df['geometry'].apply(wkt.loads)
    street_gdf = gpd.GeoDataFrame(street_df, crs = "epsg:4326")

    urban_tile_gdf["osmscID"] = ["UrbanTile_" + str(i) for i in range(len(urban_tile_gdf))]
    return urban_tile_gdf, building_gdf, VG_gdf, street_gdf


def add_contains_Tile_Street(peripheral_gdf_prj, urban_tile_gdf_prj, street_gdf_prj, osmscID_i, distance = 500):
    

    peripheral_region = gpd.GeoDataFrame()
    peripheral_region["geometry"] = [list(peripheral_gdf_prj[peripheral_gdf_prj["osmscID"]== osmscID_i].geometry)[0].centroid.buffer(distance)]
    peripheral_region.crs = peripheral_gdf_prj.crs
    
    # intersected Tile objects
    tile_temp_relationship =  gpd.sjoin(peripheral_region, urban_tile_gdf_prj, how="left", op="intersects")
    # ID of intersected Tile objects
    contains_tile_sublist = [osmscID for osmscID in tile_temp_relationship["osmscID"]] 
    
    # intersected Street objects
    street_temp_relationship =  gpd.sjoin(peripheral_region, street_gdf_prj, how="left", op="intersects")
    # ID of intersected Street objects
    contains_street_sublist = [osmscID for osmscID in street_temp_relationship["osmscID"]]     
    
    
    return contains_tile_sublist,  contains_street_sublist

# Street
def add_Street_Individual(graph, Street_Num, street_gdf):
        
    Street_Num_URI = URIRef(names[Street_Num])

    graph.add((Street_Num_URI, RDF.type, OWL.NamedIndividual))
    graph.add((Street_Num_URI, RDF.type, Street)) 

    graph.add((Street_Num_URI, hasArea , 
            Literal(list(street_gdf[street_gdf["osmscID"] == Street_Num].Street_area)[0], 
                    datatype = XSD["decimal"]))) 

    graph.add((Street_Num_URI, hasPerimeter , 
            Literal(list(street_gdf[street_gdf["osmscID"] == Street_Num].Street_perimeter)[0], 
                    datatype = XSD["decimal"]))) 

    # geometry
    geom_str = str(list(street_gdf[street_gdf["osmscID"] == Street_Num].geometry)[0])
    graph.add((Street_Num_URI, hasGeometry, Literal(geom_str, datatype = XSD["string"])))     

# Building 
def add_Building_Individual(graph, Building_Num, building_gdf):
        
    Building_Num_URI = URIRef(names[Building_Num])

    graph.add((Building_Num_URI, RDF.type, OWL.NamedIndividual))
    graph.add((Building_Num_URI, RDF.type, Building)) 

    graph.add((Building_Num_URI, hasArea , 
            Literal(list(building_gdf[building_gdf["osmscID"] == Building_Num].Building_area)[0], 
                    datatype = XSD["decimal"]))) 

    graph.add((Building_Num_URI, hasPerimeter , 
            Literal(list(building_gdf[building_gdf["osmscID"] == Building_Num].Building_perimeter)[0], 
                    datatype = XSD["decimal"]))) 

    graph.add((Building_Num_URI, hasBuildingType , 
            Literal("Office", 
                    datatype = XSD["string"]))) 

    graph.add((Building_Num_URI, hasHeight , 
            Literal(list(building_gdf[building_gdf["osmscID"] == Building_Num].Building_height)[0], 
                    datatype = XSD["decimal"]))) 

    # geometry
    geom_str = str(list(building_gdf[building_gdf["osmscID"] == Building_Num].geometry)[0])
    graph.add((Building_Num_URI, hasGeometry, Literal(geom_str, datatype = XSD["string"]))) 

# Vegetation 
def add_Vegetation_Individual( graph, Vegetation_Num,VG_gdf ):
        
    Vegetation_Num_URI = URIRef(names[Vegetation_Num])

    graph.add((Vegetation_Num_URI, RDF.type, OWL.NamedIndividual))
    graph.add((Vegetation_Num_URI, RDF.type, Vegetation)) 

    graph.add((Vegetation_Num_URI, hasArea , 
            Literal(list(VG_gdf[VG_gdf["osmscID"] == Vegetation_Num].Vegetation_area)[0], 
                    datatype = XSD["decimal"]))) 

    graph.add((Vegetation_Num_URI, hasPerimeter , 
            Literal(list(VG_gdf[VG_gdf["osmscID"] == Vegetation_Num].Vegetation_perimeter)[0], 
                    datatype = XSD["decimal"]))) 


    # geometry
    geom_str = str(list(VG_gdf[VG_gdf["osmscID"] == Vegetation_Num].geometry)[0])
    graph.add((Vegetation_Num_URI, hasGeometry, Literal(geom_str, datatype = XSD["string"]))) 

# UrbanTile 
def add_UrbanTile_Individual(graph, UrbanTile_Num, urban_tile_gdf):
    
    UrbanTile_Num_URI = URIRef(names[UrbanTile_Num])
    #URIRef(names[UrbanTile_Num])

    graph.add((UrbanTile_Num_URI, RDF.type, OWL.NamedIndividual))
    graph.add((UrbanTile_Num_URI, RDF.type, UrbanTile)) 
    
    graph.add((UrbanTile_Num_URI, hasArea , 
            Literal(str(list(urban_tile_gdf[urban_tile_gdf["osmscID"] == UrbanTile_Num].UrbanTile_area)[0]), 
                    datatype = XSD["decimal"]))) 

    graph.add((UrbanTile_Num_URI, hasPerimeter , 
            Literal(str(list(urban_tile_gdf[urban_tile_gdf["osmscID"] == UrbanTile_Num].UrbanTile_perimeter)[0]), 
                    datatype = XSD["decimal"]))) 

    # geometry
    geom_str = str(list(urban_tile_gdf[urban_tile_gdf["osmscID"] == UrbanTile_Num].geometry)[0])
    graph.add((UrbanTile_Num_URI, hasGeometry, Literal(geom_str, datatype = XSD["string"]))) 


    # spatial semantics
    ############################################
    try:
        conBldg_list = ast.literal_eval(list(urban_tile_gdf[urban_tile_gdf["osmscID"] ==UrbanTile_Num]["contains_Building"])[0])
        for Bldg_i in conBldg_list:
            graph.add((UrbanTile_Num_URI, containsBuilding, URIRef(names[Bldg_i])))        
    except:
        #print("[nan]")
        pass

    ############################################ 

    try: 
        conVeg_list = ast.literal_eval(list(urban_tile_gdf[urban_tile_gdf["osmscID"] == UrbanTile_Num].contains_Vegetation)[0])
        for Veg_i in conVeg_list:
            graph.add((UrbanTile_Num_URI, containsVegetation, URIRef(names[Veg_i]))) 
    except:
        pass
            
    ############################################            

    try: 
        Stre_list = ast.literal_eval(list(urban_tile_gdf[urban_tile_gdf["osmscID"] == UrbanTile_Num].has_StreetNeighbor)[0])
        for Stre_i in Stre_list:
            graph.add((UrbanTile_Num_URI, hasStreetNeighbor , URIRef(names[Stre_i])))      
    except:
        pass

# UrbanPatch
def add_UrbanPatch_Individual(graph, UrbanPatch_Num, urban_patch_gdf_prj):
    
    UrbanPatch_Num_URI = URIRef(names[UrbanPatch_Num])
    graph.add((UrbanPatch_Num_URI, RDF.type, OWL.NamedIndividual))
    graph.add((UrbanPatch_Num_URI, RDF.type, UrbanPatch)) 

    # spatial semantics
    ############################################
    try:
        conTile_list = list(urban_patch_gdf_prj[urban_patch_gdf_prj["osmscID"] =="UrbanPatch_0"].containsTile)[0]
        for Tile_i in conTile_list:
            graph.add((UrbanPatch_Num_URI, containsTile, URIRef(names[Tile_i])))        
    except:
        pass

    ############################################ 

    try: 
        conStreet_list = list(urban_patch_gdf_prj[urban_patch_gdf_prj["osmscID"] == UrbanPatch_Num].containsStreet)[0]
        for Street_i in conStreet_list:
            graph.add((UrbanPatch_Num_URI, containsStreet, URIRef(names[Street_i]))) 
    except:
        pass

# UWG_paras
def UWG_paras_for_UrbanPatch(graph, UrbanPatch_Num_URI):

    all_Tile_area = 0
    all_Street_area = 0
    all_Building_area = 0
    all_Building_facade = 0
    height_multiply_area = 0
    all_veg_area = 0

    # 含有多少buildings veg street tile
    temp_1 = graph.objects(subject=UrbanPatch_Num_URI,predicate = containsTile )
    tile_URI_list = list(temp_1)

    # Tile
    for tile_URI in tile_URI_list:
        all_Tile_area = all_Tile_area + float(list(graph.objects(subject=tile_URI,predicate = hasArea))[0])

        # Building
        try: 
            temp_2 = graph.objects(subject=tile_URI,predicate = containsBuilding )
            bldg_URI_list = list(temp_2)
            for bldg_URI in bldg_URI_list:
                all_Building_area = all_Building_area + float(list(graph.objects(subject=bldg_URI,predicate = hasArea))[0])
                height_multiply_area = height_multiply_area + float(list(graph.objects(subject=bldg_URI,predicate = hasArea))[0]) * float(list(graph.objects(subject=bldg_URI,predicate = hasHeight))[0])
                all_Building_facade  = all_Building_facade +  float(list(graph.objects(subject=bldg_URI,predicate = hasPerimeter))[0]) * float(list(graph.objects(subject=bldg_URI,predicate = hasHeight))[0])
        except:
            pass
        
        # Veg
        try:         
            temp_3 = graph.objects(subject=tile_URI,predicate = containsVegetation )
            VG_URI_list = list(temp_3)
            for VG_URI in VG_URI_list:
                all_veg_area = all_veg_area + float(list(graph.objects(subject=VG_URI,predicate = hasArea))[0])
        except:
            pass
        
    # Street
    try:   
        temp_4 = graph.objects(subject=UrbanPatch_Num_URI,predicate = containsStreet )
        Street_URI_list = list(temp_4)       

        for Street_URI in Street_URI_list:
            all_Street_area = all_Street_area + float(list(graph.objects(subject=Street_URI,predicate = hasArea))[0])
    except:
        pass
    
    if all_Building_area == 0:
        AvgBuildingHeight = 0
    else:
        AvgBuildingHeight  = height_multiply_area / all_Building_area
        
    BuildingDensity =  all_Building_area/ (all_Tile_area+all_Street_area )
    VegetationDensity =  all_veg_area/ (all_Tile_area+all_Street_area )
    VerticalToHorizontalRatio = all_Building_facade/(all_Tile_area+all_Street_area )

    if BuildingDensity >1:
        BuildingDensity =1
    if VegetationDensity>1:
        VegetationDensity =1
        
    return AvgBuildingHeight, BuildingDensity, VegetationDensity, VerticalToHorizontalRatio


def construct_UPTO_individual(cityName, VG_gdf, building_gdf, street_gdf, urban_tile_gdf, urban_patch_gdf_prj):
    # Build graph
    graph = rdflib.Graph()
    graph.parse("init.ttl", format="turtle")

    ###################################################
    # Add UPTO individuals
    for j in range(len(VG_gdf)):
        Vegetation_Num = VG_gdf["osmscID"][j]
        add_Vegetation_Individual(graph,Vegetation_Num,VG_gdf )
        
    for z in range(len(building_gdf)):
        Building_Num = building_gdf["osmscID"][z]
        add_Building_Individual(graph,Building_Num, building_gdf)

    for q in range(len(street_gdf)):
        Street_Num = street_gdf["osmscID"][q]
        add_Street_Individual(graph, Street_Num, street_gdf)

    for k in range(len(urban_tile_gdf)):  
        UrbanTile_Num = urban_tile_gdf["osmscID"][k]
        add_UrbanTile_Individual(graph, UrbanTile_Num, urban_tile_gdf)
        
    for i in range(len(urban_patch_gdf_prj)):
        UrbanPatch_Num = urban_patch_gdf_prj["osmscID"][i]
        add_UrbanPatch_Individual(graph, UrbanPatch_Num, urban_patch_gdf_prj)
        

    # Add spatial semantics

    for k in range(len(urban_tile_gdf)):
        UrbanTile_Num = urban_tile_gdf["osmscID"][k]
        UrbanTile_Num_URI = URIRef(names[UrbanTile_Num])
        
        # withinTile for Building
        try:
            temp_1 = graph.objects(subject=UrbanTile_Num_URI,predicate = containsBuilding )
            bldg_URI_list = list(temp_1)
            for bldg_URI in bldg_URI_list:
                graph.add((bldg_URI, withinTile , UrbanTile_Num_URI)) 
        except:
            pass
            
        # withinTile for Vegetation
        try: 
            temp_2 = graph.objects(subject=UrbanTile_Num_URI,predicate = containsVegetation )
            VG_URI_list = list(temp_2)
            for VG_URI in VG_URI_list:
                graph.add((VG_URI, withinTile , UrbanTile_Num_URI))  
        except:
            pass
        
        # hasTileNeighbor for Street 
        try:
            temp_3 = graph.objects(subject=UrbanTile_Num_URI,predicate = hasStreetNeighbor )
            Street_URI_list = list(temp_3)
            for Street_URI in Street_URI_list:
                graph.add((Street_URI, hasTileNeighbor , UrbanTile_Num_URI))
        except:
            pass


    # hasTileNeighbor for UrbanTile
    condition = """
    SELECT ?UrbanTile_x ?UrbanTile_y
    WHERE { 
        ?UrbanTile_x :hasStreetNeighbor ?Street_z .
        ?UrbanTile_y :hasStreetNeighbor ?Street_z .
        FILTER (?UrbanTile_x != ?UrbanTile_y)
    }"""

    for row in graph.query(condition):
        graph.add((row.UrbanTile_x, hasTileNeighbor , row.UrbanTile_y)) 

    # withinPatch for UrbanTile Street 
    for i in range(len(urban_patch_gdf_prj)):
        
        UrbanPatch_Num = urban_patch_gdf_prj["osmscID"][i]
        UrbanPatch_Num_URI = URIRef(names[UrbanPatch_Num])
        
        # withinPatch for UrbanTile
        try:
            temp_1 = graph.objects(subject=UrbanPatch_Num_URI,predicate = containsTile )
            tile_URI_list = list(temp_1)
            for tile_URI in tile_URI_list:
                graph.add((tile_URI, withinPatch ,  UrbanPatch_Num_URI)) 
        except:
            pass
        
        # withinPatch for Street 
        try:
            temp_2 = graph.objects(subject=UrbanPatch_Num_URI,predicate = containsStreet )
            Street_URI_list = list(temp_2)
            for Street_URI in Street_URI_list:
                graph.add((Street_URI, withinPatch ,  UrbanPatch_Num_URI)) 
        except:
            pass

    # UWG_paras for UrbanPatch
    for i in range(len(urban_patch_gdf_prj)):
        
        UrbanPatch_Num = urban_patch_gdf_prj["osmscID"][i]
        UrbanPatch_Num_URI = URIRef(names[UrbanPatch_Num])
        
        AvgBuildingHeight, BuildingDensity, VegetationDensity, VerticalToHorizontalRatio = UWG_paras_for_UrbanPatch(graph, UrbanPatch_Num_URI)
        graph.add((UrbanPatch_Num_URI, hasAvgBuildingHeight ,  Literal(str(AvgBuildingHeight), datatype = XSD["decimal"]))) 
        graph.add((UrbanPatch_Num_URI, hasBuildingDensity ,  Literal(str(BuildingDensity), datatype = XSD["decimal"]))) 
        graph.add((UrbanPatch_Num_URI, hasVegetationDensity , Literal(str(VegetationDensity), datatype = XSD["decimal"]))) 
        graph.add((UrbanPatch_Num_URI, hasVerticalToHorizontalRatio ,  Literal(str( VerticalToHorizontalRatio), datatype = XSD["decimal"]))) 


    graph.serialize( cityName + ".ttl",format="turtle") 

