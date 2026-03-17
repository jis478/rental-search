import json
from openai import AsyncOpenAI
from config import OPENAI_API_KEY
from models import ParsedQuery, SearchParams

client = AsyncOpenAI(api_key=OPENAI_API_KEY)

SYSTEM_PROMPT = """You are a rental property search assistant for Australian properties.
Given a natural language query, extract structured search parameters for the Domain.com.au API.

Extract the following when mentioned:
- listingType: always "Rent" unless the user says they want to buy
- propertyTypes: list from ["House", "Apartment", "Townhouse", "Unit", "Studio", "Villa"]
- minBedrooms / maxBedrooms: bedroom count or range
- minBathrooms / maxBathrooms: bathroom count or range
- minCarspaces: car spaces needed
- minPrice / maxPrice: weekly rent in AUD
- locations: list of {state, suburb, postcode, includeSurroundingSuburbs, surroundingRadiusInMeters}
  - Default includeSurroundingSuburbs to true unless user is very specific
  - Australian states: NSW, VIC, QLD, SA, WA, TAS, NT, ACT
- keywords: any extra filters like "pet friendly", "pool", "furnished", "balcony"

Also return a friendly message describing what you're searching for.

If the user's query is ambiguous or conversational (not a property search), still do your best to interpret it as a search, or return sensible defaults with an appropriate message."""

SEARCH_TOOL = {
    "type": "function",
    "function": {
        "name": "search_properties",
        "description": "Search for rental properties with structured parameters",
        "parameters": {
            "type": "object",
            "required": ["message", "searchParams"],
            "properties": {
                "message": {
                    "type": "string",
                    "description": "A friendly message describing the search being performed",
                },
                "searchParams": {
                    "type": "object",
                    "properties": {
                        "listingType": {
                            "type": "string",
                            "enum": ["Rent", "Sale"],
                            "default": "Rent",
                        },
                        "propertyTypes": {
                            "type": "array",
                            "items": {
                                "type": "string",
                                "enum": [
                                    "House",
                                    "ApartmentUnitFlat",
                                    "Townhouse",
                                    "Studio",
                                    "Villa",
                                ],
                            },
                        },
                        "minBedrooms": {"type": "integer"},
                        "maxBedrooms": {"type": "integer"},
                        "minBathrooms": {"type": "integer"},
                        "maxBathrooms": {"type": "integer"},
                        "minCarspaces": {"type": "integer"},
                        "minPrice": {"type": "integer"},
                        "maxPrice": {"type": "integer"},
                        "locations": {
                            "type": "array",
                            "items": {
                                "type": "object",
                                "properties": {
                                    "state": {"type": "string"},
                                    "suburb": {"type": "string"},
                                    "postcode": {"type": "string"},
                                    "includeSurroundingSuburbs": {
                                        "type": "boolean",
                                        "default": True,
                                    },
                                    "surroundingRadiusInMeters": {"type": "integer"},
                                },
                            },
                        },
                        "keywords": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                    },
                },
            },
        },
    },
}


async def parse_query(query: str) -> ParsedQuery:
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": query},
        ],
        tools=[SEARCH_TOOL],
        tool_choice={"type": "function", "function": {"name": "search_properties"}},
    )

    tool_call = response.choices[0].message.tool_calls[0]
    parsed = json.loads(tool_call.function.arguments)

    search_params = SearchParams(**parsed.get("searchParams", {}))

    return ParsedQuery(
        message=parsed.get("message", "Searching for properties..."),
        searchParams=search_params,
    )
