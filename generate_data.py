import pandas as pd
import numpy as np

np.random.seed(42)

# ── 1. DEFINE NEIGHBORHOODS ───────────────────────────────────────────────────
# We're modeling neighborhoods in a fictional US city
# Each has real latitude/longitude coordinates (based on Chicago areas)
neighborhoods = [
    {"name": "Riverside Heights",  "lat": 41.8781, "lng": -87.6298},
    {"name": "Oak Park East",       "lat": 41.8850, "lng": -87.7845},
    {"name": "Lakeview North",      "lat": 41.9430, "lng": -87.6530},
    {"name": "Downtown Core",       "lat": 41.8827, "lng": -87.6233},
    {"name": "Westfield",           "lat": 41.8700, "lng": -87.7200},
    {"name": "Northgate",           "lat": 41.9800, "lng": -87.6600},
    {"name": "South Harbor",        "lat": 41.8300, "lng": -87.6100},
    {"name": "Elmwood District",    "lat": 41.9100, "lng": -87.7100},
    {"name": "Midtown East",        "lat": 41.8950, "lng": -87.6400},
    {"name": "Greenfield Park",     "lat": 41.9300, "lng": -87.7400},
    {"name": "University Row",      "lat": 41.7900, "lng": -87.6000},
    {"name": "Harbor View",         "lat": 41.8600, "lng": -87.5900},
    {"name": "West Commons",        "lat": 41.8750, "lng": -87.7600},
    {"name": "Parkside",            "lat": 41.9600, "lng": -87.7000},
    {"name": "Industrial North",    "lat": 41.9900, "lng": -87.7200},
]

# ── 2. GENERATE SCORES FOR EACH FACTOR ───────────────────────────────────────
# Each factor is scored 0-100 (higher = better)
# We use realistic distributions so some neighborhoods are clearly better

n = len(neighborhoods)

data = []
for i, hood in enumerate(neighborhoods):
    
    # Crime Safety Score (0=very dangerous, 100=very safe)
    # Downtown and Industrial areas tend to have more crime
    if "Downtown" in hood["name"] or "Industrial" in hood["name"]:
        crime_safety = np.random.randint(30, 55)
    elif "University" in hood["name"] or "Harbor" in hood["name"]:
        crime_safety = np.random.randint(45, 70)
    else:
        crime_safety = np.random.randint(55, 95)

    # School Quality Score
    # University areas and wealthy neighborhoods have better schools
    if "University" in hood["name"] or "Oak Park" in hood["name"]:
        school_quality = np.random.randint(75, 98)
    elif "Industrial" in hood["name"] or "South" in hood["name"]:
        school_quality = np.random.randint(30, 55)
    else:
        school_quality = np.random.randint(50, 85)

    # Transit Access Score (proximity to public transport)
    # Downtown and Lakeview have great transit
    if "Downtown" in hood["name"] or "Lakeview" in hood["name"]:
        transit_access = np.random.randint(80, 100)
    elif "West" in hood["name"] or "Elmwood" in hood["name"]:
        transit_access = np.random.randint(35, 60)
    else:
        transit_access = np.random.randint(50, 80)

    # Air Quality Score (higher = cleaner air)
    # Industrial areas have worse air quality
    if "Industrial" in hood["name"]:
        air_quality = np.random.randint(20, 45)
    elif "Park" in hood["name"] or "Green" in hood["name"]:
        air_quality = np.random.randint(75, 98)
    else:
        air_quality = np.random.randint(50, 85)

    # Walkability Score (can you walk to shops, restaurants, etc.)
    if "Downtown" in hood["name"] or "Midtown" in hood["name"]:
        walkability = np.random.randint(80, 100)
    elif "West" in hood["name"] or "Industrial" in hood["name"]:
        walkability = np.random.randint(20, 45)
    else:
        walkability = np.random.randint(45, 80)

    # Green Space Score (parks, trees, nature)
    if "Park" in hood["name"] or "Green" in hood["name"]:
        green_space = np.random.randint(75, 98)
    elif "Downtown" in hood["name"] or "Industrial" in hood["name"]:
        green_space = np.random.randint(15, 40)
    else:
        green_space = np.random.randint(40, 80)

    # Median Home Price (realistic US city prices)
    base_price = 250000
    price_modifier = (crime_safety + school_quality + walkability) / 3
    median_home_price = int(base_price + (price_modifier * 3000) + np.random.randint(-20000, 20000))

    data.append({
        "neighborhood":      hood["name"],
        "lat":               hood["lat"],
        "lng":               hood["lng"],
        "crime_safety":      crime_safety,
        "school_quality":    school_quality,
        "transit_access":    transit_access,
        "air_quality":       air_quality,
        "walkability":       walkability,
        "green_space":       green_space,
        "median_home_price": median_home_price,
    })

# ── 3. CALCULATE COMPOSITE LIVABILITY SCORE ──────────────────────────────────
# This is the weighted average of all factors
# Weights represent how much each factor matters
# They must add up to 1.0

df = pd.DataFrame(data)

DEFAULT_WEIGHTS = {
    "crime_safety":   0.25,  # 25% - Safety is most important
    "school_quality": 0.20,  # 20% - Schools matter a lot for families
    "transit_access": 0.15,  # 15% - Getting around matters
    "air_quality":    0.15,  # 15% - Health factor
    "walkability":    0.15,  # 15% - Lifestyle factor
    "green_space":    0.10,  # 10% - Nice to have
}

def calculate_livability(row, weights):
    """Calculate weighted composite score for a neighborhood"""
    score = sum(row[factor] * weight for factor, weight in weights.items())
    return round(score, 1)

df["livability_score"] = df.apply(
    lambda row: calculate_livability(row, DEFAULT_WEIGHTS), axis=1
)

# Rank neighborhoods by livability
df["rank"] = df["livability_score"].rank(ascending=False).astype(int)
df = df.sort_values("livability_score", ascending=False).reset_index(drop=True)

# ── 4. SAVE DATA ──────────────────────────────────────────────────────────────
df.to_csv("neighborhoods.csv", index=False)

print("✅ Generated neighborhood data!")
print(f"\n🏆 Top 5 Most Livable Neighborhoods:")
print(df[["rank", "neighborhood", "livability_score"]].head())
print(f"\n⚠️  Bottom 5 Neighborhoods:")
print(df[["rank", "neighborhood", "livability_score"]].tail())
print(f"\n📊 Score Statistics:")
print(df["livability_score"].describe().round(1))