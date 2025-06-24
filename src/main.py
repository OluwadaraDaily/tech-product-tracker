import asyncio
from processing.microcenter import process_microcenter
from alerts.telegram import TelegramAlert
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, TELEGRAM_ALERT_ENABLED
from utils import select_stores


async def process_store(store: str, search_param: str) -> str:
    """Process a single store and return the CSV filename."""
    if store == "microcenter":
        return await process_microcenter(search_param)
    # Add more store handlers here as they are implemented
    else:
        print(f"Handler for {store} not implemented yet")
        return None

async def main():
    # First, let user select stores
    selected_stores = select_stores()
    print(f"\nSelected stores: {', '.join(store.title() for store in selected_stores)}")
    
    # Get search parameter
    search_param = input("\nEnter the search parameter: ")
    
    # Process each selected store
    processed_files = []
    for store in selected_stores:
        print(f"\nProcessing {store.title()}...")
        file_name = await process_store(store, search_param)
        if file_name:
            processed_files.append(file_name)
            print(f"Data written to src/data/{file_name}")

    # Send files via Telegram if enabled
    if processed_files and TELEGRAM_ALERT_ENABLED and TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        telegram = TelegramAlert(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
        
        for file_name in processed_files:
            success = await telegram.send_file(
                f"src/data/{file_name}",
                caption=f"Product data for search: {search_param} from {file_name.replace('.csv', '').title()}"
            )
            
            if success:
                print(f"File {file_name} sent successfully via Telegram")
            else:
                print(f"Failed to send file {file_name} via Telegram")
    elif processed_files:
        print("Telegram alerts are disabled or not configured")

if __name__ == "__main__":
    asyncio.run(main())
