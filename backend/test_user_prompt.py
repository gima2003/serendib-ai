import asyncio
import json
import httpx
from main import app

async def main():
    transport = httpx.ASGITransport(app=app)
    async with httpx.AsyncClient(transport=transport, base_url="http://test", timeout=120.0) as client:
        # 1. First we need to extract the profile using the extract endpoint
        prompt = "I want a 7-day Sri Lanka family holiday with my wife and two children. We will start from Colombo. We have a budget of 150,000 LKR. We prefer safe places, beaches, wildlife, and easy activities suitable for children. We need affordable family-friendly hotels, restaurants with different food options, and a comfortable travel schedule without too much driving."
        
        print("Extracting profile...")
        extract_res = await client.post("/profile/extract", json={"text": prompt})
        
        if extract_res.status_code != 200:
            print("Failed to extract profile:")
            print(extract_res.text)
            return
            
        profile_data = extract_res.json()
        print(f"Profile extracted: duration={profile_data.get('duration_days')}, budget={profile_data.get('budget', {}).get('amount')} {profile_data.get('budget', {}).get('currency')}")
        
        print("Generating trip via LangGraph...")
        # 2. Now call the master generate endpoint
        generate_res = await client.post("/api/trips/generate", json={
            "raw_user_request": prompt,
            "traveller_profile": profile_data
        })
        
        if generate_res.status_code != 200:
            print("Failed to generate trip:")
            print(generate_res.text)
            return
            
        trip_data = generate_res.json()
        print("Trip generated successfully!")
        
        with open("test_output_final.json", "w", encoding="utf-8") as f:
            json.dump(trip_data, f, indent=2)
            
        print("Validating outputs:")
        
        schedule = trip_data.get("schedule_plan", {})
        itinerary = schedule.get("itinerary", [])
        print(f"- Itinerary days generated: {len(itinerary)}")
        
        route = trip_data.get("route_plan", {})
        summary = route.get("route_summary", {})
        print(f"- Route start: {summary.get('start_location')}, destinations: {summary.get('destinations')}")
        
        budget = trip_data.get("budget_plan", {})
        breakdown = budget.get("cost_breakdown", {})
        print(f"- Budget categories: Accommodation={breakdown.get('accommodation_lkr')}, Food={breakdown.get('food_lkr')}, Transport={breakdown.get('transport_lkr')}, Attractions={breakdown.get('attractions_lkr')}")

if __name__ == "__main__":
    asyncio.run(main())
