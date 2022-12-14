# T.H.A.T. Guide api endpoints

Base url for all endpoints:

- `<BASE_URL>`: `https://thatguide.herokuapp.com`

## Home

- method: `GET`
- url: `<BASE_URL>`
- response: an object that contains a random Meme:

```
{
  "team": "Purple Rain",
  "description": "We are going to crush this project!",
  "meme_image": "https://i.redd.it/hsx65uf65yd91.jpg"
}
```

<br />

## Start Hike App

- **Start Hike Session - Select Destination Option**
  - method: `POST`
  - url: `<BASE_URL>/map/`
  - Authorization data: IF YOU ARE A LOGGED IN USER you need to set authorization header with the token as the value
    - Example: `Authorization: Token b4eecdcb2731a4a1383ad2ae15a2eb2fd6a1ac3d`
  - data required to start: The "start_location", "end_location", and "current_elevation"
  - data calculated from backend once checkpoint is hit: "distance_travled" 
  - data calculated from backend once hike is finished:  "elevation_gain" and "elevation_loss"
  - Response: 201 Created:
```
    {
      "id": 101,
      "hike_user": "Ryan",
      "created_at": "2022-08-28T22:51:01.035359Z",
      "updated_at": "2022-08-28T22:51:01.035398Z",
      "distance": 279,
      "start_location": {
        "latitude": 40,
        "longitude": -71
      },
      "end_location": {
        "latitude": 43.988847,
        "longitude": -71.907141
      },
      "distance_traveled": null,
      "avg_mph": null,
      "travel_time": null,
      "elevation_gain": 0,
      "elevation_loss": 0,
      "current_elevation": 150
    }
```

- **Start Hike Session - Set Distance Option**
 - method: `POST`
  - url: `<BASE_URL>/map/`
  - Authorization data: IF YOU ARE A LOGGED IN USER you need to set authorization header with the token as the value
    - Example: `Authorization: Token b4eecdcb2731a4a1383ad2ae15a2eb2fd6a1ac3d`
  - data required to start: The "start_location" and "current_elevation"
  - data calculated from backend once checkpoint is hit: "distance_travled" 
  - data calculated from backend once hike is finished:  "elevation_gain" and "elevation_loss"
```
    {
      "id": 101,
      "hike_user": "Ryan",
      "created_at": "2022-08-28T22:51:01.035359Z",
      "updated_at": "2022-08-28T22:51:01.035398Z",
      "distance": 279,
      "start_location": {
        "latitude": 40,
        "longitude": -71
      },
      "end_location": null,
      "distance_traveled": null,
      "avg_mph": null,
      "travel_time": null,
      "elevation_gain": 0,
      "elevation_loss": 0,
      "current_elevation": 150
    }
```

- **Start Hike Session - Freeform hike Option**
 - method: `POST`
  - url: `<BASE_URL>/map/`
  - Authorization data: IF YOU ARE A LOGGED IN USER you need to set authorization header with the token as the value
    - Example: `Authorization: Token b4eecdcb2731a4a1383ad2ae15a2eb2fd6a1ac3d`
  - data required to start: The "start_location" and "current_elevation"
  - data calculated from backend once checkpoint is hit: "distance_travled" 
  - data calculated from backend once hike is finished:  "elevation_gain" and "elevation_loss"
```
    {
      "id": 101,
      "hike_user": "Ryan",
      "created_at": "2022-08-28T22:51:01.035359Z",
      "updated_at": "2022-08-28T22:51:01.035398Z",
      "distance": 279,
      "start_location": {
        "latitude": 40,
        "longitude": -71
      },
      "end_location": null,
      "distance_traveled": null,
      "avg_mph": null,
      "travel_time": null,
      "elevation_gain": 0,
      "elevation_loss": 0,
      "current_elevation": 150
    }
```

<br />

- **View Hike Session**
  - method: `GET`
  - url: `<BASE_URL>/map/<int:pk/`
  - Response: 200 ok: an array of the objects for the particular hike session:

```
    {
      "id": 1,
      "created_at": "2022-08-16T19:01:31.865507Z",
      "updated_at": "2022-08-16T19:16:29.902823Z",
      "distance": 1,
      "start_location": {
        "latitude": 39.099105,
        "longitude": -79.660706
      },
      "end_location": {
        "latitude": 39.099105,
        "longitude": -40.660706
      },
      "distance_traveled": null,
      "avg_mph": null,
      "travel_time": 8,
      "elevation_gain": 0,
      "elevation_loss": 0,
      "current_elevation": null,
      "hike_user": null
    }
```

<br />

- **Update/Edit Hike Session**
  - method: `PATCH`
  - url: `<BASE_URL>/map/<int:pk/`
  - Response: 200 ok: an array of the objects for the particular hike session:

```
    {
      "id": 1,
      "created_at": "2022-08-16T19:01:31.865507Z",
      "updated_at": "2022-08-16T19:16:29.902823Z",
      "distance": 1,
      "start_location": {
        "latitude": 39.099105,
        "longitude": -79.660706
      },
      "end_location": {
        "latitude": 39.099105,
        "longitude": -40.660706
      },
      "distance_traveled": null,
      "avg_mph": null,
      "travel_time": 8,
      "elevation_gain": 0,
      "elevation_loss": 0,
      "current_elevation": null,
      "hike_user": null
    }
```

<br />

- **Post Checkpoint Within Session**
  - method: `POST`
  - url: `<BASE_URL>/map/<int:pk/checkpoint/`
  - Response: 201 created

```
        {
          "id": 5,
          "created_at": "2022-08-16T21:43:41.548609Z",
          "updated_at": "2022-08-16T21:43:41.548632Z",
          "location": {
            "latitude": 52.099105,
            "longitude": -64.660706
          },
          "elevation": 123,
          "time_logged": "2022-08-22T19:59:12.654784Z" ,
          "hike_session": 4
        }
```

<br />

- **See Checkpoint Within Session**
  - method: `GET`
  - url: `<BASE_URL>/map/<int:pk/checkpoint_pk/`
  - Response: 200 ok: an array of the objects for the particular checkpoint:

```
      {
        "id": 5,
        "created_at": "2022-08-16T21:43:41.548609Z",
        "updated_at": "2022-08-16T21:43:41.548632Z",
        "location": {
          "latitude": 52.099105,
          "longitude": -64.660706
        },
        "elevation": 150,
        "hike_session": 4
      }
```

## User Authentication

- **Create user**

  - method: `POST`
  - url: `<BASE_URL>/auth/users/`
  - data: json object `{ "username": "yourusername", "password": "yourpassword" }`
  - response: will be a user object
    `{ "email": "", "username": "test", "id": 1 }`
    <br />

- **Login**

  - method: `POST`
  - url: `<BASE_URL>/auth/token/login/`
  - data: json object `{ "username": "yourusername", "password": "yourpassword" }`
  - response: will be a token: `{ "auth_token": "b4eecdcb2731a4a1383ad2ae15a2eb2fd6a1ac3d" }`
    <br />

- **Logout**

  - method: `POST`
  - url: `<BASE_URL>/auth/token/logout/`
  - data: you need to set authorization header with the token as the value, make sure you have a space after "Token":
    - Example: `Authorization: Token b4eecdcb2731a4a1383ad2ae15a2eb2fd6a1ac3d`
    - `<YOUR TOKEN>` is a long string you get back from the login endpoint
    - `Authorization: Token <YOUR TOKEN>`
  - response: will be empty (no data)

    <br />

  ## View a List of Users

- method: `GET`
- url: `<BASE_URL>/users/`
- response: an array of user objects:

```
{
        "id": 1,
        "password": "admin",
        "last_login": null,
        "is_superuser": false,
        "first_name": "",
        "last_name": "",
        "is_staff": false,
        "is_active": true,
        "date_joined": "2022-08-16T13:24:30.217898Z",
        "experience_list": "beginner",
        "pace_list": "leisure",
        "username": "firstuser",
        "email": null,
        "phone": null,
        "groups": [],
        "user_permissions": []
},
{
        "id": 2,
        "password": "admin",
        "last_login": null,
        "is_superuser": false,
        "first_name": "",
        "last_name": "",
        "is_staff": false,
        "is_active": true,
        "date_joined": "2022-08-16T13:25:17.861669Z",
        "experience_list": "beginner",
        "pace_list": "leisure",
        "username": "seconduser",
        "email": null,
        "phone": null,
        "groups": [],
        "user_permissions": []
},

```

  <br />

## Edit Your User

- method: `PATCH`
- url: `<BASE_URL>/users/me`
- data: you need to set authorization header with the token as the value
- Example: `Authorization: Token b4eecdcb2731a4a1383ad2ae15a2eb2fd6a1ac3d`
- response: an array of users updated objects:

```
{
	      "id": 5,
	      "password": "pbkdf2_sha256$320000$Ccg0yWqd8qmsoCfdtHauCO$83o6Nvu6ZZ8mo3VVX0Ny9K9blxjg2/rS/C6cc8lETRA=",
	      "last_login": "2022-08-16T14:58:56.641874Z",
	      "is_superuser": false,
	      "first_name": "",
	      "last_name": "",
	      "is_staff": false,
	      "is_active": true,
	      "date_joined": "2022-08-16T14:58:41.661105Z",
	      "experience_list": "beginner",
        "pace_list": "powerwalk",
	      "username": "fifthuser",
	      "email": "",
	      "phone": null,
	      "groups": [],
	      "user_permissions": []
}

```

 <br />


## Display a User's Hiking Sessions

- method: `GET`
- url: `<BASE_URL>/users/me/map`
- data: you need to set authorization header with the token as the value
- Example: `Authorization: Token b4eecdcb2731a4a1383ad2ae15a2eb2fd6a1ac3d`
- response: an array of users objects:

```
[
	{
		"id": 17,
		"created_at": "2022-08-23T14:19:38.753504Z",
		"updated_at": "2022-08-23T14:19:38.753569Z",
		"distance": 1,
		"start_location": {
			"latitude": 8,
			"longitude": 13
		},
		"end_location": {
			"latitude": 80,
			"longitude": 10
		},
		"distance_traveled": null,
		"avg_mph": null,
		"travel_time": null,
		"elevation_gain": 0,
    "elevation_loss": 0,
		"current_elevation": "40.00",
		"hike_user": 5
	},
	{
		"id": 18,
		"created_at": "2022-08-23T14:31:13.556576Z",
		"updated_at": "2022-08-23T14:31:13.556594Z",
		"distance": 1,
		"start_location": {
			"latitude": 8,
			"longitude": 13
		},
		"end_location": {
			"latitude": 80,
			"longitude": 10
		},
		"distance_traveled": null,
		"avg_mph": null,
		"travel_time": null,
		"elevation_gain": 0,
    "elevation_loss": 0,
		"current_elevation": "40.00",
		"hike_user": 5
	}
]

```

 <br />