## DOTS-CONNECT-DETA

A basic websocket backend to allow users to join arbitrary rooms, send messages in that room, get messages from that room.
It currently acts as a naive middle-man to broadcast messages between people in the same room.
Nothing is saves in the backend for now.

## Prerequisites

1. Need [python >= 3.7.6](https://www.python.org/downloads/release/python-376/)
2. (Optional) Recommeded to use [Anaconda](https://www.anaconda.com/) as a primary python distribution.
3. Need [Redis](https://redis.io/) for channel backend.

## Getting Started

1. Clone this repo
2. Install the requirements

```console
python -m pip install -r requirements.txt
```

3. Start Redis Server in a new console window. Make sure that the redis-server uses localhost:6379

```console
redis-server
```

4. Run server

```console
python manage.py runserver
```

## Client Usage

1. Open Websocket connection

```js
const chatSocket = new WebSocket(
  "ws://" + window.location.host + "/ws/chat/" + roomName + "/"
);
```

2. Listen for websocket for any data

```js
chatSocket.onmessage = function (e) {
  const data = JSON.parse(e.data);
  console.log(data);
  // data will be a Object of the form {message: "...xyz..."}
};
```

3. Better to handle disconnect

```js
chatSocket.onclose = function (e) {
  console.error("Chat socket closed unexpectedly");
};
```

4. Send a message to the room

```js
chatSocket.send(
  JSON.stringify({
    message: "...your payload here...",
  })
);
```

## Copyrights & License

© [Sinha, Ujjawal](https://github.com/Sinha-Ujjawal)

Licensed under [MIT](./LICENSE)
