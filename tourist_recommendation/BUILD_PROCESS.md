Build Process

I started this project thinking about two different ideas:
1. Choosing a laptop under a budget
2. Picking an investment strategy

I actually wrote some code for these ideas, but eventually, I deleted it, as the first one could be the majority pick while the 2nd one had a wide variety of options and was somewhat complex to me. I realized that a Travel Recommendation app would be much more good to build. It allowed me to use interesting inputs like a person's age, their budget, how many days they had, and what kind of trip they liked (like beaches, mountains, or cities).

How My Thinking Evolved -

At first, I thought about making a simple, fixed list of 50 travel destinations. But I realized that would get boring quickly if people kept getting the exact same suggestions over and over.

So, my thinking evolved: instead of a fixed list, I decided to use worldwide timezones to randomly pick cities across the globe. This way, the app could suggest endless, unique places every time you clicked search!

Alternative Approaches Considered -

1. Using AI: I considered using a smart AI to read the user's inputs and pick the best city. But AI can be tricky, slow, and expensive. Instead, I built a simple "points system" where a city just earns points if it matches the user's budget and landscape choice.

2. Live Flight Prices: I thought about connecting the app to a real travel website to fetch live ticket prices. But that takes too long to load. So as an alternative, I just created a simple list of "Expensive Countries" and "Cheap Countries". This trick keeps the app extremely fast.

Cleaned the Code -

1. Making it Faster: In the beginning, the app was very slow. It took over 15 seconds to load because it was asking Wikipedia for information on 40 different cities one by one. I changed the code so that it asks Wikipedia about all 40 cities at the exact same time. Now the app loads in just a few seconds

2. Cleaning the Logic: I originally had huge blocks of messy code to assign the icons and descriptions. I cleaned this up by grouping them into simple, neat, organized lists.

Mistakes and Corrections-

1. App Crashes: I originally wrote some code that tried to read thick paragraphs of Wikipedia text to find the names of local parks or monuments. But the code got confused by the long text and kept freezing the entire app, I fixed this mistake by changing the app to simply ask Wikipedia for a clean list of "related links" instead. It never crashes anymore.
2. Wrong Budget Guesses: Early on, the app was guessing a country's average cost based purely on its continent. This was a mistake because it wasn't accurate. I corrected it by making the app check the exact country name to give a much more accurate budget rating.

Changes while on Development-

1. Match Scores: During the build, a new rule was added requiring specific percentage numbers on the screen. The top suggestion needed to say it was over a "90% match", and the other two had to say they were between "70% and 90%". I updated the display code to guarantee these exact numbers always show up.

2. Minimum Days Requirement: I realized that suggesting a short 2-day trip to a remote mountain or countryside didn't make much sense because traveling there takes too long. So I changed the app to demand more vacation days if the user wanted a nature trip.