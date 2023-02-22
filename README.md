# Hack the North 2023 Backend Challenge

# Database Design
The data is separated into the following tables in an SQLITE database. 

Table: USERS  
Primary Key: USERID
|Column|Type|Setting|
|---|---|---|
|USERID|INTEGER|Primary Key|
|NAME|TEXT||
|COMPANY|TEXT||
|EMAIL|TEXT||
|PHONE|TEXT||

Table: USERSKILLS  
Primary Key: (USERID, SKILL)
|Column|Type|Setting|
|---|---|---|
|USERID|INTEGER|References Users|
|SKILL|TEXT|References Skills|
|RATING|INTEGER||


Table: SKILLS  
Primary Key: SKILL
|Column|Type|Settings|
|---|---|---|
|SKILL|TEXT|Primary Key|
|FREQUENCY|INTEGER||

Table: USEREVENTS  
Primary Key: (USERID, EVENT)
|Column|Type|Settings|
|---|---|---|
|USERID|INTEGER|References Users|
|EVENT|TEXT||

# API
`GET /users/?<query>`
Returns all stored users

Queries
|Query|Description|
|---|---|
|`name`|Return only users that have a name equal to `name` (optional)|
|`company`|Return only users that have a company equal to `company` (optional)|
|`email`|Return only users that have an email equal to `email` (optional)|
|`phone`|Return only users that have an phone equal to `phone` (optional)|

Example Response
```
[
  {
      "id": "2579234888",
      "company": "Google",
      "email": "cam@google.net",
      "name": "Cam",
      "phone": "+1-023-214-9233",
      "skills": [
          {
              "rating": 1,
              "skill": "OpenCV"
          },
      ]
  },
  {
      "id": "996806564",
      "company": "Meta",
      "email": "mitchell@example.org",
      "name": "Mitchell",
      "phone": "(289)599-0428",
      "skills": [
          {
              "rating": 4,
              "skill": "Elixir"
          },
          {
              "rating": 2,
              "skill": "Fortran"
          },
      ]
  },
]
```

`GET /users/<userid>`
Get information about a particular user

Example Response
```
{
    "id": "123456789",
    "company": "Apple",
    "email": "phil@apple.org",
    "name": "phil",
    "phone": "+1-031-528-3741",
    "skills": [
        {
            "rating": 1,
            "skill": "OpenCV"
        },
    ]
},
```

`PUT /users/<userid>`
Update information about a particular user

Example Request
```
{
  "company": "Oranges",
  "skills": [
    {
      "skill": "OpenCV",
      "rating": 5
    }
  ]
}
```

Example Response
```
{
    "id": "123456789",
    "company": "Oranges",
    "email": "phil@apple.org",
    "name": "phil",
    "phone": "+1-031-528-3741",
    "skills": [
        {
            "rating": 5,
            "skill": "OpenCV"
        },
    ]
},
```

`GET /skills/?<queries>`
Get information about skills that match a query 

Queries
|Query|Description|
|---|---|
|`min_frequency`|Return only skills that have a frequency no less than `min_frequency` (optional)|
|`max_frequency`|Return only skills that have a frequency no higher than `max_frequency` (optional)|

Example Response
```
[
  {
      "rating": 13,
      "skill": "Svelte"
  },
  {
      "rating": 16,
      "skill": "AutoHotkey"
  },
]
```

`GET /userevents/?<queries>`
Get information about userevents that match a query 

Queries
|Query|Description|
|---|---|
|`userid`|Return only skills for the user with `userid` (required)|

Example Response
```
[
    "ice hockey",
    "ice skating",
    "ice skiing" 
]
```

`POST /userevents/`
Create an event for a user

Example Request
```
{
  "userid": "123456789",
  "event": "ice sledding"
}
```

Example Response
```
[
    "ice hockey",
    "ice skating",
    "ice skiing",
    "ice sledding",
]
```


# Usage
Update `JSON_DATA_FILE` in `config.py` to match the given data file name.  
Update `DATABASE_FILE` in `config.py` to the SQLITE database name.  
Run `python fill.py` to fill the database with the initial data.  
Run `python rest.py` to start the REST API server.  
The `Users` class in `data.py` is used to allow for future changes of the user fields and query parsing.