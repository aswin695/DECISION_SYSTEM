# Data Flow Diagram (DFD)

This document contains the Data Flow Diagrams defining how data moves through the Travel Suggestion application.

## Level 0 DFD (Context Diagram)
This shows the highest level view of the system, illustrating how the user interacts with the app as a whole.

```mermaid
graph LR
    User([User]) -- "Travel Preferences (Age, Budget, Landscape, Duration)" --> System((Travel Suggestion App))
    System -- "3 Tailored Travel Recommendations" --> User
    
    System -- "Request Location Data" --> Wiki["Wikipedia API"]
    Wiki -- "Return Location Information (Images, Descriptions)" --> System
```

## Level 1 DFD (Process Level)
This breaks down the main system into detailed internal processes, showing step-by-step how the data is transformed to generate the suggestions.

```mermaid
graph TD
    %% Entities
    User([User])
    Wiki["Wikipedia API"]

    %% Processes
    P1((1. Process Inputs))
    P2((2. Generate Global Candidates))
    P3((3. Fetch Wikipedia Data))
    P4((4. Calculate Match Scores))
    P5((5. Format and Rank))

    %% Data Stores
    D1[(Static Data Sets)]

    %% Flow Level 1
    User -- "Age, Budget, Landscape, Duration" --> P1
    P1 -- "Cleaned Preferences" --> P4

    D1 -- "Timezones & Countries list" --> P2
    P2 -- "40 Random Cities (Timezones)" --> P3

    P3 -- "City Names" --> Wiki
    Wiki -- "Descriptions, Images, Links" --> P3
    P3 -- "Valid City Profiles" --> P4

    D1 -- "Budget Definitions (High/Low)" --> P4
    P4 -- "Scored Destinations" --> P5

    P5 -- "(1) >90% Match \n (2) 70-90% Match" --> User
```

### Process Explanations
- **1. Process Inputs**: Receives the form submission from the user and prepares it for calculation.
- **2. Generate Global Candidates**: Grabs a randomized chunk of exactly 40 global timezones to ensure the app gives different possible results every single time.
- **3. Fetch Wikipedia Data**: Speaks to Wikipedia using the 40 random cities simultaneously (Concurrent futures) to get their pictures and real-world monument names.
- **4. Calculate Match Scores**: Compares the user's Preferences (from Step 1) against the downloaded valid cities (from Step 3) using a strict points system (e.g., matching the budget, checking duration limits).
- **5. Format and Rank**: Takes the highest scoring locations, locks the top result to an overt 90%+ match and strings together the final custom pitches before sending them back to the user's screen.
