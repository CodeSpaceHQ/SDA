# Datasets Folder.

## Datasets
### Income Dataset
_2013 Tax Income Statistics_   
Dataset Filename: `income-data.csv`    
UID: STATE + ZIPCODE + AGI_STUB

| Attribute    | Type          | Description |
| ---          | ---           | --- |
| STATEFIPS    | CHAR(2)       | 01-56 |
| STATE        | CHAR(2)       | Two-digit State abbreviation code |
| ZIPCODE      | CHAR(5)       | |
| AGI_STUB     | TINYINT       | See below |
| NUM_RETURNS  | FLOAT(15, 4)  | |
| TOTAL_INCOME | FLOAT(15, 4)  | 1040:22 / 1040A:15 / 1040EZ:4 |

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

| Attribute    | Type        | Description |
| ---          | ---         | --- |
| STORE_NUMBER | VARCHAR(20) | Two sets of numbers separated by '-' |
| CITY         | VARCHAR(50) | |
| STATE        | CHAR(2)     | Two-digit State abbreviation code |
| ZIPCODE      | CHAR(5)     | |
| LONG         | VARCHAR(10) | Longitude |
| LAT          | VARCHAR(10) | Latitude |


> [Source](https://www.kaggle.com/starbucks/store-locations)

### Diversity Dataset
_County Diversity Information_  
Dataset Filename: `diversity.csv`    
UID: COUNTY + STATE

| Attribute    | Type | Description |
| ---          | ---  | --- |
| COUNTY | VARCHAR(50) | |
| STATE  | CHAR(2) | |
| INDEX  | FLOAT(7,6) | Two-digit State abbreviation code |
| 1      | FLOAT(3,1) | Black or African American alone |
| 2      | FLOAT(3,1) | American Indian and Alaska Native alone |
| 3      | FLOAT(3,1) | Asian alone |
| 4      | FLOAT(3,1) | Native Hawaiian and Other Pacific Islander alone |
| 5      | FLOAT(3,1) | Two or More Races |
| 6      | FLOAT(3,1) | Hispanic or Latino |
| 7      | FLOAT(3,1) | White alone, not Hispanic or Latino |



> [Source](https://github.com/kdallas2/diversity/blob/master/di.csv)

### Location Dataset
_Zipcodes, Cities, States & Counties_  
Dataset Filename: `locations.csv`    

| Attribute | Type | Description |
| ---       | ---  | --- |
| ZIPCODE   | CHAR(5)  | |
| CITY      | VARCHAR(50) | |
| STATE     | CHAR(2) | Two-digit State abbreviation code  |
| COUNTY    | VARCHAR(50) | |


> [Source](https://www.gaslampmedia.com/download-zip-code-latitude-longitude-city-state-county-csv/)
