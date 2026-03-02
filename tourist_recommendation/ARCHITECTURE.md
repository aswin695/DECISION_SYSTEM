# System Architecture

This document outlines the high-level architecture, data movement, and decision logic that powers the Travel Suggestion application.

## 1. Architecture Diagram
This diagram shows the basic structure of the client-server relationship and external data sources.

```mermaid
graph TD
    Client["User Interface (Web Browser)"] <-->|Submit Form / Returns HTML| FlaskServer["Python Flask Backend"]
    
    subgraph "Server Environment"
        FlaskServer <-->|Retrieves Timezones & Constraints| StaticData["Static Country & Budget Sets"]
        FlaskServer <-->|Parallel Lookups| ThreadPool["Concurrent Execution Pool"]
    end
    
    ThreadPool <-->|HTTP JSON Queries| WikipediaAPI["Wikipedia REST API"]
```

## 2. Data Flow Diagram (DFD)
This diagram details how the user's input flows through the internal functions to eventually generate the top three travel outputs.

```mermaid
graph TD
    User([User Submit Form]) --> InputProcess((1. Parse Inputs))
    InputProcess -- "Age, Budget, Landscape, Duration" --> Filter((2. Randomize Timezones))
    
    DataStore[(Global Timezone Data)] --> Filter
    Filter -- "40 Random Cities" --> WikiProcess((3. Fetch Wikipedia Data))
    
    WikiProcess -- "Concurrent Requests" --> WikiAPI["Wikipedia API"]
    WikiAPI -- "City Descriptions & Images" --> ValidCities((4. Pass to Scoring Engine))
    
    ValidCities -- "Valid Wikipedia Response" --> ScoringEngine((5. Calculate Points))
    ScoringEngine -- "Ranked Cities (Filtered > 0)" --> Formatting((6. Apply Percentages & Insights))
    
    Formatting -- "1 >90% Match, 2 >70% Matches" --> Output([Final Travel Report])
```

## 3. Decision Logic Diagram
This diagram shows the core heuristic engine: how points are strictly added or subtracted based on whether a city meets the user's constraints.

```mermaid
flowchart TD
    Start["User Inputs: Age=25, Landscape=Mountains, Budget=Medium"] --> Initialize["Start City Score at 0"]
    
    Initialize --> BudgetCheck{"Does Country Budget Match User Input?"}
    BudgetCheck -- "Exact Match" --> AddBudget["+30 Points"]
    BudgetCheck -- "Country is Cheaper" --> AddPartialBudget["+15 Points"]
    BudgetCheck -- "Country is Too Expensive" --> SubBudget["-20 Points (Penalty)"]
    
    AddBudget --> LandscapeCheck
    AddPartialBudget --> LandscapeCheck
    SubBudget --> LandscapeCheck
    
    LandscapeCheck{"Does Location Landscape Match?"}
    LandscapeCheck -- Yes --> AddLandscape["+60 Points"]
    LandscapeCheck -- No --> SubLandscape["-40 Points (Penalty)"]
    
    AddLandscape --> DurationCheck
    SubLandscape --> DurationCheck
    
    DurationCheck{"Is User Duration >= Min Required Days?"}
    DurationCheck -- "Yes, With Extra Days" --> AddDuration["+20 Points (Bonus)"]
    DurationCheck -- "Yes, Exactly" --> AddBaseDuration["+10 Points"]
    DurationCheck -- "No, Trip Too Short" --> SubDuration["-40 Points (Penalty)"]
    
    AddDuration --> FinalCheck
    AddBaseDuration --> FinalCheck
    SubDuration --> FinalCheck
    
    FinalCheck{"Final Score > 0?"}
    FinalCheck -- Yes --> Keep["Keep Destination for Ranking"]
    FinalCheck -- No --> Discard["Discard City"]
```
