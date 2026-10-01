from .profile_adapter import (
    extract_destination_preferences
)

from .data_loader import load_data

from .interest_matcher import (
    match_interests_to_experiences
)

from .attraction_ranker import (
    score_attractions
)

from .destination_ranker import (
    rank_destinations
)

from .text_utils import normalize_text

from .cost_loader import load_costs

from .destination_validator import validate_destination
from services.destination.attraction_ranker import score_attractions

# =====================================================
# Interest Based Destination Recommendation
# =====================================================

def recommend_destinations(
    interests,
    top_destinations=5,
    top_attractions=5,
    debug=False
):

    (
        attractions,
        experiences,
        relationships
    ) = load_data()


    cost_lookup = load_costs()



    matched_experiences = (
        match_interests_to_experiences(
            interests,
            experiences
        )
    )

    matched_interest_names = {
        normalize_text(item["interest"])
        for item in matched_experiences
    }


    unmatched_interests = [
        interest
        for interest in interests
        if normalize_text(interest)
        not in matched_interest_names
    ]



    if not matched_experiences:

        return {

            "input_interests": interests or [],

            "matched_experiences": [],

            "unmatched_interests": unmatched_interests,

            "recommended_destinations": []

        }



    matched_interest_names = {

        normalize_text(
            item["interest"]
        )

        for item in matched_experiences

    }



    unmatched_interests = [

        interest

        for interest in interests

        if normalize_text(interest)
        not in matched_interest_names

    ]



    attraction_results = (

        score_attractions(
            matched_experiences,
            attractions,
            relationships
        )

    )



    requested_experience_ids = {

        item["experience_id"]

        for item in matched_experiences

    }



    destination_results = (

        rank_destinations(

            attraction_results,

            requested_experience_count=len(
                requested_experience_ids
            )

        )

    )



    recommendations = []



    for _, destination in (

        destination_results
        .head(top_destinations)
        .iterrows()

    ):


        city = destination["city"]



        city_attractions = (

            attraction_results[

                attraction_results["city"]
                == city

            ]

            .head(top_attractions)

        )



        attraction_list = []



        for _, attraction in city_attractions.iterrows():


            attraction_id = attraction[
                "attraction_id"
            ]



            item = {

                "attraction_id":
                    attraction_id,


                "name":
                    attraction[
                        "attraction_name"
                    ],


                "category":
                    attraction[
                        "category"
                    ],


                "indoor_outdoor":
                    attraction.get(
                        "indoor_outdoor"
                    ),


                "sub_category":
                    attraction[
                        "sub_category"
                    ],


                "match_score":
                    round(
                        float(
                            attraction[
                                "match_score"
                            ]
                        ),
                        3
                    ),


                "coverage_score":
                    round(
                        float(
                            attraction[
                                "coverage_score"
                            ]
                        ),
                        3
                    ),


                "entry_costs":
                    cost_lookup.get(
                        attraction_id,
                        []
                    )

            }



            if debug:

                item[
                    "debug_matches"
                ] = attraction[
                    "matched_experiences"
                ]



            attraction_list.append(item)



        recommendations.append(

            {

                "destination":
                    city,


                "score":
                    round(
                        float(
                            destination[
                                "final_score"
                            ]
                        ),
                        3
                    ),


                "recommendation_source":
                    "interest_matching",


                "interest_coverage":
                    round(
                        float(
                            destination[
                                "destination_coverage"
                            ]
                        ),
                        3
                    ),


                "matching_attractions":
                    int(
                        destination[
                            "matching_attractions"
                        ]
                    ),


                "strong_attractions":
                    int(
                        destination[
                            "strong_attractions"
                        ]
                    ),


                "attractions":
                    attraction_list

            }

        )



    return {

        "input_interests":
            interests,


        "matched_experiences":
            matched_experiences,


        "unmatched_interests":
            unmatched_interests,


        "recommended_destinations":
            recommendations

    }





# =====================================================
# Preferred Destination Recommendation
# =====================================================

def recommend_from_preferred_destinations(
    destinations,
    interests=None,
    top_attractions=5
):

    (
        attractions,
        experiences,
        relationships
    ) = load_data()


    cost_lookup = load_costs()


    recommendations = []


    # ==========================================
    # If user gives interests with destination
    # ==========================================

    attraction_scores = None
    matched_experiences = []
    unmatched_interests = []


    if interests:

        matched_experiences = (
            match_interests_to_experiences(
                interests,
                experiences
            )
        )

        attraction_scores = score_attractions(
            matched_experiences,
            attractions,
            relationships
        )

        


        if not matched_experiences:

            return {

                "input_interests": interests,

                "matched_experiences": [],

                "unmatched_interests": interests,

                "recommended_destinations": []

            }

            attraction_scores = (
                score_attractions(
                    matched_experiences,
                    attractions,
                    relationships
                )
            )



    for destination in destinations:

            validation = validate_destination(
                destination,
                attractions["city"].unique()
            )


            if validation["status"] != "valid":

                recommendations.append(
                    {
                        "destination": destination,

                        "score": 0,

                        "recommendation_source":
                            "destination_validation",

                        "validation_status":
                            validation["status"],

                        "message":
                            (
                                "Destination is not available "
                                "in the supported dataset."
                            ),

                        "suggestions":
                            validation["suggestions"],

                        "attractions": []
                    }
                )

                continue


            # Filter selected destination
            if attraction_scores is not None and not attraction_scores.empty:

                destination_attractions = attraction_scores[
                    attraction_scores["city"]
                    .str.lower()
                    ==
                    destination.lower()
                ]

            else:

                destination_attractions = attractions[
                    attractions["city"]
                    .str.lower()
                    ==
                    destination.lower()
                ]



        # ======================================
        # Rank by interests if available
        # ======================================

            if (
                attraction_scores is not None
                and not attraction_scores.empty
            ):


                destination_scores = attraction_scores[
                    attraction_scores["city"]
                    .str.lower()
                    ==
                    destination.lower()
                ]


                if not destination_scores.empty:

                    city_attractions = (
                        destination_scores
                        .sort_values(
                            by=[
                                "match_score",
                                "coverage_score",
                                "relevance_score"
                            ],
                            ascending=False
                        )
                        .head(top_attractions)
                    )





                    # ==========================================
                    # Interest compatibility filtering
                    # ==========================================

                    user_interests = [
                        item["interest"].lower()
                        for item in matched_experiences
                    ]


                    


                    city_attractions = (
                        city_attractions
                        .sort_values(
                            by=[
                                "match_score",
                                "coverage_score",
                                "relevance_score"
                            ],
                            ascending=False
                        )
                        .head(
                            top_attractions
                        )
                    )


                else:

                    city_attractions = (
                        destination_attractions
                        .head(top_attractions)
                    )


            else:

                city_attractions = (
                    destination_attractions
                    .head(top_attractions)
                )



            attraction_list = []



            for _, attraction in city_attractions.iterrows():


                attraction_id = attraction[
                    "attraction_id"
                ]


                attraction_list.append(
                    {

                        "attraction_id":
                            attraction_id,


                        "name":
                            attraction[
                                "attraction_name"
                            ],


                        "category":
                            attraction[
                                "category"
                            ],


                        "indoor_outdoor":
                            attraction.get(
                                "indoor_outdoor"
                            ),


                        "sub_category":
                            attraction[
                                "sub_category"
                            ],


                        "match_score":
                            round(
                                float(
                                    attraction.get(
                                        "match_score",
                                        1.0
                                    )
                                ),
                                3
                            ),


                        "coverage_score":
                            round(
                                float(
                                    attraction.get(
                                        "coverage_score",
                                        1.0
                                    )
                                ),
                                3
                            ),


                        "entry_costs":
                            cost_lookup.get(
                                attraction_id,
                                []
                            )

                    }
                )



            recommendations.append(
                {

                    "destination":
                        destination,


                    "score":
                        1.0,


                    "recommendation_source":
                        (
                            "user_selected_destination"
                        ),


                    "interest_coverage":
                        None,


                    "matching_attractions":
                        len(
                            attraction_list
                        ),


                    "strong_attractions":
                        len(
                            attraction_list
                        ),


                    "attractions":
                        attraction_list

                }
            )



            return {

                "input_interests": interests or [],

                "matched_experiences": matched_experiences,

                "unmatched_interests": unmatched_interests,

                "recommended_destinations": recommendations

            }



# =====================================================
# Agent 1 -> Agent 2 Adapter
# =====================================================

def recommend_from_traveller_profile(
    traveller_profile,
    top_destinations=5,
    top_attractions=5,
    debug=False
):


    agent2_preferences = (

        extract_destination_preferences(
            traveller_profile
        )

    )



    interests = agent2_preferences[
        "interests"
    ]



    preferred_destinations = (

        agent2_preferences.get(
            "preferred_destinations",
            []
        )

    )



    # Explicit destination always gets priority

    if preferred_destinations:


        result = recommend_from_preferred_destinations(

            destinations=preferred_destinations,
            interests=interests,
            top_attractions=top_attractions

        )


        return {

            "status":
                "success",


            "agent2_input":
                agent2_preferences,


            **result

        }



    # Interest based recommendation

    if interests:


        result = recommend_destinations(

            interests=interests,

            top_destinations=top_destinations,

            top_attractions=top_attractions,

            debug=debug

        )


        return {

            "status":
                "success",


            "agent2_input":
                agent2_preferences,


            **result

        }



    return {

        "status":
            "needs_preferences",


        "message":
            (
                "No destination interests "
                "or preferred destinations were provided."
            ),


        "recommended_destinations":
            []

    }