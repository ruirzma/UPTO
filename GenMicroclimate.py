from uwg import UWG
import rdflib 
from rdflib import RDF, Namespace, URIRef, Literal, OWL ,XSD

# Load TTL dataset
graph = rdflib.Graph()
graph.parse("sample_data.ttl", format="turtle")
names = Namespace("http://www.urbanpatchtopologyontology.org/upto#")


# URIRef
withinPatch = URIRef(names["withinPatch"])
UrbanPatch = URIRef(names["UrbanPatch"])
hasAvgBuildingHeight  = URIRef(names["hasAvgBuildingHeight"])
hasBuildingDensity = URIRef(names["hasBuildingDensity"])
hasVegetationDensity =  URIRef(names["hasVegetationDensity"])
hasVerticalToHorizontalRatio = URIRef(names["hasVerticalToHorizontalRatio"])


# Target UrbanTile
UrbanTile_Num_URI = URIRef(names["UrbanTile_0"])
UrbanPatch_Num_URI = list(graph.objects(subject=UrbanTile_Num_URI, predicate= withinPatch))[0]


# Extract the features
AvgBuildingHeight = float(list(graph.objects(subject= UrbanPatch_Num_URI, predicate= hasAvgBuildingHeight))[0])
BuildingDensity = float(list(graph.objects(subject= UrbanPatch_Num_URI, predicate= hasBuildingDensity))[0])
VegetationDensity = float(list(graph.objects(subject= UrbanPatch_Num_URI, predicate= hasVegetationDensity))[0])
VerticalToHorizontalRatio =float(list(graph.objects(subject= UrbanPatch_Num_URI, predicate= hasVerticalToHorizontalRatio))[0])


# Define the .epw, .uwg paths to create an uwg object.
# Could Download from EnergyPlus Website.
epw_path = 'XXX_TMY3.epw' 

# Initialize the UWG model by passing parameters as arguments, or relying on defaults
model = UWG.from_param_args(epw_path=epw_path, bldheight=AvgBuildingHeight, blddensity=BuildingDensity ,
                            vertohor=VegetationDensity, treecover=VerticalToHorizontalRatio, zone='8',nday=365)

model.generate()
model.simulate()

# Write the simulation result to a file.
model.write_epw()


