import pandas as pd
import numpy as np


# Load the dataset
deaths_by_cause_df = pd.read_csv('dataset/1. annual-number-of-deaths-by-cause.csv')
number_of_deaths_by_age_group = pd.read_csv('dataset/2. number-of-deaths-by-age-group.csv')
medical_doctors_per_10000_population = pd.read_excel('dataset/3. Medical Doctors Per 10000 population.xlsx', header=2)
iso_country_codes = pd.read_csv('dataset/4. ISO 3166_country-and-continent-codes-list-csv.csv')
world_population_data = pd.read_csv('dataset/5. World Population.csv')
current_health_expenditure = pd.read_excel('dataset/6. Current health expenditure (% of GDP).xlsx', header=4)

# Health care related causes of death
healthcare_causes = [
    "Entity",
    "Code",
    "Year",
    "Meningitis",
    "Alzheimer's disease and other dementias",
    "Parkinson's disease",
    "Nutritional deficiencies",
    "Malaria",
    "Drowning",
    "Interpersonal violence",
    "Maternal disorders",
    "HIV/AIDS",
    "Drug use disorders",
    "Tuberculosis",
    "Cardiovascular diseases",
    "Lower respiratory infections",
    "Neonatal disorders",
    "Alcohol use disorders",
    "Self",
    "Diarrheal diseases",
    "Neoplasms",
    "Diabetes mellitus",
    "Chronic kidney disease",
    "Poisonings",
    "Road injuries",
    "Chronic respiratory diseases",
    "Cirrhosis and other chronic liver diseases",
    "Digestive diseases",
    "Fire, heat, and hot substances",
    "Acute hepatitis"
]

# Subset healthcare causes of death
deaths_by_cause_df = deaths_by_cause_df[healthcare_causes]

# Remove not sovereign countries
not_sovereign_countries = [
    "Mayotte",
    "Reunion",
    "Saint Helena",
    "Western Sahara"
]
iso_country_codes = iso_country_codes[~iso_country_codes['Country_Name'].isin(not_sovereign_countries)]
african_countries_mask = iso_country_codes['Continent_Name'] == 'Africa'
iso_country_codes = iso_country_codes[african_countries_mask]
three_letter_codes = iso_country_codes['Three_Letter_Country_Code'].tolist()
three_letter_codes.append('SYC')

# Subset African countries
african_country_mask = deaths_by_cause_df['Code'].str.lower().isin([x.lower() for x in three_letter_codes])
deaths_by_cause_df = deaths_by_cause_df[african_country_mask]

# Rename columns
medical_doctors_per_10000_population.rename(columns={
    'ThreeLocCode':'Code',
    'Period': 'Year',
    'FactValueNumeric': 'Number of medical doctors'
}, inplace=True)

# Drop column in medical_doctors_per_10000_population
medical_doctors_per_10000_population.drop(columns=[
                                                   'Value', 'IndicatorCode',
                                                   'ParentLocationCode',
                                                   'Location', 'ParentLocation'], inplace=True)

# Rename columns
current_health_expenditure.rename(columns={
    'Country Name':'Entity',
    'Country Code':'Code',
}, inplace=True)

# Drop column in current_health_expenditure
current_health_expenditure.drop(columns=['Indicator Name'], inplace=True)

# Flatten expenditure
current_health_expenditure = current_health_expenditure.melt(
    id_vars=["Entity", "Code"],   # columns to keep fixed
    var_name="Year",              # name for the year column
    value_name="Health_Expenditure"  # name for the value column
)


# Flatten Death by Cause
deaths_by_cause_df = deaths_by_cause_df.melt(
    id_vars=["Entity", "Code", "Year"],     # columns to keep
    var_name="Cause",                       # new column for cause names
    value_name="Deaths"                     # new column for number of deaths
)


# Flatten Age group
number_of_deaths_by_age_group = number_of_deaths_by_age_group.melt(
    id_vars=["Entity", "Code", "Year"],     # columns to keep
    var_name="Age Group",                       # new column for cause names
    value_name="Deaths per age group"                     # new column for number of deaths
)


# Drop Entity columns
number_of_deaths_by_age_group.drop(columns=['Entity'], inplace=True)
current_health_expenditure.drop(columns=['Entity'], inplace=True)
world_population_data.drop(columns=['Entity'], inplace=True)

# Merge dataset
core_health = deaths_by_cause_df.merge(number_of_deaths_by_age_group, on=["Code", "Year"], how="outer")
core_health = core_health.merge(medical_doctors_per_10000_population, on=['Code', "Year"], how="left")
core_health = core_health.merge(current_health_expenditure, on=["Code", "Year"], how="left")
core_health = core_health.merge(world_population_data, on=["Code", "Year"], how="left")


# Drop na in Entity
core_health.dropna(subset=['Entity'], inplace=True)


# Filter for years above 2000
core_health = core_health[core_health['Year'] >= 2000]

# Imputation
core_health['Deaths per age group'] = core_health['Deaths per age group'].fillna(core_health['Deaths per age group'].median())
core_health['Deaths'] = core_health['Deaths'].fillna(core_health['Deaths'].median())


# Impute for Health_Expenditure
core_health['Health_Expenditure'] = (
    core_health.groupby('Entity')['Health_Expenditure']
              .transform(lambda x: x.fillna(x.median()))
)
core_health['Health_Expenditure'] = core_health['Health_Expenditure'].fillna(core_health['Health_Expenditure'].median())

core_health.to_csv('dataset/core_health.csv', index=False)

# Doctors dataset
core_health_doctors = core_health[core_health['Number of medical doctors'].notna()].copy()
core_health_doctors.to_csv('dataset/core_health_doctors.csv', index=False)

# Non doctors dataset
core_health_non_doctors = core_health[core_health['Number of medical doctors'].isna()].copy()
core_health_non_doctors.drop(columns=['Number of medical doctors', 'Indicator'], inplace=True)
core_health_non_doctors.to_csv('dataset/core_health_non_doctors.csv', index=False)