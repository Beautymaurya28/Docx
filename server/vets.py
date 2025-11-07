from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel, Field
from typing import List, Optional
import httpx

from models import User
from security import get_current_user  # Our route-protection dependency
from config import settings            # To get our secret API key

# 1. --- Define our new router ---
router = APIRouter(
    prefix="/api/vets",
    tags=["Vets"]
)

# 2. --- Define the *clean* response model we will send to our app ---
class VetPublic(BaseModel):
    """
    A simplified Vet model that we send to the frontend.
    """
    place_id: str
    name: str
    address: str
    lat: float
    lng: float
    rating: float = 0
    total_ratings: int = 0
    phone: Optional[str] = None # We'll add this in Phase 5
    
    class Config:
        from_attributes = True

# 3. --- The "Nearby Vets" Endpoint ---
@router.get("/nearby", response_model=List[VetPublic])
async def get_nearby_vets(
    lat: float,  # The frontend will provide this (e.g., 19.0760)
    lng: float,  # The frontend will provide this (e.g., 72.8777)
    current_user: User = Depends(get_current_user) # This protects the route
):
    """
    Fetches a list of nearby veterinarians from the Google Places API.
    """
    GOOGLE_PLACES_URL = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
    
    # Parameters for our Google API request
    params = {
        "location": f"{lat},{lng}",
        "radius": 5000,  # 5km radius, as per our plan
        "keyword": "veterinarian", # The most important part
        "key": settings.GOOGLE_PLACES_API_KEY
    }

    # 4. --- Make the async request to Google ---
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(GOOGLE_PLACES_URL, params=params)
        
        response.raise_for_status() # Raises an error if Google returns 4xx or 5xx
        data = response.json()
        
    except httpx.HTTPStatusError as e:
        print(f"Google API Error: {e}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Error fetching data from Google"
        )
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An internal error occurred"
        )
        
    # 5. --- Parse Google's complex response into our clean list ---
    vets_list: List[VetPublic] = []
    
    for place in data.get("results", []):
        # Extract location safely
        location = place.get("geometry", {}).get("location", {})
        
        # Ensure we have the minimum required data
        if not all([
            place.get("place_id"),
            place.get("name"),
            place.get("vicinity"), # 'vicinity' is Google's name for the address
            location.get("lat"),
            location.get("lng")
        ]):
            continue # Skip this result if it's missing key info

        # Build our clean VetPublic object
        vet = VetPublic(
            place_id=place["place_id"],
            name=place["name"],
            address=place["vicinity"],
            lat=location["lat"],
            lng=location["lng"],
            rating=place.get("rating", 0),
            total_ratings=place.get("user_ratings_total", 0)
        )
        vets_list.append(vet)
        
    return vets_list