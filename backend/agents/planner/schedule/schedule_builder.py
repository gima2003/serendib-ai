import uuid
from typing import List, Dict, Any, Optional
from collections import defaultdict

from agents.planner.schedule.schemas import (
    ScheduleAgentRequest,
    ScheduleResponse,
    DailySchedule,
    ScheduledActivity
)

def build_itinerary(request: ScheduleAgentRequest) -> ScheduleResponse:
    """
    Main builder for the Schedule Agent.
    Transforms specialist outputs into a chronological itinerary covering ALL trip days.
    """
    profile = request.profile
    total_days = max(1, profile.duration_days or 1)
    
    # 1. Determine destination sequence from Route Agent
    route_plan = request.route_plan
    
    # Route summary.destinations is a list like ["Kandy", "Nuwara Eliya", "Ella"]
    # It does NOT include the start location. We add it from route_summary.start_location.
    ordered_cities: List[str] = []
    
    if route_plan.route_summary:
        if route_plan.route_summary.start_location:
            ordered_cities.append(route_plan.route_summary.start_location)
        if route_plan.route_summary.destinations:
            ordered_cities.extend(route_plan.route_summary.destinations)
    
    # Fallback to destinations list if route summary is incomplete
    if not ordered_cities:
        ordered_cities = [
            d.get("city") or d.get("destination", "")
            for d in request.destinations
            if d.get("city") or d.get("destination")
        ]
        if profile.starting_location and ordered_cities and profile.starting_location.lower() != ordered_cities[0].lower():
            ordered_cities.insert(0, profile.starting_location)
    
    # Remove duplicates preserving order (case-insensitive)
    unique_ordered_cities: List[str] = []
    seen_norm = set()
    for c in ordered_cities:
        if c and c.lower().strip() not in seen_norm:
            unique_ordered_cities.append(c)
            seen_norm.add(c.lower().strip())

    if not unique_ordered_cities:
        unique_ordered_cities = ["Colombo"]

    # 2. Day Allocation — distribute total_days across destinations
    # Priority: use accommodation nights if available, else distribute evenly
    city_nights: Dict[str, int] = {}
    for stay in request.stays:
        if stay.nights > 0:
            city_nights[stay.city] = stay.nights
    
    # If accommodation gave us nights, verify they add up; adjust if needed
    total_acc_nights = sum(city_nights.values())
    
    if total_acc_nights != total_days or not city_nights:
        # Redistribute: evenly divide days across unique cities
        # Give each city at least 1 night
        n_cities = len(unique_ordered_cities)
        base_nights = max(1, total_days // n_cities)
        remainder = total_days - base_nights * n_cities
        
        city_nights = {}
        for idx, city in enumerate(unique_ordered_cities):
            nights = base_nights + (1 if idx < remainder else 0)
            city_nights[city] = max(1, nights)
    
    # 3. Match Context and Safety data
    # Safety segment warnings (keyed by "to" city)
    safety_warnings: Dict[str, List[str]] = defaultdict(list)
    for segment in (request.safety_plan.route_segments if request.safety_plan else []):
        dest_city = segment.get("to_location") or segment.get("to", "")
        if dest_city:
            if segment.get("risk_level", "").upper() not in ("LOW", ""):
                safety_warnings[dest_city].append(f"Safety risk on this leg: {segment.get('risk_level', 'UNKNOWN')}")
    
    # Context weather/crowd keyed by location name
    crowd_data: Dict[str, Any] = {}
    if request.context_plan:
        for cp in request.context_plan.crowd_predictions:
            crowd_data[cp.location] = cp

    weather_data: Dict[str, Any] = {}
    if request.context_plan:
        for wp in request.context_plan.weather_predictions:
            weather_data[wp.location] = wp

    # 4. Build lookup maps for destinations and food
    dest_map: Dict[str, Dict] = {}
    for d in request.destinations:
        key = d.get("city") or d.get("destination", "")
        if key:
            dest_map[key] = d
    
    # FIX: food_map should be city → LIST of restaurants (not single item overwriting)
    food_map: Dict[str, List[Dict]] = defaultdict(list)
    for f in request.food_options:
        city_key = f.get("city") or f.get("destination", "")
        if city_key:
            food_map[city_key].append(f)

    # 5. Process Itinerary Days
    itinerary: List[DailySchedule] = []
    current_day = 1
    
    for i, city in enumerate(unique_ordered_cities):
        if current_day > total_days:
            break
            
        nights = city_nights.get(city, 1)
        # Cap nights so we don't exceed total_days
        nights = min(nights, total_days - current_day + 1)
        if nights <= 0:
            nights = 1

        # Attraction pool for this city
        city_dest_info = dest_map.get(city, {})
        attractions: List[Dict] = list(city_dest_info.get("attractions", []))
        
        # Restaurant pool for this city
        restaurants: List[Dict] = list(food_map.get(city, []))
        
        # Accommodation: find selected hotel
        stay_info = next((s for s in request.stays if s.city == city), None)
        selected_hotel = None
        if stay_info:
            for opt in stay_info.hotel_options:
                if opt.is_selected:
                    selected_hotel = opt
                    break
            # Fallback: pick first available option if none is selected
            if not selected_hotel and stay_info.hotel_options:
                selected_hotel = stay_info.hotel_options[0]
        
        attr_index = 0
        rest_index = 0
        
        for n in range(nights):
            if current_day > total_days:
                break
            
            daily_activities: List[ScheduledActivity] = []
            daily_warnings: List[str] = []
            notes: List[str] = []
            
            # --- MORNING: Travel or Activity ---
            if n == 0 and i > 0:
                # Travel from previous city
                prev_city = unique_ordered_cities[i - 1]
                travel_duration = 120  # Default 2h
                leg = next(
                    (l for l in route_plan.legs if l.from_location == prev_city and l.to_location == city), None
                )
                if leg and leg.road_route:
                    travel_duration = leg.road_route.estimated_duration_minutes
                
                daily_activities.append(ScheduledActivity(
                    activity_id=str(uuid.uuid4()),
                    time="Morning",
                    name=f"Travel from {prev_city} to {city}",
                    type="travel",
                    description=f"Estimated travel time: {int(travel_duration)} minutes by car.",
                    duration_minutes=int(travel_duration)
                ))
                notes.append(f"Travel to {city} occupies the morning.")
                
                # Late Morning Attraction
                if attr_index < len(attractions):
                    attr = attractions[attr_index]
                    daily_activities.append(ScheduledActivity(
                        activity_id=str(uuid.uuid4()),
                        time="Late Morning",
                        name=attr.get("name", "Local Attraction"),
                        type="attraction",
                        description=attr.get("sub_category", ""),
                    ))
                    attr_index += 1
            else:
                # Morning Attraction 1
                if attr_index < len(attractions):
                    attr = attractions[attr_index]
                    weather_note = [f"Weather: {weather_data[city].weather_condition} {weather_data[city].temperature:.0f}°C"] if city in weather_data else []
                    daily_activities.append(ScheduledActivity(
                        activity_id=str(uuid.uuid4()),
                        time="Morning",
                        name=attr.get("name", "Local Attraction"),
                        type="attraction",
                        description=attr.get("sub_category", ""),
                        warnings=safety_warnings.get(city, []) + weather_note
                    ))
                    attr_index += 1
                
                # Late Morning Attraction 2
                if attr_index < len(attractions):
                    attr = attractions[attr_index]
                    daily_activities.append(ScheduledActivity(
                        activity_id=str(uuid.uuid4()),
                        time="Late Morning",
                        name=attr.get("name", "Local Attraction"),
                        type="attraction",
                        description=attr.get("sub_category", ""),
                    ))
                    attr_index += 1

            if attr_index >= len(attractions) and not any(a.type == "attraction" for a in daily_activities):
                daily_activities.append(ScheduledActivity(
                    activity_id=str(uuid.uuid4()),
                    time="Morning",
                    name=f"Explore {city}",
                    type="leisure",
                    description=f"Free time to explore the local area of {city}.",
                ))
            
            # --- LUNCH ---
            if rest_index < len(restaurants):
                rest = restaurants[rest_index]
                daily_activities.append(ScheduledActivity(
                    activity_id=str(uuid.uuid4()),
                    time="Lunch",
                    name=rest.get("place_name", "Local Restaurant"),
                    type="meal",
                    description=rest.get("reasoning", f"Lunch at {rest.get('place_name', 'a local restaurant')}")
                ))
                rest_index += 1
            
            # --- AFTERNOON ---
            afternoon_added = False
            # Afternoon Attraction 1
            if attr_index < len(attractions):
                attr = attractions[attr_index]
                daily_activities.append(ScheduledActivity(
                    activity_id=str(uuid.uuid4()),
                    time="Afternoon",
                    name=attr.get("name", "Local Attraction"),
                    type="attraction",
                    description=attr.get("sub_category", ""),
                ))
                attr_index += 1
                afternoon_added = True
                
            # Late Afternoon / Evening Attraction 2
            if attr_index < len(attractions):
                attr = attractions[attr_index]
                daily_activities.append(ScheduledActivity(
                    activity_id=str(uuid.uuid4()),
                    time="Evening",
                    name=attr.get("name", "Local Attraction"),
                    type="attraction",
                    description=attr.get("sub_category", ""),
                ))
                attr_index += 1
                afternoon_added = True
                
            if not afternoon_added:
                daily_activities.append(ScheduledActivity(
                    activity_id=str(uuid.uuid4()),
                    time="Afternoon",
                    name=f"Leisure time in {city}",
                    type="leisure",
                    description="Relax or explore at your own pace.",
                ))
                
            # --- CHECK-IN ---
            if n == 0 and selected_hotel:
                daily_activities.append(ScheduledActivity(
                    activity_id=str(uuid.uuid4()),
                    time="16:00",
                    name=f"Check-in at {selected_hotel.name}",
                    type="accommodation",
                    description=f"Accommodation in {city}."
                ))
                
            # --- DINNER ---
            if rest_index < len(restaurants):
                rest = restaurants[rest_index]
                daily_activities.append(ScheduledActivity(
                    activity_id=str(uuid.uuid4()),
                    time="19:00",
                    name=rest.get("place_name", "Local Restaurant"),
                    type="meal",
                    description=rest.get("reasoning", "")
                ))
                rest_index += 1
            else:
                daily_activities.append(ScheduledActivity(
                    activity_id=str(uuid.uuid4()),
                    time="19:00",
                    name=f"Dinner in {city}",
                    type="meal",
                    description="Enjoy local cuisine."
                ))
                
            # --- CHECK-OUT note on last night of city stay ---
            if n == nights - 1 and i < len(unique_ordered_cities) - 1:
                daily_activities.append(ScheduledActivity(
                    activity_id=str(uuid.uuid4()),
                    time="Next Morning",
                    name="Check-out and prepare for next destination",
                    type="accommodation"
                ))

            # Crowd / weather context warnings
            if city in crowd_data:
                cp = crowd_data[city]
                daily_warnings.append(
                    f"Crowd Level: {cp.crowd_level}" +
                    (f" — {cp.recommendations[0]}" if cp.recommendations else "")
                )
            
            if city in weather_data:
                wp = weather_data[city]
                daily_warnings.append(f"Weather: {wp.weather_condition}, {wp.temperature:.0f}°C, Rain: {wp.rain_probability}%")
            
            if profile.travel_pace and profile.travel_pace.value == "relaxed":
                notes.append("Relaxed pace — no rushing between sites.")
                
            hotel_dict = selected_hotel.model_dump() if selected_hotel else None
                
            itinerary.append(DailySchedule(
                day=current_day,
                city=city,
                activities=daily_activities,
                accommodation=hotel_dict,
                warnings=daily_warnings,
                notes=notes
            ))
            current_day += 1
    
    # Sanity check: if we generated fewer days than expected (e.g., city list ended early)
    # extend with last city leisure days
    while current_day <= total_days and unique_ordered_cities:
        last_city = unique_ordered_cities[-1]
        itinerary.append(DailySchedule(
            day=current_day,
            city=last_city,
            activities=[
                ScheduledActivity(
                    activity_id=str(uuid.uuid4()),
                    time="09:00",
                    name=f"Free day in {last_city}",
                    type="leisure",
                    description="Explore the area or relax before departure."
                )
            ],
            accommodation=itinerary[-1].accommodation if itinerary else None,
            warnings=[],
            notes=["Final day — flexible schedule."]
        ))
        current_day += 1

    budget_summary = {}
    if request.budget_plan:
        budget_summary = {
            "available": request.budget_plan.available_budget_lkr,
            "estimated_cost": request.budget_plan.estimated_total_cost_lkr,
            "utilization_percent": request.budget_plan.budget_utilization_percent,
            "within_budget": request.budget_plan.within_budget
        }
    
    overall_warnings: List[str] = []
    if request.safety_plan:
        overall_warnings.extend(request.safety_plan.warnings)
    if request.budget_plan:
        overall_warnings.extend(request.budget_plan.warnings)
    
    return ScheduleResponse(
        trip_id=request.budget_plan.trip_id if request.budget_plan else "TRIP-001",
        status="completed",
        itinerary=itinerary,
        budget_summary=budget_summary,
        overall_warnings=overall_warnings,
        planning_notes=[
            f"Itinerary covers {len(itinerary)} days across {len(unique_ordered_cities)} destinations.",
            "Generated from specialist agent outputs."
        ]
    )
