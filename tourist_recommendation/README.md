Travel Suggestion App   

*ABOUT*

This project is a simple web app that helps people decide where to travel.

Inputs :

- Your age  
- Your budget  
- The type of place you like (mountains, beach, city, etc.)  
- How many days you want to travel  

Based on this, the app gives you 3 travel suggestions:

- 1 Best Match (over 90%)
- 2 Good Matches (between 70% and 90%)

It also shows real information about the place — like parks, monuments, or famous spots — so the results feel interesting and not boring.

---

*Assumptions*

1. Finding Places

Instead of manually creating a small list of cities,  used global timezones to randomly pick real cities around the world.

This means:
- The app can suggest endless locations
- Results feel fresh every time
- I don’t need a huge hardcoded database



2. Matching People to Places

I made some simple assumptions:

- Younger people might prefer cheaper, adventure-style trips.
- Older people might prefer comfort and relaxed trips.
- Mountain trips usually need more days.
- City trips can be shorter.

These basic ideas help the app decide what fits best.



3. Getting Real Information

To make the suggestions look real and interesting, the app uses Wikipedia to:

- Get city information
- Find local attractions
- Suggest real places to visit

This keeps the app dynamic instead of static.



*Working of App*

1. Score System

Didn't use complicated AI.

Instead, built a simple points system:

- Every city starts with 0 points.
- If it matches your budget → it gains points.
- If the duration is too short → it loses points.
- If it matches your preferred landscape → it gains points.

At the end:
- The highest score becomes the top suggestion.
- The next two become good alternatives.

Simple and easy to understand.



2. Getting Local Attractions

To find things to do in a city, the app directly asks Wikipedia for related links.

This gives:
- Real names of monuments and parks
- Clean and real data




*Design Choices & Trade-offs*

1. Randomness vs Perfect Accuracy

Because the app chooses random cities worldwide:

You can discover new places  
Sometimes it might pick a small or less exciting town  

I accepted this because it keeps the app fun and dynamic.



2. Simple Budget System

Instead of checking real flight or hotel prices (which is slow and complex), prompted to create:

- A list of “High Budget” countries
- A list of “Low Budget” countries

This keeps the app:
- Fast  
- Simple  
- Reliable  



3. About the Percentages

The app first finds the 3 best matches.

Then:
- The top one is shown as above 90%
- The other two are shown between 70–90%

This makes the results clear and easy to understand for users.



*Edge Cases*

1. Very Short Trips

If someone asks for:
- A 3-day mountain trip  

The app knows that’s probably too short and reduces the score heavily.


2. No Famous Landmarks Found

If the city is very small and Wikipedia has no major attractions:

- The app won’t crash.
- It will suggest general things like:
  - Hiking Trails
  - Local Coastlines
  - City Parks



3. Slow or Broken Website

If Wikipedia is slow or not responding:

- The app waits only 3 seconds.
- Then it skips that city.
- So the user doesn’t experience long delays.



*How to Run*

1. Make sure Python is installed.
2. Open terminal and install required packages:
   pip install flask pytz
3. Run the app:
   python app.py
4. Open the app in your browser


---

What I May Improve in the Future

If I had more time, I would add:

1. Real Travel Prices & Weather
- Connect to real flight and hotel datas
- Show live weather updates


2. A Curated List of Top Tourist Spots
Instead of fully random cities, I would build a database of the:

> “Top 500 Tourist Destinations in the World”

This would ensure every suggestion is exciting and well-known.



*Final Thoughts*

This project is a:

- Simple  
- Fast  
- Easy-to-understand  
- Rule-based  

travel recommendation system.

It doesn’t use complex AI, but it still gives personalized and useful suggestions based on what the user wants.
