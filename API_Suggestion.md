# Friday Night Game Jam Public API

### Proposal:

FNGJ api will be a public REST api to fetch data relevant to the series of gamejams and events. Listing past jams, games submitted and winners will be its core functionality. Ongoing jams/events can also be listed. The entries can be input from a separate, closed-source application.

### Routes:

#### Note that this is only a suggestion as of now and not final in any aspect.

### /events

This route lists all events held between the given dates. Query should be in json format.

```js
{
  "type": "jam",
  "date": {
    "start": "all",//"all" to list all jams before end date
    "end": "2021-01-20T00:00:00.00Z"//"all" to list all jams after start date
  },
  "search": "<someParam or empty>"//Search some words in event title or description
}
```

### /events/current

Lists ongoing/planned future events/jams.

```js
{
  "type":"jam", //List only given type of event
  "time":"ongoing" || "upcoming" //List only ongoing or upcoming events. Leave blank to list both.
}
```

##### /submissions

This route will list all the submissions according to given params (REQUIRED).
Query parameters are:

```js
{
  "header":"author" || "eventID" || "genre",
  "value": "Deathvenom"||"2020-42"||"scifi"
}
```

### Objects

The response returns json objects with particular formats. Not final.

##### Event Object

An event object contains information on a past, upcoming or ongoing event or jam. The format is as follows.

```js
{
  "id":"id of the jam or event"//Jam id's are "year-week", like 2020-42
  //event id's are "event-year#number", like event-2021#1 or event-2020#69
  "type": "The type of event, leave blank if a jam", //"hackathon", "coding challenge"
  "startTime": "The starting date and time", //This is generated in javascript using JSON.stringify(Date object)
  //See https://stackoverflow.com/a/44074625/12872811 to parse it in python
  "endTime": "The ending date and time",
  "theme":"A short theme name",//Only applicable if a jam
  "desc":"A comparatively longer string describing the theme, if a jam, or describing the event.",
  "link":"Jam link, or event link if hosted on some platform",
  "submissions":[{},{},{}]//All submissions for the jam/event. Game object if a jam, submission object if a normal event submission.
}
```

### Submission Object

Contains information about a submission for an event, jam or not.

```js
{
  "id":"author-title in camelcase-date",//deathvenom-jumpForJoy-11/1/2021
  "title":"Title of the submission",
  "desc":"description of submission",
  "image":"url to thumbnail image." //https://img.itch.zone/aW1nLzM4NzYzNzIucG5n/315x250%23c/fiFiEa.png
  "author": {
    "name": "author",
    "email": "author@author.com", // optional
    "discord":"author's discord usertag" // optional
  },
  "event":"id for the event",
  "link": {
    "submission": "link to the submission",
    "rating": "link to the rating of the submissions" // optional
  },
  "win":["","",""], //Array of categories in which the submission won. Empty array if none.
  "tags":["genre","special keyword","anything else"]
}
```
