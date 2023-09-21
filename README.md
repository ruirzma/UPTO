# UrbanPatch Topology Ontology (UPTO)

This repo provides  four code samples to edit or use UPTO-based multi-city digitized building models dataset.

![Ontology](UPTO.png "Ontology")
<p align = "center"> UrbanPatch Topology Ontology</p>


 ## Code samples
  
  * `ConPatchForTile.py`: construct UrbanPatch individuals for UrbanTile objects when changing the receptive radius.
  * `ConPatchForBuilding.py`: construct UrbanPatch individuals for Building objects for a given receptive radius.
  * `GenMicroclimate.py`: generate the UrbanTile-scale microclimate.
  * `GenIDF.py`: generate UrbanTile-scale EnergyPlus IDF file.


## Dataset
Ma, Rui; Li, Xin; Chen, jiayu (2022): A tiled multi-city urban objects dataset for city-scale building energy simulation. https://doi.org/10.6084/m9.figshare.20799637

### Citation
If you use UPTO in scientific work, I kindly ask you to cite it:

```bibtex
@article{Ma2023,
doi = {10.1038/s41597-023-02261-5},
issn = {2052-4463},
journal = {Scientific Data},
month = {jun},
number = {1},
pages = {352},
title = {{A tiled multi-city urban objects dataset for city-scale building energy simulation}},
url = {https://www.nature.com/articles/s41597-023-02261-5},
volume = {10},
year = {2023}
}
```

## Main dependencies 
[RDFLib](https://pypi.org/project/rdflib/) 
[Geomeppy](https://pypi.org/project/geomeppy/) 
[UWG](https://pypi.org/project/uwg/) 
[OSMnx](https://pypi.org/project/osmnx/) 
[OSMsc](https://pypi.org/project/osmsc/) 







