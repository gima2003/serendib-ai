from .text_utils import normalize_text


def match_interests_to_experiences(
    interests,
    experiences
):

    matched = []

    seen = set()

    for interest in interests:

        normalized_interest = (
            normalize_text(
                interest
            )
        )

        for _, experience in (
            experiences.iterrows()
        ):

            experience_name = (
                normalize_text(
                    experience[
                        "experience_name"
                    ]
                )
            )

            keywords = str(
                experience[
                    "preference_keywords"
                ]
            ).split("|")

            normalized_keywords = [
                normalize_text(
                    keyword
                )
                for keyword in keywords
            ]

            match_type = None
            match_strength = 0.0

            if (
                normalized_interest
                ==
                experience_name
            ):

                match_type = (
                    "exact_name"
                )

                match_strength = 1.0

            elif (
                normalized_interest
                in normalized_keywords
            ):

                match_type = (
                    "exact_keyword"
                )

                match_strength = 0.95

            if match_type:

                key = (
                    normalized_interest,
                    experience[
                        "experience_id"
                    ],
                )

                if key in seen:
                    continue

                seen.add(key)

                matched.append(
                    {
                        "interest":
                            interest,

                        "experience_id":
                            experience[
                                "experience_id"
                            ],

                        "experience_name":
                            experience[
                                "experience_name"
                            ],

                        "match_type":
                            match_type,

                        "match_strength":
                            match_strength,
                    }
                )

    return matched