# Datasets Folder.

## Datasets
### Income Dataset
_ 2013 Tax Income Statistics_   
Dataset Filename: `income-data.csv`    
UID: ZIPCODE

| Attribute    | Type | Description |
| ---          | ---  | ---         |
| STATEFIPS    | Char | 01-56       |
| STATE        | Char | Two-digit State abbreviation code |
| ZIPCODE      | Char | |
| AGI_STUB     | Num  | See below |
| NUM_RETURNS  | Num  |  |
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
_ All the US Starbucks Locations _  
Dataset Filename: `starbucks.csv`    
UID: STORE_NUMBER

| Attribute    | Type | Description          |
| ---          | ---  | ---                  |
| STORE_NUMBER | Char | Two sets of numbers separated by '-'      |
| CITY         | Char | |
| STATE        | Char | Two-digit State abbreviation code  |
| ZIPCODE      | Char | |
| LONG         | Char | Longitude |
| LAT          | Char | Latitude |


> [Source](https://www.kaggle.com/starbucks/store-locations)
