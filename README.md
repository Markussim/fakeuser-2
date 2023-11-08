# Discord Bot with OpenAI Integration

This Discord bot integrates OpenAI's GPT model for generating message responses and engages with users in conversation on Discord.

## Features

- Responds to user messages randomly based on a defined chance.
- Uses a predefined backstory to maintain context in conversations.
- Generates responses using OpenAI's Chat Completions feature with customizable model and token limit.
- Logs onto Discord and communicates with users in channels the bot has access to.
- Can look at images and respond to them.

## Setup

### Prerequisites

- Python 3.x
- Discord account and a Discord server where you have permissions to add bots.
- An OpenAI API key (you can get one from [OpenAI](https://platform.openai.com/))

### Installation

1. Clone the repository or download the bot program to your local machine.
2. Install the required Python libraries:

   ```
   pip install discord openai
   ```

3. Create and configure your `.env` file with your OpenAI API key and Discord bot token (This file must be in the same directory as your bot script):

   ```
   OPENAI_API_KEY='your_openai_api_key'
   DISCORD_BOT_TOKEN='your_discord_bot_token'
   ```

4. Add your backstory to the `backstory.txt` file.

5. Run the bot:

   ```
   python app.py
   ```

### Configuration

The following variables can be adjusted in the script:

- `CHANCE_TO_RESPOND`: Controls the likelihood of the bot responding, set as a "X in 10" chance.
- `OPENAI_MODEL`: Determines the OpenAI model to use for generating responses.
- `MAX_TOKENS`: Sets the maximum number of tokens (words/characters) in the generated responses.
- `MESSAGE_HISTORY_LIMIT`: Specifies how many previous messages to take into account for context.

## Usage

Once the bot is running and connected to your Discord server, it will respond to mentions or randomly based on the configured chance. The bot fetches the message history to maintain context while creating responses with the OpenAI model.

You can customize the behavior of the bot by modifying the constants at the beginning of the script.

## License

See [license](/LICENSE)

## Acknowledgments

- Thanks to OpenAI for providing the GPT model accessible via API.
- Special thanks to the Python and Discord.py communities for the helpful resources.
