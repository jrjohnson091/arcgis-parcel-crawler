curl "https://gisccapps.charlestoncounty.org/arcgis/rest/services/GIS_VIEWER/New_Parcel_Search/MapServer?f=pjson" \
| jq '.layers[] | {id,name}'

# {
#   "id": 0,
#   "name": "Base Data"
# }
# {
#   "id": 1,
#   "name": "Address Points"
# }
# {
#   "id": 2,
#   "name": "Streets (Major Only)"
# }
# {
#   "id": 3,
#   "name": "Streets"
# }
# {
#   "id": 61,
#   "name": "PARCELS"
# }
# {
#   "id": 5,
#   "name": "Misc Parcel Features"
# }
# {
#   "id": 6,
#   "name": "Building Footprints"
# }
# {
#   "id": 7,
#   "name": "1992 Building Footprints"
# }
# {
#   "id": 8,
#   "name": "2001 Building Footprints"
# }
# {
#   "id": 9,
#   "name": "2012 Building Footprints"
# }
# {
#   "id": 10,
#   "name": "2017 Building Footprints"
# }
# {
#   "id": 11,
#   "name": "2019 Building Footprints"
# }
# {
#   "id": 21,
#   "name": "2025 Building Footprints"
# }
# {
#   "id": 12,
#   "name": "SC Beachfront Jurisdictional Lines"
# }
# {
#   "id": 13,
#   "name": "2016-2018 Baseline"
# }
# {
#   "id": 14,
#   "name": "2016-2018 Setback Line"
# }
# {
#   "id": 15,
#   "name": "Hydrology"
# }
# {
#   "id": 16,
#   "name": "Marsh"
# }
# {
#   "id": 17,
#   "name": "Water Bodies"
# }
# {
#   "id": 18,
#   "name": "Boundaries"
# }
# {
#   "id": 19,
#   "name": "Chas County Urban Growth Boundary"
# }
# {
#   "id": 20,
#   "name": "Municipal Boundaries"
# }
# {
#   "id": 28,
#   "name": "County Boundary"
# }
# {
#   "id": 22,
#   "name": "County Council Districts"
# }
# {
#   "id": 23,
#   "name": "County Tax Districts"
# }
# {
#   "id": 24,
#   "name": "Planning & Zoning"
# }
# {
#   "id": 25,
#   "name": "Charleston County Historic Properties"
# }
# {
#   "id": 26,
#   "name": "Charleston County Historic Properties Buffer"
# }
# {
#   "id": 27,
#   "name": "Zoning Districts"
# }
# {
#   "id": 60,
#   "name": "Chas County Future Land Use"
# }
# {
#   "id": 29,
#   "name": "Chas County Overlay Zoning Districts"
# }
# {
#   "id": 30,
#   "name": "Public Works"
# }
# {
#   "id": 31,
#   "name": "Drainage Easements"
# }
# {
#   "id": 32,
#   "name": "Environmental Management"
# }
# {
#   "id": 33,
#   "name": "Convenient Centers and Dropsites"
# }
# {
#   "id": 34,
#   "name": "RECYCLING ROUTES"
# }
# {
#   "id": 35,
#   "name": "City of Charleston Data"
# }
# {
#   "id": 36,
#   "name": "City of Charleston Addresses"
# }
# {
#   "id": 37,
#   "name": "City of Charleston Zoning"
# }
# {
#   "id": 38,
#   "name": "City of North Charleston Data"
# }
# {
#   "id": 39,
#   "name": "North Charleston Addresses"
# }
# {
#   "id": 40,
#   "name": "North Charleston Zoning"
# }
# {
#   "id": 41,
#   "name": "North Charleston Future Land Use"
# }
# {
#   "id": 42,
#   "name": "Mt Pleasant Data"
# }
# {
#   "id": 43,
#   "name": "Mt Pleasant Addresses"
# }
# {
#   "id": 44,
#   "name": "Mt Pleasant Urban Growth Boundary"
# }
# {
#   "id": 45,
#   "name": "Mt Pleasant Future Land Use"
# }
# {
#   "id": 46,
#   "name": "Mt Pleasant Zoning"
# }
# {
#   "id": 47,
#   "name": "Town of Summerville"
# }
# {
#   "id": 48,
#   "name": "Summerville Addresses"
# }
# {
#   "id": 49,
#   "name": "Town of Awendaw"
# }
# {
#   "id": 50,
#   "name": "Awendaw Zoning"
# }
# {
#   "id": 51,
#   "name": "Flood and Earthquake Data"
# }
# {
#   "id": 52,
#   "name": "Seismic Lines"
# }
# {
#   "id": 53,
#   "name": "Current FEMA Dfirms"
# }
# {
#   "id": 54,
#   "name": "LOMR BOUNDARIES"
# }
# {
#   "id": 55,
#   "name": "LOMR PARCELS"
# }
# {
#   "id": 56,
#   "name": "LiMWA"
# }
# {
#   "id": 57,
#   "name": "Current FEMA Flood Data"
# }
# {
#   "id": 58,
#   "name": "2004 FEMA Dfirms"
# }
# {
#   "id": 59,
#   "name": "2004 FEMA Flood Data"
# }
