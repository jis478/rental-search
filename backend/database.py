import json
import aiosqlite

DB_PATH = "rental_search.db"


async def init_db():
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute("""
            CREATE TABLE IF NOT EXISTS searches (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                query TEXT NOT NULL,
                search_params TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        await db.execute("""
            CREATE TABLE IF NOT EXISTS listings (
                id INTEGER PRIMARY KEY,
                search_id INTEGER,
                listing_type TEXT,
                price_display TEXT,
                bedrooms INTEGER,
                bathrooms INTEGER,
                carspaces INTEGER,
                property_type TEXT,
                suburb TEXT,
                state TEXT,
                postcode TEXT,
                address TEXT,
                headline TEXT,
                description TEXT,
                image_url TEXT,
                latitude REAL,
                longitude REAL,
                agent_name TEXT,
                listing_slug TEXT,
                raw_json TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (search_id) REFERENCES searches(id)
            )
        """)
        await db.commit()


async def save_search(query: str, search_params: dict) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cursor = await db.execute(
            "INSERT INTO searches (query, search_params) VALUES (?, ?)",
            (query, json.dumps(search_params)),
        )
        await db.commit()
        return cursor.lastrowid


async def save_listings(search_id: int, listings: list[dict]):
    async with aiosqlite.connect(DB_PATH) as db:
        for item in listings:
            listing = item.get("listing", item)
            prop = listing.get("propertyDetails", {})
            price = listing.get("priceDetails", {})
            media = listing.get("media", [])
            geo = prop.get("geoLocation", {})
            advertiser = listing.get("advertiser", {})

            listing_id = listing.get("id")
            if not listing_id:
                continue

            await db.execute(
                """INSERT OR REPLACE INTO listings
                   (id, search_id, listing_type, price_display, bedrooms, bathrooms,
                    carspaces, property_type, suburb, state, postcode, address,
                    headline, description, image_url, latitude, longitude,
                    agent_name, listing_slug, raw_json)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (
                    listing_id,
                    search_id,
                    listing.get("listingType"),
                    price.get("displayPrice"),
                    prop.get("bedrooms"),
                    prop.get("bathrooms"),
                    prop.get("carspaces"),
                    prop.get("propertyType"),
                    prop.get("suburb"),
                    prop.get("state"),
                    prop.get("postcode"),
                    prop.get("displayableAddress"),
                    listing.get("headline"),
                    listing.get("summaryDescription"),
                    media[0].get("url") if media else None,
                    geo.get("latitude"),
                    geo.get("longitude"),
                    advertiser.get("name"),
                    listing.get("listingSlug"),
                    json.dumps(item),
                ),
            )
        await db.commit()


async def get_searches():
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute(
            "SELECT id, query, search_params, created_at FROM searches ORDER BY created_at DESC LIMIT 50"
        )
        rows = await cursor.fetchall()
        return [dict(row) for row in rows]


async def get_listing(listing_id: int):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        cursor = await db.execute("SELECT * FROM listings WHERE id = ?", (listing_id,))
        row = await cursor.fetchone()
        return dict(row) if row else None
