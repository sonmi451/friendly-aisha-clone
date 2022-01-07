# Friendly Aisha Clone is a very useful discord bot

## Basic Setup

Create an `.env` file in the top level folder:

Set these env vars to be the token for server and the token for your bot/application to allow connection
```
DISCORD_SERVER=<server_id>
DISCORD_TOKEN=<token_id>
```

If you want to test/dev with a second (test) bot/application you can set the following optional env vars:
```
DEBUG_MODE=1
DISCORD_TOKEN_TEST=<alternate_token_id>
```

This 2 application setup allows to test new changes on a dev/test bot whilst the prod bot is still online.
However you can set the `DISCORD_TOKEN_TEST` token to be the same as your `DISCORD_TOKEN`.

## Running with Docker Compose

use `docker-compose up` to start the robot
use `docker-compose up -d` to start the robot in detached mode
use `docker-compose down` to stop the robot

## Wordlist

The `$wordle` function uses the `3of6` wordlist from: [12 Dicts](http://wordlist.aspell.net/12dicts/)