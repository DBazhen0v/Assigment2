import pandas as pd
import requests
import matplotlib.pyplot as plt
response = requests.get("https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/all_month.geojson")
data = response.json()


data = data ["features"]
e = []
for i in data:
    prop = i["properties"]
    geometry = i["geometry"]

    e.append({
        "place": prop["place"],
        "Magnitude": prop["mag"],
        "Time": prop["time"],
        "Depth": geometry["coordinates"][2]
    })
df = pd.DataFrame(e)
print(df)
filtered_df = df[df['Magnitude'] > 3.0]
df['Time'] = pd.to_datetime(df["Time"], unit='ms')
df = df.dropna(subset=["Depth"])
top_5 = df.nlargest(5, 'Magnitude')
MAX = filtered_df["Magnitude"].max()
MIN = filtered_df["Magnitude"].min()
avg = filtered_df["Magnitude"].mean()
correlation = df['Magnitude'].corr(df['Depth'])
region_counts = df["place"].value_counts()


plt.figure(figsize=(10, 6))
plt.hist(df['Magnitude'].dropna(), bins=20, color='skyblue', edgecolor='black')


plt.title("Гістограма розподілу магнітуд землетрусів за останній місяць", fontsize=14)
plt.xlabel("Магнітуда", fontsize=12)
plt.ylabel("Кількість землетрусів", fontsize=12)
plt.grid(axis='y', alpha=0.75)

plt.show()

print(f"Максимальна магнітуда:{MAX}")
print(f"Мінімальна магнітуда:{MIN}")
print(f"Середня магнітуда:{avg}")
print(f"top 5 magnitute:")
print(top_5[["place", "Magnitude", "Time"]])
print(f"Коеф. кореляції:{correlation}")
print(f"біля якого регіону чи країни сталося найбільше землетрусів :{region_counts.idxmax()}")