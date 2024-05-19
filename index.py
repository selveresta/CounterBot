import logging
import json
import os
import asyncio
from datetime import datetime, timedelta
from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# File to store message counts
FILE_NAME = "db.json"

# Load message counts from file
if os.path.exists(FILE_NAME):
    with open(FILE_NAME, "r") as file:
        message_counts = json.load(file)
else:
    message_counts = {}


def save_counts():
    """Save the current message counts to the file."""
    with open(FILE_NAME, "w") as file:
        json.dump(message_counts, file)


# Initialize bot and dispatcher
API_TOKEN = "6524725754:AAFZJSmH2NvWA5jqRhxMup2B0y3_mDEAtjs"
bot = Bot(token=API_TOKEN)
dp = Dispatcher()


def calcualteMessages(fromTime, toTime, arr):
    count = 0
    date_format = "%Y-%m-%d %H:%M:%S"
    for i in arr:
        time = datetime.strptime(i, date_format)
        if time > fromTime and time < toTime:
            count += 1

    return count


@dp.message(Command("counts"))
async def send_counts(message: types.Message):
    """Send the current message counts to the chat."""

    now = datetime.now()
    lastDay = now - timedelta(days=1)
    last7Day = now - timedelta(days=7)
    last30Days = now - timedelta(days=30)
    resultStr = f"\t\tStatistic for Users\n\n"
    try:
        for user_id, data in message_counts.items():
            messagesOneDay = calcualteMessages(lastDay, now, data["messages"])
            messages7Day = calcualteMessages(last7Day, now, data["messages"])
            messages30Day = calcualteMessages(last30Days, now, data["messages"])

            resultStr += f"{str(data['name'])}\n"
            resultStr += f"Messages for last day: {messagesOneDay}\n"
            resultStr += f"Messages for last 7 day: {messages7Day}\n"
            resultStr += f"Messages for last 30 day: {messages30Day}\n"

            resultStr += f"\n\n"

        await message.answer(resultStr)
    except:
        print(resultStr)


@dp.message()
async def count_message(message: types.Message):
    """Count messages from each user."""

    user_id = message.from_user.id
    user_name = message.from_user.full_name
    sID = str(user_id)
    date_format = "%Y-%m-%d %H:%M:%S"
    if sID in message_counts:
        date = str(datetime.now().strftime(date_format))
        message_counts[sID]["messages"].append(date)

        save_counts()

        logger.info(f"Save message from {user_name} ({user_id}) at {date}")


async def main():
    """Start the bot."""
    await dp.start_polling(bot, skip_updates=True)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())
