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

- **Start Hike Session**
  - method: `POST`
  - url: `<BASE_URL>/map/`
  - Response: 201 Created:

```
      {
        "id": 3,
        "created_at": "2022-08-15T02:12:48.444555Z",
        "updated_at": "2022-08-15T02:12:48.444605Z",
        "distance_list": 1,
        "start_location": {
          "latitude": 39.099105,
          "longitude": -79.660706
        },
        "end_location": null,
        "distance_traveled": null,
        "avg_mph": null,
        "travel_time": null,
        "elevation_gain": null
      }
```

<br />