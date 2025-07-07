# Affiliaters Bot

This is a Telegram and Facebook bot that scrapes Flipkart product deals, converts them to affiliate links, and posts them to Telegram channels and Facebook pages automatically.

## Features

- Scrapes random Flipkart URLs for product deals
- Converts product links to affiliate links using the Affiliaters API
- Posts product deals with images to Telegram channels
- Posts product deals with images to Facebook pages
- Runs continuously with configurable interval

## Installation

1. Clone the repository.

2. Install dependencies:

```
pip install -r requirements.txt
```

## Configuration

Set the following environment variables (can be set in your shell or in a `.env` file):

- `BOT_TOKEN`: Telegram bot token
- `CHANNEL_ID`: Telegram channel IDs (list)
- `PAGE_ACCESS_TOKEN`: Facebook page access token
- `PAGE_ID`: Facebook page ID
- `API_KEY`: Affiliaters API key

## Usage

Run the bot using the start script or directly with Python:

```bash
./start.sh
```

or

```bash
python main.py
```

The bot will start scraping Flipkart URLs, convert links, and post deals automatically.

### Dashboard

The bot also runs a Flask web server accessible at `http://localhost:5050/dashboard` which shows the current status and last posted product.

### Docker Deployment

You can run the bot inside a Docker container:

1. Build the Docker image:

```bash
docker build -t affiliaters-bot .
```

2. Run the Docker container (make sure to set environment variables):

```bash
docker run -d -p 5050:5050 --env BOT_TOKEN=your_bot_token --env CHANNEL_ID='["channel_id1","channel_id2"]' --env PAGE_ACCESS_TOKEN=your_page_access_token --env PAGE_ID=your_page_id --env API_KEY=your_api_key affiliaters-bot
```

This will start the bot and expose the dashboard on port 5050.

## License

This project is created by @priyanshusingh999 and @r_ajput999.
