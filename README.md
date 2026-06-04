# GambStats

## Overview
GambStats is a gambling activity tracking application designed to help users log casino trips, sessions, and individual games for later analysis.

Rather than focusing only on win/loss totals, the application is designed to capture structured behavioral data that can reveal patterns in casino activity, bankroll decisions, session pacing, and game-level outcomes.

This repository currently focuses on the MVP backend: a serverless API for managing trips, sessions, and games.
## Problem Statement
Many gamblers track little more than overall wins and losses, making it difficult to identify patterns in spending, session behavior, and decision-making. During casino visits, players often make decisions in environments specifically designed to encourage continued play and emotional decision-making.

GambStats aims to provide a structured system for tracking gambling activity at the trip, session, and game level, creating a foundation for self-analysis, responsible gambling habits, and future behavioral insights.

## MVP Goals
The MVP serves to accomplish the following benchmarks:
  - Create, validate, and persist gambling activity across trip, session, and game entities
  - Provide persistent storage and retrieval of gambling activity through DynamoDB 
  - Create a functioning web application for user input 

## Future Enhancements (2.0+)
Future Enhancements include the following:
  - User authentication and profile management
  - A dashboard with a suite of analytical reports
  - Customizable fields within a trip, session, and game  
  - Budget creation and tracking with real-time display at trip and session-level
  - Multi-user functionality to track and store individual play with a combined budget
  - Customizable notifications to alert to potential unwise game play
---

## Features

### Trip Management
Each trip belongs to a single user and includes a required name, location, budget, and start date/time. Users may also add notes and an optional end date/time.

Trips are active by default. A trip is marked completed when an end date/time is provided, as long as there are no active child sessions. Active trips may contain sessions; completed trips cannot be used to create new sessions.

For MVP flexibility, completed trips may still be edited to correct entry mistakes. Additional lifecycle constraints, including stricter reopen behavior, are planned for a future version.
### Session Management
Each session belongs to a single trip and represents a user-defined collection of gambling activity. A session includes a required casino and may optionally include start date/time, end date/time, and notes.

Sessions are active by default. A session is marked completed when an end date/time is provided, provided the session has no active child games. Active sessions may contain games, while completed sessions cannot be used to create new games.

For MVP flexibility, completed sessions may still be edited to correct entry mistakes.
### Game Management
A game is the smallest unit of tracked activity and belongs to a single session. Each game includes a required name, game type, and cash-in amount, with optional cash-out, start date/time, end date/time, notes, entry mode, and free play used.

Games are active by default. A game is marked completed once a cash-out amount is provided. Active games prevent the parent session, and therefore the parent trip, from being completed.

Completed games may still be edited to correct entry mistakes.

---

## Architecture

### High-Level Architecture

The GambStats MVP backend is a serverless API built using Python and AWS services. The application follows a layered architecture consisting of handlers, services, repositories, and schemas.

User requests are processed through AWS Lambda functions, validated through service and schema layers, and persisted in Amazon DynamoDB.

Frontend functionality is planned for a future phase of development.

### Technology Stack

#### Backend

- Python
- AWS Lambda
- Pydantic
- JSON-based REST API design

#### Database

- Amazon DynamoDB
- NoSQL document storage

#### Cloud Services

- AWS Lambda
- Amazon DynamoDB

#### Testing

- Pytest
- Automated integration-style testing
- 68 passing tests covering trip, session, and game workflows
---

## Project Structure
The backend follows a layered architecture with handlers, services, repositories, and schemas organized by domain entity.

```text
src/
├── common/
├── trips/
├── sessions/
├── games/

tests/
├── helpers/
├── trips/
├── sessions/
└── games/
```

---

## Data Model

### Trip

#### Fields
Trip fields include the following:
  - trip_id (Primary Key)
  - user_id
  - trip_name
  - location
  - trip_budget
  - started_at
  - ended_at
  - created_at
  - status 
  - notes

#### Status Lifecycle
If no ended_at is provided upon creation, status is set to "active". Status becomes "completed" when an ended_at value is provided and all child sessions have been completed.

#### Relationships

- One user may own many trips.
- A trip belongs to exactly one user.
- One trip may contain many sessions.
- A session belongs to exactly one trip.

#### Business Rules

Trip business rules include the following:

- Users cannot modify trip_id, user_id, created_at, or status directly.
- A trip cannot be completed while active child sessions exist.
- Status automatically updates to completed when ended_at is provided and all child sessions have been completed.
- Users cannot create new sessions under a completed trip.
- Users cannot delete a trip that contains sessions.
- Completed trips may still be edited to correct entry mistakes.

#### Validation Rules
Trip validation rules are as follows:
- trip_name is required.
- location is required.
- trip_budget is required.
- started_at is required.
- If ended_at is provided, it must not be prior to started_at.
- trip_budget cannot be less than 0.

---

### Session

#### Fields
Session fields include the following:
- session_id (Primary Key)
- user_id
- trip_id
- casino
- started_at
- ended_at
- created_at
- status
- notes

#### Status Lifecycle
If no ended_at is provided upon creation, status is set to "active". Status becomes "completed" when an ended_at value is provided and all child games have been completed.

#### Relationships

- A trip may contain many sessions.
- A session belongs to exactly one trip.
- A session may contain many games.
- A game belongs to exactly one session.

#### Business Rules
Session business rules include the following:
- Users cannot modify session_id, trip_id, user_id, created_at, or status directly.
- A session cannot be completed while active child games exist.
- Status automatically updates to completed when ended_at is provided and all child games have been completed.
- Users cannot create new games under a completed session.
- Users cannot delete a session that contains child games.
- Completed sessions may still be edited to correct entry mistakes.

#### Validation Rules
Session validation rules are as follows:
- casino is required.
- started_at is required.
- If ended_at is provided, it must not be prior to started_at.

---

### Game

#### Fields
Game fields include the following:
- game_id (Primary Key)
- session_id
- trip_id
- user_id
- game_name
- game_type
- cash_in
- cash_out
- status
- started_at
- ended_at
- created_at
- notes
- entry_mode
- freeplay_used

#### Status Lifecycle
If no cash_out is provided upon creation, status is set to "active". Status becomes "completed" when a cash_out value is provided. 

#### Relationships

- A session may contain many games.
- A game belongs to exactly one session.
- A game belongs to exactly one trip.

#### Business Rules
Game business rules are as follows:
- Users cannot modify game_id, session_id, trip_id, user_id, created_at, or status directly.
- Status automatically updates to completed when cash_out is provided.
- Removing cash_out automatically returns the game to active status.
- Active games prevent parent sessions and trips from being completed.
- Completed games may still be edited to correct entry mistakes.

#### Validation Rules
Game validation rules are as follows:
- game_name is required.
- game_type is required.
- cash_in is required.
- If cash_in is 0, freeplay_used must be greater than 0.
- If ended_at is provided, cash_out must also be provided.
- If ended_at is provided, it must not be prior to started_at.
- cash_in, cash_out, and freeplay_used cannot be less than 0.

---

## API Endpoints

### Trips

#### POST /trips
Creates a new trip.

Required body fields:
- trip_name
- location
- trip_budget
- started_at

Optional body fields:
- ended_at
- notes

Returns:
- Created trip object

Common errors:
- 400 validation_error — missing required field or invalid value

#### GET /trips
Returns all trips for the current user.

Optional query params:
- status: active | completed

Returns:
- All trips belonging to the current user

#### GET /trips/{trip_id}
Returns a single trip by ID.

Returns:
- Single trip object

Common errors:
- 400 bad_request — trip_id is required
- 404 not_found — trip not found

#### PATCH /trips/{trip_id}
Updates an existing trip.

Editable fields:
- trip_name
- location
- trip_budget
- started_at
- ended_at
- notes

Returns:
- Updated trip object

Common errors:
- 400 bad_request — trip_id is required
- 400 validation_error — invalid value
- 404 not_found — trip not found

#### DELETE /trips/{trip_id}
Deletes a trip if it has no child sessions.

Returns:
- Confirmation of successful deletion

Common errors:
- 400 bad_request — trip_id is required
- 400 bad_request — cannot delete a trip with sessions
- 404 not_found — trip not found

---

### Sessions

#### POST /trips/{trip_id}/sessions
Creates a new session.

Required body fields:
- casino
- started_at

Optional body fields:
- ended_at
- notes

Returns:
- Created session object

Common errors:
- 400 validation_error — missing required field or invalid value
- 400 bad_request — trip must be active to create a session

#### GET /sessions/{session_id}
Returns a single session by ID.

Returns:
- Single session object

Common errors:
- 400 bad_request — session_id is required
- 404 not_found — session not found

#### GET /trips/{trip_id}/sessions
Returns all sessions for the provided trip.

Returns:
- All sessions belonging to the trip

Common errors:
- 400 bad_request — trip_id is required
- 404 not_found — trip not found

#### PATCH /sessions/{session_id}
Updates an existing session.

Editable fields:
- casino
- started_at
- ended_at
- notes

Returns:
- Updated session object

Common errors:
- 400 bad_request — session_id is required
- 400 validation_error — invalid value
- 404 not_found — session not found

#### DELETE /sessions/{session_id}
Deletes a session if it has no child games.

Returns:
- Confirmation of successful deletion

Common errors:
- 400 bad_request — session_id is required
- 400 bad_request — cannot delete a session that contains child games
- 404 not_found — session not found

---

### Games

#### POST /sessions/{session_id}/games
Creates a new game.

Required body fields:
- game_name
- game_type
- cash_in

Optional body fields:
- cash_out
- started_at
- ended_at
- notes
- entry_mode
- freeplay_used

Returns:
- Created game object

Common errors:
- 400 validation_error — missing required field or invalid value
- 400 bad_request — session must be active to create a game


#### GET /games/{game_id}
Returns a single game by ID.

Returns:
- Single game object

Common errors:
- 400 bad_request — game_id is required
- 404 not_found — game not found

#### GET /sessions/{session_id}/games
Returns all games for the provided session.

Returns:
- All games belonging to the session

Common errors:
- 400 bad_request — session_id is required
- 404 not_found — session not found

#### PATCH /games/{game_id}
Updates an existing game.

Editable fields:
- game_name
- game_type
- cash_in
- cash_out
- started_at
- ended_at
- notes
- entry_mode
- freeplay_used

Returns:
- Updated game object

Common errors:
- 400 bad_request — game_id is required
- 400 validation_error — invalid value
- 404 not_found — game not found

#### DELETE /games/{game_id}
Deletes a game.

Returns:
- Confirmation of successful deletion

Common errors:
- 400 bad_request — game_id is required
- 404 not_found — game not found

---

## Testing

### Test Strategy
The GambStats backend uses automated integration-style tests to validate API behavior, entity lifecycle management, business rules, and data validation.

Tests focus on:

- Successful CRUD operations
- Validation failures
- Parent-child relationship constraints
- Entity lifecycle transitions
- Error handling scenarios

### Test Organization

Tests are organized by entity:

```text
tests/
├── helpers/
├── trips/
├── sessions/
└── games/
```

### Running Tests
```bash
PYTHONPATH=. python -m pytest -v
```

### Current Test Coverage
Current automated test coverage includes:

- Trip CRUD operations
- Session CRUD operations
- Game CRUD operations
- Validation rules
- Parent-child lifecycle restrictions
- Status transition logic
- Error handling scenarios

Current status:
- 68 passing tests
- 2 skipped tests (authentication/profile functionality planned for future implementation)

---

## Local Development

### Prerequisites
- Python 3.13+
- AWS Account (optional for local development)
- DynamoDB tables configured
- Python virtual environment

### Installation

```bash
git clone <repo>
cd gambstats
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```


### Environment Variables
- TRIPS_TABLE
- SESSIONS_TABLE
- GAMES_TABLE

### Running Tests
```bash
PYTHONPATH=. python -m pytest -v
```

---

## Future Roadmap

### Authentication
Status: Planned

User authentication and profile management using Amazon Cognito.

### Wallet / Bankroll Management
Status: Planned

Trip-level and session-level bankroll tracking, budget management, and cash flow reporting.

### Analytics Dashboard
Status: Planned

Behavioral analytics, session trends, and bankroll reporting.

### Data Export
Status: Planned

Export gambling activity and analytics for personal record keeping and external analysis.

### Behavioral Insights
Status: Planned

Data-driven recommendations and responsible gambling notifications.

### Mobile Application
Status: Future Consideration

Native mobile experience for trip and session tracking.