from pathlib import Path
import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent.parent

DATA_DIR = (
    BASE_DIR
    / "data"
    / "destination"
    / "combined"
)

ATTRACTIONS_FILE = DATA_DIR / "attractions.csv"
EXPERIENCES_FILE = DATA_DIR / "experiences.csv"
RELATIONSHIPS_FILE = (
    DATA_DIR / "attraction_experiences.csv"
)


def load_data():

    attractions = pd.read_csv(
        ATTRACTIONS_FILE
    )

    experiences = pd.read_csv(
        EXPERIENCES_FILE
    )

    relationships = pd.read_csv(
        RELATIONSHIPS_FILE
    )

    return (
        attractions,
        experiences,
        relationships
    )