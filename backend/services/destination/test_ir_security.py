import requests
from services.destination.agent4_adapter import prepare_agent4_input
from services.destination.destination_recommender import recommend_destinations


def test_IR01_relevant_destination_retrieval():

    # -----------------------------
    # Test Input
    # -----------------------------
    interests = ["hiking", "nature"]

    # -----------------------------
    # Execute the actual retrieval
    # -----------------------------
    result = recommend_destinations(
        interests=interests,
        top_destinations=5,
        top_attractions=5,
        debug=True
    )

    # -----------------------------
    # Display results as evidence
    # -----------------------------
    print("\n========================================")
    print("IR-01: Relevant Destination Retrieval")
    print("========================================")

    print(f"Input interests: {interests}")

    print("\nMatched experiences:")
    for experience in result["matched_experiences"]:
        print(
            f"- {experience.get('interest')} "
            f"(ID: {experience.get('experience_id')})"
        )

    print("\nRecommended destinations:")

    for index, destination in enumerate(
        result["recommended_destinations"],
        start=1
    ):
        print(
            f"{index}. {destination['destination']} "
            f"| Score: {destination['score']} "
            f"| Coverage: {destination['interest_coverage']} "
            f"| Matching attractions: "
            f"{destination['matching_attractions']}"
        )

    # -----------------------------
    # Security / reliability checks
    # -----------------------------

    # The retrieval system should return results
    assert result["recommended_destinations"], (
        "No destinations were retrieved for valid "
        "hiking and nature interests."
    )

    # At least one interest should be recognized
    assert result["matched_experiences"], (
        "The system failed to match the supplied "
        "hiking/nature interests."
    )

    # Every recommendation should contain the required
    # retrieval information
    for destination in result["recommended_destinations"]:

        assert destination["destination"], (
            "A recommendation was returned without "
            "a destination name."
        )

        assert "score" in destination, (
            "A recommendation is missing its retrieval score."
        )

        assert "interest_coverage" in destination, (
            "A recommendation is missing interest coverage."
        )

    # Scores should be ordered from highest to lowest
    scores = [
        destination["score"]
        for destination in result["recommended_destinations"]
    ]

    assert scores == sorted(scores, reverse=True), (
        "Retrieved destinations are not ordered "
        "by descending relevance score."
    )






def test_IR02_multi_interest_retrieval():

    interests = ["hiking", "nature", "photography"]

    result = recommend_destinations(
        interests=interests,
        top_destinations=5,
        top_attractions=5,
        debug=True
    )

    print("\n========================================")
    print("IR-02: Multi-Interest Retrieval")
    print("========================================")

    print(f"Input interests: {interests}")

    print("\nMatched experiences:")
    for experience in result["matched_experiences"]:
        print(
            f"- {experience.get('interest')} "
            f"(ID: {experience.get('experience_id')})"
        )

    print("\nRecommended destinations:")

    for index, destination in enumerate(
        result["recommended_destinations"],
        start=1
    ):
        print(
            f"{index}. {destination['destination']} "
            f"| Score: {destination['score']} "
            f"| Coverage: {destination['interest_coverage']} "
            f"| Matching attractions: "
            f"{destination['matching_attractions']}"
        )

    matched_interests = {
        experience.get("interest")
        for experience in result["matched_experiences"]
    }

    assert set(interests).issubset(matched_interests), (
        "Not all requested interests were matched."
    )

    assert result["recommended_destinations"], (
        "No destinations were retrieved for multiple interests."
    )

    scores = [
        destination["score"]
        for destination in result["recommended_destinations"]
    ]

    assert scores == sorted(scores, reverse=True), (
        "Destinations are not ranked by descending relevance score."
    )







def test_IR03_irrelevant_query_handling():

    interests = ["quantum_computing"]

    result = recommend_destinations(
        interests=interests,
        top_destinations=5,
        top_attractions=5,
        debug=True
    )

    print("\n========================================")
    print("IR-03: Irrelevant Query Handling")
    print("========================================")

    print(f"Input interests: {interests}")

    print("\nMatched experiences:")
    for experience in result["matched_experiences"]:
        print(
            f"- {experience.get('interest')} "
            f"(ID: {experience.get('experience_id')})"
        )

    print("\nRecommended destinations:")

    for index, destination in enumerate(
        result["recommended_destinations"],
        start=1
    ):
        print(
            f"{index}. {destination['destination']} "
            f"| Score: {destination['score']} "
            f"| Coverage: {destination['interest_coverage']} "
            f"| Matching attractions: "
            f"{destination['matching_attractions']}"
        )

    # An irrelevant interest should not be matched
    matched_interests = {
        experience.get("interest")
        for experience in result["matched_experiences"]
    }

    assert "quantum_computing" not in matched_interests, (
        "An irrelevant interest was incorrectly matched."
    )

    # No relevant destination should be retrieved
    assert not result["recommended_destinations"], (
        "Destinations were returned for an irrelevant interest."
    )


def test_IR04_duplicate_keyword_manipulation():

    # Normal input
    normal_interests = ["hiking", "nature"]

    # Manipulated input with duplicated keyword
    manipulated_interests = [
        "hiking",
        "hiking",
        "hiking",
        "nature"
    ]

    # Run retrieval with normal input
    normal_result = recommend_destinations(
        interests=normal_interests,
        top_destinations=5,
        top_attractions=5,
        debug=True
    )

    # Run retrieval with manipulated input
    manipulated_result = recommend_destinations(
        interests=manipulated_interests,
        top_destinations=5,
        top_attractions=5,
        debug=True
    )

    print("\n========================================")
    print("IR-04: Duplicate/Keyword Manipulation")
    print("========================================")

    print(f"Normal input: {normal_interests}")
    print(f"Manipulated input: {manipulated_interests}")

    print("\nNormal results:")

    for i, destination in enumerate(
        normal_result["recommended_destinations"],
        start=1
    ):
        print(
            f"{i}. {destination['destination']} "
            f"| Score: {destination['score']}"
        )

    print("\nManipulated results:")

    for i, destination in enumerate(
        manipulated_result["recommended_destinations"],
        start=1
    ):
        print(
            f"{i}. {destination['destination']} "
            f"| Score: {destination['score']}"
        )

    normal_destinations = [
        d["destination"]
        for d in normal_result["recommended_destinations"]
    ]

    manipulated_destinations = [
        d["destination"]
        for d in manipulated_result["recommended_destinations"]
    ]

    normal_scores = [
        d["score"]
        for d in normal_result["recommended_destinations"]
    ]

    manipulated_scores = [
        d["score"]
        for d in manipulated_result["recommended_destinations"]
    ]

    # Duplicate keywords should not change the retrieved destinations
    assert normal_destinations == manipulated_destinations, (
        "Duplicate keywords changed the retrieved destinations."
    )

    # Duplicate keywords should not change relevance scores
    assert normal_scores == manipulated_scores, (
        "Duplicate keywords changed the relevance scores."
    )



from services.destination.destination_validator import validate_destination


def test_IR05_malicious_invalid_retrieval_data():

    available_destinations = [
        "Colombo",
        "Kandy",
        "Ella",
        "Nuwara Eliya",
        "Dambulla",
        "Sigiriya"
    ]

    malicious_input = "<script>alert('xss')</script>"

    result = validate_destination(
        malicious_input,
        available_destinations
    )

    print("\n========================================")
    print("IR-05: Malicious/Invalid Retrieval Data")
    print("========================================")

    print(f"Input: {malicious_input}")
    print(f"Validation result: {result}")

    # Malicious/invalid input must not be accepted
    assert result["status"] != "valid", (
        "Malicious input was incorrectly accepted as a valid destination."
    )

    # It should not map to an actual destination
    assert result["destination"] is None, (
        "Malicious input was mapped to a valid destination."
    )

    print("Result: Malicious input was rejected.")





def test_IR06_unsupported_information():

    interests = ["hiking", "nature"]

    result = recommend_destinations(
        interests=interests,
        top_destinations=5,
        top_attractions=5,
        debug=True
    )

    print("\n========================================")
    print("IR-06: Unsupported Information")
    print("========================================")

    print(f"Input interests: {interests}")

    print("\nRetrieved information:")

    for index, destination in enumerate(
        result["recommended_destinations"],
        start=1
    ):
        print(
            f"{index}. {destination['destination']} "
            f"| Score: {destination['score']} "
            f"| Coverage: {destination['interest_coverage']} "
            f"| Matching attractions: "
            f"{destination['matching_attractions']}"
        )

    # Every returned destination must have supporting
    # retrieval information.
    for destination in result["recommended_destinations"]:

        assert destination["destination"], (
            "A recommendation was returned without "
            "a destination name."
        )

        assert destination["matching_attractions"] > 0, (
            f"Unsupported destination returned: "
            f"{destination['destination']}"
        )

        assert destination["interest_coverage"] > 0, (
            f"Destination has no supporting interest coverage: "
            f"{destination['destination']}"
        )

    print("\nResult: All retrieved destinations have supporting data.")




def test_IR07_retrieval_context_mismatch():

    interests = ["hiking", "nature"]

    result = recommend_destinations(
        interests=interests,
        top_destinations=5,
        top_attractions=5,
        debug=True
    )

    print("\n========================================")
    print("IR-07: Retrieval-Context Mismatch")
    print("========================================")

    print(f"Input interests: {interests}")

    print("\nRetrieved destinations:")

    for index, destination in enumerate(
        result["recommended_destinations"],
        start=1
    ):
        print(
            f"{index}. {destination['destination']} "
            f"| Score: {destination['score']} "
            f"| Coverage: {destination['interest_coverage']} "
            f"| Matching attractions: "
            f"{destination['matching_attractions']}"
        )

    # Every retrieved destination should have some
    # context overlap with the requested interests.
    for destination in result["recommended_destinations"]:

        assert destination["interest_coverage"] > 0, (
            f"Context mismatch: {destination['destination']} "
            f"has no interest coverage."
        )

        assert destination["matching_attractions"] > 0, (
            f"Context mismatch: {destination['destination']} "
            f"has no matching attractions."
        )

    print("\nResult: All retrieved destinations have relevant context.")


def test_IR08_source_consistency():

    interests = ["hiking", "nature"]

    # First retrieval
    first_result = recommend_destinations(
        interests=interests,
        top_destinations=5,
        top_attractions=5,
        debug=True
    )

    # Second retrieval using the same input
    second_result = recommend_destinations(
        interests=interests,
        top_destinations=5,
        top_attractions=5,
        debug=True
    )

    print("\n========================================")
    print("IR-08: Source Consistency")
    print("========================================")

    print(f"Input interests: {interests}")

    first_destinations = [
        (d["destination"], d["score"])
        for d in first_result["recommended_destinations"]
    ]

    second_destinations = [
        (d["destination"], d["score"])
        for d in second_result["recommended_destinations"]
    ]

    print("\nFirst retrieval:")
    for destination, score in first_destinations:
        print(f"- {destination} | Score: {score}")

    print("\nSecond retrieval:")
    for destination, score in second_destinations:
        print(f"- {destination} | Score: {score}")

    # Same source data and same input should produce
    # consistent retrieval results.
    assert first_destinations == second_destinations, (
        "Retrieval results were inconsistent across repeated executions."
    )

    print("\nResult: Retrieval results remained consistent.")

def test_IR09_missing_outdated_information():

    available_destinations = [
        "Colombo",
        "Kandy",
        "Ella",
        "Nuwara Eliya",
        "Dambulla",
        "Sigiriya"
    ]

    # Destination not available in the current retrieval data
    missing_destination = "Mirissa"

    result = validate_destination(
        missing_destination,
        available_destinations
    )

    print("\n========================================")
    print("IR-09: Missing/Outdated Information")
    print("========================================")

    print(f"Input destination: {missing_destination}")
    print(f"Available destinations: {available_destinations}")
    print(f"Validation result: {result}")

    # A destination that is not present in the available
    # data must not be accepted as valid.
    assert result["status"] != "valid", (
        "Missing destination information was accepted as valid."
    )

    assert result["destination"] is None, (
        "A destination missing from the available data "
        "was incorrectly returned as valid."
    )

    print("\nResult: Missing destination information was not accepted.")

def test_SEC01_unauthenticated_api_access():

    url = "http://127.0.0.1:8000/api/planner/route"

    # Valid request structure, but NO authentication token
    request_body = {
        "trip_id": "SEC-TEST-01",
        "destinations": ["Kandy", "Ella"]
    }

    response = requests.post(
        url,
        json=request_body
    )

    print("\n========================================")
    print("SEC-01: Unauthenticated API Access")
    print("========================================")

    print(f"Endpoint: {url}")
    print("Authentication: None")
    print(f"HTTP Status: {response.status_code}")
    print(f"Response: {response.text}")

    # Protected endpoint should reject unauthenticated access
    assert response.status_code in [401, 403], (
        "Protected API accepted an unauthenticated request."
    )

    print("\nResult: Unauthenticated access was rejected.")

def test_SEC02_invalid_expired_token():

    url = "http://127.0.0.1:8000/api/planner/route"

    request_body = {
        "trip_id": "SEC-TEST-02",
        "destinations": ["Kandy", "Ella"]
    }

    headers = {
        "Authorization": "Bearer invalid.token.value"
    }

    response = requests.post(
        url,
        json=request_body,
        headers=headers
    )

    print("\n========================================")
    print("SEC-02: Invalid/Expired Token")
    print("========================================")

    print(f"Endpoint: {url}")
    print("Authentication: Invalid JWT token")
    print(f"HTTP Status: {response.status_code}")
    print(f"Response: {response.text}")

    # Invalid/expired tokens should be rejected
    assert response.status_code in [401, 403], (
        "API accepted an invalid or expired authentication token."
    )

    print("\nResult: Invalid token was rejected.")


def test_SEC03_unauthorized_protected_operation():

    url = "http://127.0.0.1:8000/api/planner/route"

    request_body = {
        "trip_id": "SEC-TEST-03",
        "destinations": ["Kandy", "Ella"]
    }

    headers = {
        "Authorization": "Bearer unauthorized.user.token"
    }

    response = requests.post(
        url,
        json=request_body,
        headers=headers
    )

    print("\n========================================")
    print("SEC-03: Unauthorized Protected Operation")
    print("========================================")

    print(f"Endpoint: {url}")
    print("User: Unauthorized user")
    print(f"HTTP Status: {response.status_code}")
    print(f"Response: {response.text}")

    # Unauthorized users should not be allowed to perform
    # protected operations.
    assert response.status_code in [401, 403], (
        "Unauthorized user was allowed to perform a protected operation."
    )

    print("\nResult: Unauthorized operation was rejected.")


def test_API01_invalid_input():

    url = "http://127.0.0.1:8000/api/planner/route"

    # Invalid request:
    # trip_id should be a string
    # destinations should be a list
    request_body = {
        "trip_id": 12345,
        "destinations": "Kandy"
    }

    response = requests.post(
        url,
        json=request_body
    )

    print("\n========================================")
    print("API-01: Invalid Input")
    print("========================================")

    print(f"Endpoint: {url}")
    print(f"Invalid input: {request_body}")
    print(f"HTTP Status: {response.status_code}")
    print(f"Response: {response.text}")

    # Invalid input should be rejected by the API
    assert response.status_code == 422, (
        "API accepted invalid input instead of rejecting it."
    )

    print("\nResult: Invalid input was rejected.")

def test_API02_malicious_oversized_input():

    url = "http://127.0.0.1:8000/api/planner/route"

    # Controlled oversized input
    oversized_trip_id = "A" * 10000
    oversized_destinations = ["Kandy"] * 1000

    request_body = {
        "trip_id": oversized_trip_id,
        "destinations": oversized_destinations
    }

    response = requests.post(
        url,
        json=request_body,
        timeout=30
    )

    print("\n========================================")
    print("API-02: Malicious/Oversized Input")
    print("========================================")

    print("Endpoint:", url)
    print("Input: Oversized trip_id and destination list")
    print(f"trip_id length: {len(oversized_trip_id)}")
    print(f"Number of destinations: {len(oversized_destinations)}")
    print(f"HTTP Status: {response.status_code}")
    print(f"Response: {response.text[:500]}")

    # The API should reject an oversized request rather than
    # processing it normally.
    assert response.status_code in [400, 413, 422], (
        "API accepted oversized input instead of rejecting it."
    )

    print("\nResult: Oversized input was rejected.")



def test_COM01_invalid_agent_message():

    # Invalid Agent 2 message:
    # recommended_destinations should be a list,
    # but an invalid string is provided.
    invalid_message = {
        "recommended_destinations": "INVALID_DATA"
    }

    print("\n========================================")
    print("COM-01: Invalid Agent Message")
    print("========================================")

    print(f"Input message: {invalid_message}")

    # Prepare the message for Agent 4
    result = prepare_agent4_input(
        invalid_message
    )

    print(f"Prepared Agent 4 input: {result}")

    # The invalid message should be rejected.
    # A valid Agent 2 message should contain a list.
    assert isinstance(
        invalid_message["recommended_destinations"],
        list
    ), (
        "Invalid Agent 2 message was accepted "
        "without validation."
    )

    print("\nResult: Invalid agent message was rejected.")


def test_COM02_manipulated_agent_data():

    manipulated_message = {
        "recommended_destinations": [
            {
                "destination": "Ella",
                "score": 9999,
                "attractions": []
            }
        ]
    }

    print("\n========================================")
    print("COM-02: Manipulated Agent Data")
    print("========================================")

    print(f"Input message: {manipulated_message}")

    result = prepare_agent4_input(
        manipulated_message
    )

    print(f"Prepared Agent 4 input: {result}")

    manipulated_score = result["destinations"][0]["recommendation_score"]

    print(f"Manipulated recommendation score: {manipulated_score}")

    # Recommendation score should be within the valid 0–1 range.
    assert 0 <= manipulated_score <= 1, (
        "Manipulated recommendation score was accepted "
        "without validation."
    )

    print("\nResult: Manipulated agent data was rejected.")