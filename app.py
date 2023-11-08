from dotenv import load_dotenv
import os
import random
import discord
import json
from pprint import pprint
from openai import OpenAI

# Load the .env file
load_dotenv()

# Constants
openai_key = os.getenv("OPENAI_API_KEY")
discord_key = os.getenv("DISCORD_BOT_TOKEN")
BACKSTORY_FILE = "backstory.txt"
CHANCE_TO_RESPOND = 1  # 1 in 10 chance to respond
OPENAI_MODEL = "gpt-3.5-turbo-1106"
MAX_TOKENS = 300
MESSAGE_HISTORY_LIMIT = 5

# Initialize OpenAI
openaiClient = OpenAI(api_key=openai_key)

# Read backstory.txt
with open(BACKSTORY_FILE, "r") as file:
    backstory = file.read()


class MyClient(discord.Client):
    async def on_ready(self):
        print(f"Logged on as {self.user}!")

    async def on_message(self, message):
        if message.author == self.user:
            return

        random_number = random.randint(1, 10)

        # Check if bot is mentioned
        if self.user.mentioned_in(message) or random_number <= CHANCE_TO_RESPOND:
            # Send typing indicator
            await message.channel.typing()

            tools = [
                {
                    "type": "function",
                    "function": {
                        "name": "remeber",
                        "description": "Remember something for later.",
                        "parameters": {
                            "type": "object",
                            "properties": {
                                "input": {
                                    "type": "string",
                                    "description": "Use this to remember things beyond a few messages. Note that this replaces the file each time. Use this as often as you want, the size of this memory is practically infinite.",
                                }
                            },
                            "required": ["input"],
                        },
                    },
                }
            ]

            content_list = await self.construct_content_list(message)

            response = openaiClient.chat.completions.create(
                model=OPENAI_MODEL,
                messages=content_list,
                max_tokens=MAX_TOKENS,
                tools=tools,
                tool_choice="auto",
            )

            if response.choices[0].message.tool_calls:
                rawjson = response.choices[0].message.tool_calls[0].function.arguments

                # Parse json from string
                parsedjson = json.loads(rawjson)

                remember(parsedjson.get("input"))

            if response.choices[0].message.content == None:
                content_list = await self.construct_content_list(message)

                function_response = openaiClient.chat.completions.create(
                    model=OPENAI_MODEL,
                    messages=content_list,
                    max_tokens=MAX_TOKENS,
                    tools=tools,
                    tool_choice="none",
                )

                await message.channel.send(function_response.choices[0].message.content)
                return

            await message.channel.send(response.choices[0].message.content)

    async def construct_content_list(self, message):
        # Read memories.txt
        with open("memories.txt", "r") as file:
            memories = file.read()

        # First message is the backstory with the role 'system'
        content_list = [{"role": "system", "content": backstory + memories}]

        # Temporarily store messages before reversing
        message_history = []

        # Fetch the last 5 messages and append them to message_history
        async for past_message in message.channel.history(limit=MESSAGE_HISTORY_LIMIT):
            if past_message.author == self.user:
                message_history.append(
                    {"role": "assistant", "content": past_message.content}
                )
            else:
                user_content = (
                    f"Message from {past_message.author.name}: \n{past_message.content}"
                )
                if past_message.attachments:
                    user_content += "\n" + "\n".join(
                        [attachment.url for attachment in past_message.attachments]
                    )
                message_history.append({"role": "user", "content": user_content})

        # Reverse the message_history to be in chronological order
        message_history.reverse()

        # Extend content_list with the reversed message_history, preserving the backstory as the first item
        content_list.extend(message_history)

        return content_list


# Function that writes input to a specified file
def remember(input):
    # Write to "memories.txt"
    with open("memories.txt", "w") as file:
        file.write(input)


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)

client.run(discord_key)
