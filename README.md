# FairyJokeAPI

FairyJoke is a rhythm games database project with a public API.

The long term goal is to serve as a repository for static data such as lists of
songs, difficulties, a list of different rhythm games and their accompanying
release dates and platforms.

Think https://remywiki.com/ but more developer-friendly to be incorporated and
used into other projects without scrapping web pages.

## Cool features

- Easy to use [API](https://fairyjoke.tina.moe/docs).

- Search

- Song jackets

## The stack

FairyJoke is built with Python using FastAPI and SQLAlchemy. The frontend uses
Jinja2 templates and Materialize CSS.

## How is the data sourced

The plan is to allow sourcing the data either from game dumps or trustable
sources (such as a wiki or official songs list). It will mostly depend on what's
available for each game, and what's easier to import.

For some data such as a list of games and their release dates, I'm envisionning
a folder with text files that users could contribute to easily on GitHub, see
the
[`import/games` folder in the 1.0 branch](https://github.com/Tina-otoge/FairyJokeAPI/tree/1.0/imports/games)
for an example.

## Contributing

Please do. The project is nicely splitted into smaller modules to make it easier
to add support for more games. I will answer opened issues and help you with PRs
as much as I can.
