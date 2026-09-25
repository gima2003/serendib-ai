from typing import List, Dict, Any



def format_food_response(
    results: List[Dict[str, Any]]
):

    formatted = []


    for place in results:


        formatted.append(

            {

                # ==========================
                # Basic Restaurant Information
                # ==========================

                "restaurant_name":
                    place.get(
                        "place_name",
                        "Unknown Restaurant"
                    ),


                "city":
                    place.get(
                        "city"
                    ),


                "area":
                    place.get(
                        "area"
                    ),


                "address":
                    place.get(
                        "address"
                    ),


                "place_type":
                    place.get(
                        "place_type"
                    ),



                # ==========================
                # Food Information
                # ==========================

                "cuisine_type":
                    place.get(
                        "cuisine_focus"
                    ),


                "signature_dishes":
                    place.get(
                        "signature_dishes"
                    ),



                "recommended_dishes":
                    [

                        dish.get(
                            "food_name"
                        )

                        for dish in place.get(
                            "dishes",
                            []
                        )

                        if isinstance(
                            dish,
                            dict
                        )

                    ],



                # ==========================
                # User Preference Matching
                # ==========================

                "dietary_strength":
                    place.get(
                        "dietary_strength"
                    ),


                "local_food_strength":
                    place.get(
                        "local_food_strength"
                    ),



                "best_for":
                    place.get(
                        "best_for"
                    ),



                # ==========================
                # Recommendation Information
                # ==========================

                "rating":
                    place.get(
                        "rating"
                    ),


                "review_count":
                    place.get(
                        "review_count"
                    ),


                "price_level":
                    place.get(
                        "price_band_lkr"
                    ),



                "retrieval_score":
                    place.get(
                        "retrieval_score",
                        0
                    ),



                "reasoning":

                    place.get(
                        "recommendation_reasoning"
                    )

                    or

                    place.get(
                        "match_reasons",
                        []
                    ),



                # ==========================
                # External Information
                # ==========================

                "opening_hours":
                    place.get(
                        "opening_hours"
                    ),


                "phone":
                    place.get(
                        "phone"
                    ),


                "map_query":
                    place.get(
                        "map_query"
                    ),


                "photo_url":
                    place.get(
                        "photo_url"
                    ),



                # ==========================
                # Social / Trust Signals
                # ==========================

                "social_signals":
                    place.get(
                        "social_signals",
                        []
                    ),



                "source":

                    place.get(
                        "source"
                    )

            }

        )


    return formatted