import asyncio
from fetchers.microcenter import fetch_microcenter_html
from parsers.microcenter import parse_microcenter_html
from storage.csv_writer import write_to_csv
from alerts.telegram import TelegramAlert
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, TELEGRAM_ALERT_ENABLED

async def main():
    search_param = input("Enter the search parameter: ")

    beautiful_soup_object = fetch_microcenter_html(search_param)
    data = parse_microcenter_html(beautiful_soup_object)
    
    file_name = "microcenter.csv"
    write_to_csv(data, file_name)
    print(f"Data written to src/data/{file_name}")

    # Send file via Telegram if enabled
    if TELEGRAM_ALERT_ENABLED and TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        telegram = TelegramAlert(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
        success = await telegram.send_file(
            f"src/data/{file_name}",
            caption=f"Product data for search: {search_param}"
        )
        if success:
            print("File sent successfully via Telegram")
        else:
            print("Failed to send file via Telegram")
    else:
        print("Telegram alerts are disabled or not configured")

if __name__ == "__main__":
    asyncio.run(main())
