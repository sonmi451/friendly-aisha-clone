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

- Use `docker compose up` to start the robot
- Use `docker compose up -d` to start the robot in detached mode
- Use `docker compose down` to stop the robot

## Deploying

1. Clone directory
1. Create `.env` file in directory root
1. Run `docker compose up --build -d`

## Populating the movie list data base

From terminal run
`nano ./resources/movie_watchlist.txt` and populate the list

Run `python ./movie_data_txt_to_json.py`, which converts the `resources/movie_watchlist.txt` to `resources/movie_watchlist.json`

In discord run
`$importmovies` which imports from `resources/movie_watchlist.json` 

### Logs
use `docker-compose logs robot` to print the logs from the docker container

## Wordlist

The `$wordle` function uses the `3of6` wordlist from: [12 Dicts](http://wordlist.aspell.net/12dicts/)
