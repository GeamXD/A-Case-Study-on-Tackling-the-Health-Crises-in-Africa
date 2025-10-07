import pandas as pd
import numpy as np


# Load the dataset
df1 = pd.read_csv('dataset/1. annual-number-of-deaths-by-cause.csv')
df2 = pd.read_csv('dataset/2. number-of-deaths-by-age-group.csv')
df3 = pd.read_excel('dataset/3. Medical Doctors Per 10000 population.xlsx', header=2)
df4 = pd.read_csv('dataset/4. ISO 3166_country-and-continent-codes-list-csv.csv')
df5 = pd.read_csv('dataset/5. World Population.csv')
df6 = pd.read_excel('dataset/6. Current health expenditure (% of GDP).xlsx', header=4)


# African countries
african_countries = [
    "Algeria", "Angola", "Benin", "Botswana", "Burkina Faso", "Burundi",
    "Cabo Verde", "Cameroon", "Central African Republic", "Chad", "Comoros",
    "Congo", "Democratic Republic of Congo", "Djibouti", "Egypt", "Equatorial Guinea",
    "Eritrea", "Eswatini", "Ethiopia", "Gabon", "Gambia", "Ghana", "Guinea",
    "Guinea-Bissau", "Cote d'Ivoire", "Kenya", "Lesotho", "Liberia", "Libya",
    "Madagascar", "Malawi", "Mali", "Mauritania", "Mauritius", "Morocco",
    "Mozambique", "Namibia", "Niger", "Nigeria", "Rwanda", "Sao Tome and Principe",
    "Senegal", "Seychelles", "Sierra Leone", "Somalia", "South Africa",
    "South Sudan", "Sudan", "Tanzania", "Togo", "Tunisia", "Uganda",
    "Zambia", "Zimbabwe", "Western Sahara"
]


# african who regions
african_regiions = [
    # 🌍 Regional groupings
    "African Region (WHO)",
    "Sub-Saharan Africa",
    "Sub-Saharan Africa (WB)",
    "Middle East & North Africa",
    "Middle East & North Africa (WB)",
]
