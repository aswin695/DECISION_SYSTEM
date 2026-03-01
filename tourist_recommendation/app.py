import random
import urllib.request
import urllib.parse
import urllib.error
import json
from datetime import datetime
import pytz
from flask import Flask, render_template, request

app = Flask(__name__)

# Cache for Wikipedia results to avoid slow repeated lookups
wiki_cache = {}

def get_city_info(city_name):
    if city_name in wiki_cache:
        return wiki_cache[city_name]
        
    url = f"https://en.wikipedia.org/api/rest_v1/page/summary/{urllib.parse.quote(city_name)}"
    req = urllib.request.Request(url, headers={'User-Agent': 'WanderlustApp/1.0'})
    try:
        with urllib.request.urlopen(req, timeout=3) as response:
            data = json.loads(response.read().decode())
            
            image_url = ""
            if 'thumbnail' in data and 'source' in data['thumbnail']:
                image_url = data['thumbnail']['source']
            elif 'originalimage' in data and 'source' in data['originalimage']:
                image_url = data['originalimage']['source']
            else:
                image_url = "https://images.unsplash.com/photo-1488085061387-422e29b40080?q=80&w=800&auto=format&fit=crop"
                
            info = {
                "description": data.get('extract', 'A beautiful destination to explore.'),
                "image_url": image_url
            }
            wiki_cache[city_name] = info
            return info
    except Exception as e:
        return None

def determine_landscape(description):
    desc_lower = description.lower()
    if any(word in desc_lower for word in ['beach', 'coast', 'island', 'sea', 'ocean', 'sand']):
        return 'Beach'
    if any(word in desc_lower for word in ['mountain', 'peak', 'alps', 'andes', 'himalaya', 'valley', 'volcano']):
        return 'Mountains'
    if any(word in desc_lower for word in ['city', 'capital', 'metropolis', 'urban', 'center', 'largest']):
        return 'City'
    return 'Countryside'

# Create a mapping from timezone back to country code
timezone_country = {}
for countrycode in pytz.country_timezones:
    for tz in pytz.country_timezones[countrycode]:
        timezone_country[tz] = countrycode

def determine_budget(tz_name):
    country_code = timezone_country.get(tz_name)
    
    # High Budget Countries (Luxury)
    high_budget = [
        'US', 'GB', 'FR', 'DE', 'CH', 'JP', 'AU', 'CA', 'NO', 'SE', 
        'DK', 'FI', 'NL', 'BE', 'AT', 'IE', 'NZ', 'SG', 'IS', 'AE', 
        'QA', 'LU', 'MC', 'IL', 'BS', 'BM', 'KY'
    ]
    
    # Low Budget Countries (Backpacker)
    low_budget = [
        'IN', 'ID', 'VN', 'TH', 'PH', 'EG', 'MA', 'PE', 'CO', 'BO', 
        'KE', 'TZ', 'NP', 'LK', 'KH', 'MG', 'PK', 'BD', 'MM', 'LA', 
        'GT', 'HN', 'NI', 'SV', 'EC', 'PY', 'ZW', 'ZM', 'MW', 'UG',
        'SN', 'GH', 'DZ', 'TN'
    ]
    
    if country_code in high_budget:
        return 'High'
    elif country_code in low_budget:
        return 'Low'
    return 'Medium'

def get_realtime_recommendations(age, budget, landscape, duration):
    all_tzs = [tz for tz in pytz.common_timezones if '/' in tz and not tz.startswith('Etc/')]
    
    # Shuffle to ensure variety, but we don't lock to a tiny sample.
    random.shuffle(all_tzs)
    
    scored_destinations = []
    
    # Limit max API calls to avoid unacceptably long loading times if no perfect matches are found.
    api_calls = 0
    max_api_calls = 40
    
    for tz_name in all_tzs:
        # Check if we have 3 very strong matches (Score >= 70 basically ensures landscape and budget met)
        good_matches = [dest for score, dest in scored_destinations if score >= 70]
        if len(good_matches) >= 3:
            break
            
        if api_calls >= max_api_calls:
            break
            
        parts = tz_name.split('/')
        region = parts[0]
        city_raw = parts[-1]
        city_name = city_raw.replace('_', ' ')
            
        tz = pytz.timezone(tz_name)
        local_time = datetime.now(tz)
        hour = local_time.hour
        
        info = get_city_info(city_name)
        api_calls += 1
        
        if not info:
            continue
            
        dest_landscape = determine_landscape(info['description'])
        dest_budget = determine_budget(tz_name)
        
        score = 0
        
        # 1. Strictly weight landscape matches.
        if dest_landscape == landscape:
            score += 60
        else:
            score -= 40  # Heavy penalty for wrong landscape
            
        # 2. Strictly weight budget matches.
        if dest_budget == budget:
            score += 30
        elif (dest_budget == 'Low' and budget in ['Medium', 'High']):
            score += 15  # Being cheaper is still somewhat acceptable
        elif (dest_budget == 'Medium' and budget == 'High'):
            score += 15
        else:
            score -= 20  # Penalize if it's over budget
            
        # 3. Consider Age
        # Give logical bonuses to make the trip worthy for their life stage
        if age < 30:
            if dest_budget == 'Low': score += 10
            if dest_landscape in ['City', 'Mountains']: score += 10
        elif 30 <= age < 50:
            if dest_budget == 'Medium': score += 10
            if dest_landscape in ['Beach', 'City']: score += 10
        else: # 50+
            if dest_budget in ['Medium', 'High']: score += 10
            if dest_landscape in ['Countryside', 'Beach']: score += 10
            
        # 4. Duration - ensuring the trip is worthy of the time
        if dest_landscape == 'Mountains':
            min_days = 4
        elif dest_landscape == 'Countryside':
            min_days = 3
        elif dest_landscape == 'Beach':
            min_days = 3
        else:
            min_days = 2 # City
            
        if duration < min_days:
            score -= 40  # Heavy penalty: Trip is too short to be worthy
        elif duration >= min_days + 3:
            score += 20  # Bonus: Plenty of days to fully experience it!
        else:
            score += 10  # Good amount of time
            
        # 5. Real-time timezone boosting
        if 8 <= hour <= 18: 
            score += 15
        elif 6 <= hour < 8 or 18 < hour <= 21:
            score += 5
        else:
            score -= 5
            
        # Only keep it if it's somewhat decent
        if score > 0:
            desc = info['description']
            if len(desc) > 180:
                desc = desc[:177] + "..."
                
            dest_data = {
                "name": f"{city_name}, {region}",
                "landscape": dest_landscape,
                "budget": dest_budget,
                "min_days": min_days,
                "description": desc,
                "image_url": info['image_url'],
                "local_time": local_time.strftime("%I:%M %p"),
                "time_status": "Daytime ☀️" if 6 <= hour <= 18 else "Nighttime 🌙"
            }
            scored_destinations.append((score, dest_data))
            
    scored_destinations.sort(key=lambda x: x[0], reverse=True)
    return [item[1] for item in scored_destinations[:3]]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        try:
            age = int(request.form.get('age', 25))
            budget = request.form.get('budget', 'Medium')
            landscape = request.form.get('landscape', 'Beach')
            duration = int(request.form.get('duration', 5))
            
            recommendations = get_realtime_recommendations(age, budget, landscape, duration)
            return render_template('recommendation.html', recommendations=recommendations)
        except Exception as e:
            print("Error:", e)
            return render_template('index.html', error="Please provide valid inputs or try searching again.")
            
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
