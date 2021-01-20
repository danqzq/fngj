# Friday Night Game Jam Public API

### Proposal:

FNGJ api will be a public REST api to fetch data relevant to the series of gamejams and events. Listing past jams, games submitted and winners will be its core functionality. Ongoing jams/events can also be listed. The entries can be input from a separate, closed-source application.

### Routes:

#### Note that this is only a suggestion as of now and not final in any aspect.

##### /past-jams

This route will list all past jams as an array.
Response will be a json array, in the format [{}, {}, {}], where each {} is an event object.

##### /past-jams/:id

This route will list a particular jam object. The :id parameter is "year-week". For example, to get the data for the 42nd week of 2020, one can send a GET request to (url)/past-jams/2020-42.
Response will be a json object containing the event object.

##### /jam-games

This route will list all the games that have ever been submitted for FNGJ jams.
Returns a json array of game objects

##### /next-jam

This route will list details for the next jam.
Response will be a json object containing the event object.

##### /next-event

This route will list details for the next event, be it a jam or something else.
Response will be a json object containing the event object.

### Objects

The response returns json objects with particular formats. Not final.

##### Event Object

An event object contains information on a past, upcoming or ongoing event or jam. The format is as follows.

```js
{
  "id":"id of the jam or event"//Jam id's are "year-week", like 2020-42
  //event id's are "event-year#number", like event-2021#1 or event-2020#69
  "isJam": true //false if not a game jam
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

##### Game Object

An object containing information for a game submitted for the jam.

```js
{
  "id":"author-title in camelcase-date",//deathvenom-jumpForJoy-11/1/2021
  "title":"title of the game",
  "desc":"description of the game, as on its itch.io page",
  "link":"link to its itch.io game page",
  "ratingLink":"Link to its itch.io rating page",
  "author":"itch.io profile name of maker",
  "authorDiscord":"Discord usertag of author",//Username#1111
  "jam":"Jam for which game was submitted"//id of the jam
  "win":["","",""] //Array of categories in which the game won. Empty array if none.
}
```

##### Event Submission object

An object containing information for an event submission.

```js
{
  "id":"author-title in camelcase-date",//deathvenom-jumpForJoy-11/1/2021
  "title":"Title of the submission",
  "desc":"description of submission",
  "author":"author",
  "authorDiscord":"author's discord usertag",
  "event":"id for the event",
  "win":["","",""] //Array of categories in which the submission won. Empty array if none.
}
```
