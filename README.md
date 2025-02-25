# Discord Social Graph Creation

The purpose of this set of tools is to extract your discord friends, mutuals, and servers from discord, and then use it to create a graph database like that of Obsidian.md's graph view.

## Quick Start

Right now the best way to just run the python script raw. I used to have a poetry setup, but it was too much of a hassle to maintain.

make sure to set your environment variables in a `.env` file in the root directory of the project. The following variables are required:

```bash
export DISCORD_EMAIL="your_email"
export DISCORD_PASSWORD="your_password"
```

```bash
python discord_scraper.py
```

### Docker Implementation

Not yet done, might not be a good idea given that I would have to embed a whole browser in the docker container.
