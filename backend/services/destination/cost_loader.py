import pandas as pd
from pathlib import Path


COST_FILE = Path(
    "data/destination/combined/attraction_costs.csv"
)


def load_costs():

    df = pd.read_csv(
        COST_FILE,
        keep_default_na=False
    )

    costs = {}


    for _, row in df.iterrows():

        attraction_id = row["attraction_id"]


        if attraction_id not in costs:
            costs[attraction_id] = []


        costs[attraction_id].append(
            {
                "visitor_category":
                    row["visitor_category"],

                "age_category":
                    row["age_category"],

                "amount":
                    row["amount"],

                "currency":
                    row["currency"],

                "verification_status":
                    row["verification_status"]
            }
        )


    return costs