from cost_loader import load_costs


print("==============================")
print("COST LOADER TEST")
print("==============================")


costs = load_costs()


print("\nTotal attractions with costs:")
print(len(costs))


print("\nSample attraction cost:")
print("------------------------------")


# Colombo National Museum
attraction_id = "COL-A001"


if attraction_id in costs:

    for cost in costs[attraction_id]:

        print(cost)

else:

    print(
        "No costs found for",
        attraction_id
    )