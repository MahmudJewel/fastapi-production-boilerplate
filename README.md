# FastAPI Production Kit
A production based FastAPI template
<p>
    <a href="https://github.com/MahmudJewel/fastapi-production-boilerplate/fork">
        <img src="https://img.shields.io/github/forks/MahmudJewel/fastapi-production-boilerplate.svg?style=social&label=Fork" />
    </a>
    <a href="https://github.com/MahmudJewel/fastapi-production-boilerplate/fork">
        <img src="https://img.shields.io/github/stars/MahmudJewel/fastapi-production-boilerplate.svg?style=social&label=Stars" />
    </a>
    <a href="https://github.com/MahmudJewel/fastapi-production-boilerplate/fork">
        <img src="https://img.shields.io/nuget/dt/Azylee.Core.svg" />
    </a>
</p>
<p>
    If the repo is helpful for you, please give a star and fork it.
</p>
<a href="https://github.com/MahmudJewel/fastapi-production-boilerplate/fork">
    Click here to download/fork the repository
</a>

## Features:
* FastAPI project structure tree
* user module
    - id, first name, last name, **email** as username, **password**, role, is_active created_at, updated_at 
* admin dashboard => sqladmin
* authentication => JWT
* db migration => alembic
* middleware
* three types of server
    - production, development, test
* UUID as primary key
* Applied RBAC(Role Based Access Control)
* Applied google auth(OAuth2)

## Structured Tree
```sh
├── alembic     # Manages database migrations
├── alembic.ini
├── app
│   ├── api
│   │   ├── endpoints   # Contains modules for each feature (user, product, payments).
│   │   │   ├── __init__.py
│   │   │   └── user
│   │   │       ├── auth.py
│   │   │       ├── functions.py
│   │   │       ├── __init__.py
│   │   │       └── user.py
│   │   ├── __init__.py
│   │   └── routers     # Contains FastAPI routers, where each router corresponds to a feature.
│   │       ├── main_router.py
│   │       ├── __init__.py
│   │       └── user.py
│   ├── core    # Contains core functionality like database management, dependencies, etc. 
│   │   ├── database.py
│   │   ├── dependencies.py
│   │   ├── __init__.py
│   │   └── settings.py
│   ├── __init__.py
│   ├── main.py     # Initializes the FastAPI app and brings together various components.
│   ├── models      # Contains modules defining database models for users, products, payments, etc.
│   │   ├── admin.py
│   │   ├── common.py
│   │   ├── __init__.py
│   │   └── user.py
│   ├── schemas    # Pydantic model for data validation
│   │   ├── __init__.py
│   │   └── user.py
│   └── utils       # Can include utility functions that are used across different features.
├── requirements.txt # Lists project dependencies.
```
**app/api/endpoints/**: Contains modules for each feature (user, product, payments).

**app/api/routers/**: Contains FastAPI routers, where each router corresponds to a feature.

**app/models/**: Contains modules defining database models for users, products, payments, etc.

**app/core/**: Contains core functionality like database management, dependencies, etc.

**app/utils/**: Can include utility functions that are used across different features.

**app/main.py**: Initializes the FastAPI app and brings together various components.

**tests/**: Houses your test cases.

**alembic/**: Manages database migrations.

**docs/**: Holds documentation files.

**scripts/**: Contains utility scripts.

**requirements.txt**: Lists project dependencies.


# Setup
1. The first thing to do is to clone the repository:
```sh
$ https://github.com/MahmudJewel/fastapi-production-boilerplate
```

2. Create a virtual environment to install dependencies in and activate it:
```sh
$ cd fastapi-production-boilerplate
$ python -m venv venv
$ source venv/bin/activate
```
3. Then install the dependencies:
```sh
# for fixed version
(venv)$ pip install -r requirements.txt

# or for updated version
(venv)$ pip install -r dev.txt
```
Note the `(venv)` in front of the prompt. This indicates that this terminal
session operates in a virtual environment set up by `virtualenv2`.
4. Now rename **.env.example** to **.env** and give the information on the .env file.

5. Migrate the database:
```sh
(venv)$ alembic upgrade head
(venv)$ uvicorn app.main:app --reload
```
6. Then Run the project
```sh
# start the server
(venv)$ uvicorn app.main:app --reload # using directly uvicorn ==> old one => before version 0.100.0
or
(venv)$ fastapi dev app/main.py # using fastapi CLI ==> after version 0.100.0
```

## User module's API
| SRL | METHOD | ROUTE | FUNCTIONALITY | Fields | Access | 
| ------- | ------- | ----- | ------------- | ------------- |------------- |
| *1* | *POST* | ```/login``` | _Login user_| _**email**, **password**_| _All User_|
| *2* | *POST* | ```/refresh/?refresh_token=``` | _Refresh access token_| _None_| _All User_|
| *3* | *POST* | ```/users/``` | _Create new user_|_**email**, **password**, first name, last name_| _Anyone_|
| *4* | *GET* | ```/users/``` | _Get all users list_|_email, password, first name, last name, role, is_active, created_at, updated_at, id_|_Admin_|
| *5* | *GET* | ```/users/me/``` | _Get current user details_|_email, password, first name, last name, role, is_active, created_at, updated_at, id_|_Any User_|
| *6* | *GET* | ```/users/{user_id}``` | _Get indivisual users details_|_email, password, first name, last name, role, is_active, created_at, updated_at, id_|_Any User_|
| *7* | *PATCH* | ```/users/{user_id}``` | _Update the user partially_|_email, password, is_active, role_|_Admin_|
| *8* | *DELETE* | ```/users/{user_id}``` | _Delete the user_|_None_|_Admin_|
| *9* | *GET* | ```/``` | _Home page_|_None_|_Anyone_|
| *10* | *GET* | ```/admin``` | _Admin Dashboard_|_None_|_Anyone_|

## OAuth2 - Social Auth
| SRL | METHOD | ROUTE | FUNCTIONALITY | Fields | Access | 
| ------- | ------- | ----- | ------------- | ------------- |------------- |
| *1* | *GET* | ```/social/google/login``` | _Login by google_| _None_| _Anyone_|
| *2* | *GET* | ```/social/auth/google/callback``` | _Callback for google_| _None_| _Anyone_|

## Integration Tests

### 1. Install test dependencies

```sh
(venv)$ pip install -r requirements.txt
(venv)$ pip install -r dev.txt
```

### 2. Run tests

```sh
# run all integration tests
(venv)$ python scripts/run_integration_tests.py -q

# run single integration file
(venv)$ python scripts/run_integration_tests.py test_users -q

# run single test
(venv)$ python scripts/run_integration_tests.py "test_users::test_create_user_creates_db_object" -q
```

### 3. Database mode

```sh
# same db (default), objects remain in DB
(venv)$ python scripts/run_integration_tests.py --db-url sqlite:///./integration_test.db -q

# separate db per run
(venv)$ python scripts/run_integration_tests.py --db-url sqlite:///./integration_test.db --separate-db -q
```

Notes:
- Tests override app DB dependency with test DB session.
- Tests verify object created in relational DB.
- Objects created by tests are kept in DB (no auto cleanup).
- In separate DB mode, sqlite file name gets unique suffix each run.

# Tools
### Back-end
#### Language:
	Python

#### Frameworks:
	FastAPI
    pydantic
	
#### Other libraries / tools:
	SQLAlchemy
    starlette
    uvicorn
    python-jose
    alembic

# **warning!!!**
* Do not use the same secret key that I provided.
* Always use new secret key for each project 
* The command will generate new secret key.
```sh
openssl rand -hex 32
```

For practicing level project, Please follow this repo https://github.com/MahmudJewel/fastapi-starter-boilerplate

### Happy Coding
