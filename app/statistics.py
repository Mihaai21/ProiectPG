import pandas as pd

# date mock inspirate din proiect
data = pd.DataFrame({
    "identifier_name": ["88823141", "88823142", "88823143", "88823144", "88823145", "88823146", None],
    "description": [
        "Shampoo Product",
        "Packaging Carton",
        "Packaging Box",
        "Chemical Substance",
        "Water",
        "Shampoo Bottle",
        None
    ],
    "identifier_type": [
        "Finished Product Part",
        "Packaging Material Part",
        "Packaging Material Part",
        "Assembled Product Part",
        "Assembled Product Part",
        "Material Part",
        None
    ],
    "country": ["Luxembourg", "France", "Germany", "Belgium", "Netherlands", "Sweden", "Norway"],
    "consumers": [150, 200, 100, 120, 80, 60, None]
})

# 1. missing values
data.fillna({
    "identifier_name": "Unknown",
    "description": "Unknown",
    "identifier_type": "Unknown",
    "consumers": data["consumers"].mean()
}, inplace=True)

print("DATASET COMPLET")
print(data)

# 2. Group by identifier_type si media numarului de consumatori
grouped_data = data.groupby("identifier_type")[["consumers"]].mean()

print("\nMEDIA CONSUMATORILOR PE TIP")
print(grouped_data)

# 3. Pivot table pe tari si tipuri
pivot_table = data.pivot_table(
    values="consumers",
    index="country",
    columns="identifier_type",
    aggfunc="sum",
    fill_value=0
)

print("\n PIVOT TABLE")
print(pivot_table)

# 4. Filtrare: doar produsele cu peste 100 consumatori
filtered_data = data[data["consumers"] > 100]

print("\nPRODUSE CU PESTE 100 CONSUMATORI")
print(filtered_data)

# 5. Numar pe fiecare tip
count_by_type = data["identifier_type"].value_counts()

print("\nNUMAR DE IDENTIFIERS PE TIP")
print(count_by_type)