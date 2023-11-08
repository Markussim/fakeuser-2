from dotenv import load_dotenv
import os
import random
import discord
from pprint import pprint
from openai import OpenAI

# Load the .env file
load_dotenv()

# Constants
openai_key = os.getenv("OPENAI_API_KEY")
discord_key = os.getenv("DISCORD_BOT_TOKEN")
BACKSTORY_FILE = "backstory.txt"
CHANCE_TO_RESPOND = 1  # 1 in 10 chance to respond
OPENAI_MODEL = "gpt-4-vision-preview"
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

            response = openaiClient.chat.completions.create(
                model=OPENAI_MODEL,
                messages=await self.construct_content_list(message),
                max_tokens=MAX_TOKENS,
            )

            print(response.choices[0].message.content)

            await message.channel.send(response.choices[0].message.content)

    async def construct_content_list(self, message):
        # First message is the backstory with the role 'system'
        content_list = [{"role": "system", "content": backstory}]

        # Temporarily store messages before reversing
        message_history = []

        # Fetch the last 5 messages and append them to message_history
        async for past_message in message.channel.history(limit=MESSAGE_HISTORY_LIMIT):
            if past_message.author == self.user:
                message_history.append(
                    {"role": "assistant", "content": past_message.content}
                )
            else:
                new_message = {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": f"Message from {past_message.author.name}: \n{past_message.content}",
                        },
                    ],
                }

                if past_message.attachments:
                    new_message["content"].append(
                        {
                            "type": "image_url",
                            "image_url": past_message.attachments[0].url,
                        }
                    )

                message_history.append(new_message)

        # Reverse the message_history to be in chronological order
        message_history.reverse()

        # Extend content_list with the reversed message_history, preserving the backstory as the first item
        content_list.extend(message_history)

        return content_list


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)

client.run(discord_key)
