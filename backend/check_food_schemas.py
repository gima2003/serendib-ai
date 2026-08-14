import os
import csv

DATA_FOLDER = "data/food/raw"

for city_name in os.listdir(DATA_FOLDER):
    city_path = os.path.join(DATA_FOLDER, city_name)

    if not os.path.isdir(city_path):
        continue

    # Find the inner dataset folder
    inner_folders = [
        name for name in os.listdir(city_path)
        if os.path.isdir(os.path.join(city_path, name))
    ]

    if not inner_folders:
        print(f"\n⚠️ {city_name}: no dataset folder found")
        continue

    dataset_folder = inner_folders[0]
    dataset_path = os.path.join(city_path, dataset_folder)

    food_places_path = os.path.join(dataset_path, "food_places.csv")

    if os.path.exists(food_places_path):
        with open(food_places_path, "r", encoding="utf-8-sig") as file:
            reader = csv.reader(file)
            headers = next(reader)

        print("\nCITY:", city_name)
        print("DATASET FOLDER:", dataset_folder)
        print("COLUMNS:", headers)

    else:
        print(f"\n⚠️ {city_name}: food_places.csv NOT FOUND")