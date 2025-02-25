# Discord Social Graph Creation

The purpose of this set of tools is to extract your discord friends, mutuals, and servers from discord, and then use it to create a graph database like that of Obsidian.md's graph view.

## Preview

[](images/preview.png)

## Quick Start

Right now the best way to just run the python script raw. I used to have a poetry setup, but it was too much of a hassle to maintain.

make sure to set your environment variables in a `.env` file in the root directory of the project. The following variables are required:

### Step 1: The Scraper

To set up the scraper, you need to set up the following environment variables:

```bash
export DISCORD_EMAIL="your_email"
export DISCORD_PASSWORD="your_password"
```

And then run the scraper:

```bash
python src/discord_scraper.py
```

When this is done you will have a new file, friends.json, in the root directory of the project.

### Step 2: Merge with other users if needed

Assuming you have both your `friends.json` and another user's `friends2.json`, you can merge them together with the following command:

```bash
python src/json_merger.py friends.json friends2.json output.json
```

### Step 3: Generate Obsidian Files and Graph

Assuming you have a `friends.json` file in your project root:

```bash
python src/json_to_obsidian.py
```
