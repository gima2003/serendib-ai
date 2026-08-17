import os

from dotenv import load_dotenv
from pymongo import MongoClient, ASCENDING, DESCENDING


# ==========================================================
# 1. LOAD ENVIRONMENT VARIABLES
# ==========================================================

load_dotenv()

MONGODB_URL = os.getenv("MONGODB_URL")
DATABASE_NAME = os.getenv("DATABASE_NAME")


if not MONGODB_URL:
    raise ValueError("MONGODB_URL was not found in .env")

if not DATABASE_NAME:
    raise ValueError("DATABASE_NAME was not found in .env")


print("\n========== CREATING FOOD AGENT INDEXES ==========\n")


# ==========================================================
# 2. CONNECT TO MONGODB
# ==========================================================

client = MongoClient(
    MONGODB_URL,
    serverSelectionTimeoutMS=10000
)

client.admin.command("ping")

print("✅ MongoDB connection successful")

db = client[DATABASE_NAME]


# ==========================================================
# 3. FOOD PLACES INDEXES
# ==========================================================

food_places = db["food_places"]

food_places.create_index(
    [("place_id", ASCENDING)],
    unique=True,
    name="idx_food_places_place_id"
)

food_places.create_index(
    [("city", ASCENDING)],
    name="idx_food_places_city"
)

food_places.create_index(
    [
        ("city", ASCENDING),
        ("rating", DESCENDING)
    ],
    name="idx_food_places_city_rating"
)

food_places.create_index(
    [
        ("city", ASCENDING),
        ("price_band_lkr", ASCENDING)
    ],
    name="idx_food_places_city_price"
)

print("✅ food_places indexes created")


# ==========================================================
# 4. FOOD ITEMS INDEXES
# ==========================================================

food_items = db["food_items"]

food_items.create_index(
    [("food_id", ASCENDING)],
    unique=True,
    name="idx_food_items_food_id"
)

food_items.create_index(
    [("city", ASCENDING)],
    name="idx_food_items_city"
)

food_items.create_index(
    [("food_name", ASCENDING)],
    name="idx_food_items_name"
)

food_items.create_index(
    [
        ("city", ASCENDING),
        ("category", ASCENDING)
    ],
    name="idx_food_items_city_category"
)

print("✅ food_items indexes created")


# ==========================================================
# 5. FOOD PLACE-DISH RELATIONSHIP INDEXES
# ==========================================================

food_place_dishes = db["food_place_dishes"]

food_place_dishes.create_index(
    [("link_id", ASCENDING)],
    unique=True,
    name="idx_food_place_dishes_link_id"
)

food_place_dishes.create_index(
    [("place_id", ASCENDING)],
    name="idx_food_place_dishes_place_id"
)

food_place_dishes.create_index(
    [("food_id", ASCENDING)],
    name="idx_food_place_dishes_food_id"
)

food_place_dishes.create_index(
    [
        ("place_id", ASCENDING),
        ("food_id", ASCENDING)
    ],
    name="idx_food_place_dishes_place_food"
)

print("✅ food_place_dishes indexes created")


# ==========================================================
# 6. SOCIAL RECOMMENDATION INDEXES
# ==========================================================

social = db["social_recommendations"]

social.create_index(
    [("signal_id", ASCENDING)],
    unique=True,
    name="idx_social_signal_id"
)

social.create_index(
    [("place_id", ASCENDING)],
    name="idx_social_place_id"
)

social.create_index(
    [("signal_polarity", ASCENDING)],
    name="idx_social_polarity"
)

print("✅ social_recommendations indexes created")


# ==========================================================
# 7. CITY FOOD PROFILE INDEXES
# ==========================================================

city_profiles = db["city_food_profiles"]

city_profiles.create_index(
    [("city_id", ASCENDING)],
    unique=True,
    name="idx_city_profile_city_id"
)

city_profiles.create_index(
    [("city", ASCENDING)],
    unique=True,
    name="idx_city_profile_city"
)

print("✅ city_food_profiles indexes created")


# ==========================================================
# 8. RECOMMENDATION TAG INDEXES
# ==========================================================

recommendation_tags = db["recommendation_tags"]

recommendation_tags.create_index(
    [("tag_id", ASCENDING)],
    unique=True,
    name="idx_recommendation_tag_id"
)

recommendation_tags.create_index(
    [("tag", ASCENDING)],
    unique=True,
    name="idx_recommendation_tag"
)

print("✅ recommendation_tags indexes created")


# ==========================================================
# 9. SOURCE REGISTRY INDEXES
# ==========================================================

sources = db["source_registry"]

sources.create_index(
    [("source_id", ASCENDING)],
    unique=True,
    name="idx_source_registry_source_id"
)

sources.create_index(
    [("source_url", ASCENDING)],
    unique=True,
    sparse=True,
    name="idx_source_registry_url"
)

print("✅ source_registry indexes created")


# ==========================================================
# 10. SHOW CREATED INDEXES
# ==========================================================

collections = [
    "food_places",
    "food_items",
    "food_place_dishes",
    "social_recommendations",
    "city_food_profiles",
    "recommendation_tags",
    "source_registry",
]

print("\n========== INDEX SUMMARY ==========\n")

for collection_name in collections:

    collection = db[collection_name]

    print(f"\n📦 {collection_name}")

    indexes = collection.index_information()

    for index_name in indexes:
        print(f"   ✅ {index_name}")


client.close()

print("\n============================================")
print("✅ Food Agent MongoDB indexing completed.")
print("============================================")