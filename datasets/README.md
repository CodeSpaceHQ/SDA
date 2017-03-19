# Datasets Folder.

## Datasets
### Income Dataset
_2013 Tax Income Statistics_   
Dataset Filename: `income-data.csv`    
UID: ZIPCODE + AGI_STUB

| Attribute    | Type | Description |
| ---          | ---  | ---         |
| STATEFIPS    | Char | 01-56       |
| STATE        | Char | Two-digit State abbreviation code |
| ZIPCODE      | Char | |
| AGI_STUB     | Num  | See below |
| NUM_RETURNS  | Num  | |
| TOTAL_INCOME | Num  | 1040:22 / 1040A:15 / 1040EZ:4 |

AGI_STUB:
- 1 = $1 under $25,000
- 2 = $25,000 under $50,000
- 3 = $50,000 under $75,000
- 4 = $75,000 under $100,000
- 5 = $100,000 under $200,000
- 6 = $200,000 or more


> [Source](https://www.irs.gov/uac/soi-tax-stats-individual-income-tax-statistics-zip-code-data-soi)

### Starbucks Locations Dataset
_All the US Starbucks Locations_  
Dataset Filename: `starbucks.csv`    
UID: STORE_NUMBER

| Attribute    | Type | Description |
| ---          | ---  | --- |
| STORE_NUMBER | Char | Two sets of numbers separated by '-' |
| CITY         | Char | |
| STATE        | Char | Two-digit State abbreviation code |
| ZIPCODE      | Char | |
| LONG         | Char | Longitude |
| LAT          | Char | Latitude |


> [Source](https://www.kaggle.com/starbucks/store-locations)

### Diversity Dataset
_County Diversity Information_  
Dataset Filename: `diversity.csv`    
UID: COUNTY + STATE

| Attribute    | Type | Description |
| ---          | ---  | --- |
| COUNTY | Char | |
| STATE  | Char | |
| INDEX  | Char | Two-digit State abbreviation code |
| 1      | Num | Black or African American alone |
| 2      | Num | American Indian and Alaska Native alone |
| 3      | Num | Asian alone |
| 4      | Num | Native Hawaiian and Other Pacific Islander alone |
| 5      | Num | Two or More Races |
| 6      | Num | Hispanic or Latino |
| 7      | Num | White alone, not Hispanic or Latino |



> [Source](https://github.com/kdallas2/diversity/blob/master/di.csv)

### Location Dataset
_Zipcodes, Cities, States & Counties_  
Dataset Filename: `locations.csv`    

| Attribute | Type | Description |
| ---       | ---  | --- |
| ZIPCODE   | Char  | |
| CITY      | Char | |
| STATE     | Char | Two-digit State abbreviation code  |
| COUNTY    | Char | |


> [Source](https://www.gaslampmedia.com/download-zip-code-latitude-longitude-city-state-county-csv/)
