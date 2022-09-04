# UrbanPatch Topology Ontology (UPTO)

This repo provides  four code samples to edit or use UPTO-based multi-city digitized building models dataset.

![ONTO](UPTO.png "ONTO")
<p align = "center"> UrbanPatch Topology Ontology</p>





  * `ConPatchForTile.py`: construct UrbanPatch individuals for UrbanTile objects when changing the receptive radius.
  * `ConPatchForBuilding.py`: construct UrbanPatch individuals for Building objects for a given receptive radius.
  * `GenMicroclimate.py`: generate the UrbanTile-scale microclimate.
  * `ConPatchForBuilding.py`: generate UrbanTile-scale EnergyPlus IDF file.
  
  
  
  


![workflow](Patch_demo.png "workflow")
<p align = "center">Physical objects to be considered in a target UrbanTile simulation</p>


## Main dependencies 
[RDFLib](https://pypi.org/project/rdflib/) 
[Geomeppy](https://pypi.org/project/geomeppy/) 
[UWG](https://pypi.org/project/uwg/) 
[OSMnx](https://pypi.org/project/osmnx/) 
[OSMsc](https://pypi.org/project/osmsc/) 







