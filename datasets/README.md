# Datasets Folder.

## Purpose
This folder is here to act as a designated placeholder for all the datasets this project uses.
The reasoning for this is that the datasets are too large to have in the repo, and besides, the datasets won't be changing anyways.
So, in order to maintain consistency across all developers and users, all datasets should be listed below with a download link and the name of the file that the program is expecting it to be called.
No files in this folder will be tracked


## Datasets
### Income Dataset
Dataset Filename: `income-data.csv`  

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



| Dataset Name | Dataset Filename | Download Link |
| --- | --- | --- |
| Zip Code Data | income-data.csv | [Site](https://www.irs.gov/uac/soi-tax-stats-individual-income-tax-statistics-zip-code-data-soi)
| Starbucks Locations | starbucks.csv | [Site](https://www.kaggle.com/starbucks/store-locations)
