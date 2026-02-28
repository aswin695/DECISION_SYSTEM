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

def determine_budget(region):
    if region in ['Europe', 'US', 'Canada', 'Australia', 'Pacific']:
        return 'High'
    elif region in ['Asia', 'Africa', 'America']: 
        return 'Low'
    return 'Medium'

def get_realtime_recommendations(age, budget, landscape, duration):
    all_tzs = [tz for tz in pytz.common_timezones if '/' in tz and not tz.startswith('Etc/')]
    
    # Randomly sample to keep API calls reasonable per request
    sample_tzs = random.sample(all_tzs, min(25, len(all_tzs)))
    
    scored_destinations = []
    
    for tz_name in sample_tzs:
        parts = tz_name.split('/')
        region = parts[0]
        city_raw = parts[-1]
        city_name = city_raw.replace('_', ' ')
            
        tz = pytz.timezone(tz_name)
        local_time = datetime.now(tz)
        hour = local_time.hour
        
        info = get_city_info(city_name)
        if not info:
            continue
            
        dest_landscape = determine_landscape(info['description'])
        dest_budget = determine_budget(region)
        
        score = 0
        
        if dest_landscape == landscape:
            score += 50
            
        if dest_budget == budget:
            score += 30
        elif (dest_budget == 'Low' and budget in ['Medium', 'High']):
            score += 15
        elif (dest_budget == 'Medium' and budget == 'High'):
            score += 15
            
        min_days = 2
        if duration >= min_days:
            score += 10
            
        # Real-time scoring based on current time
        # Boost places where it's currently daytime
        if 8 <= hour <= 18: 
            score += 35
        elif 6 <= hour < 8 or 18 < hour <= 21:
            score += 15
        else:
            score -= 10
            
        if score > 0:
            # Shorten description
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
