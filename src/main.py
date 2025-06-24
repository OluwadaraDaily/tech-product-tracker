import asyncio
import os
from processing.microcenter import process_microcenter
from alerts.telegram import TelegramAlert
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, TELEGRAM_ALERT_ENABLED
from utils import select_stores


DEFAULT_STORES = ["microcenter"]
DOES_STORE_HAVE_SEARCH_PARAMS = {
    "microcenter": True
}
DEFAULT_SEARCH_PARAMS = {
    "microcenter": [
    "gpu",
    "cpu",
    "ram",
    "ssd",
    "macbook",
    "monitor"
    ]
}

async def process_store(store: str, search_param: str) -> str:
    """Process a single store and return the CSV filename."""
    if store == "microcenter":
        return await process_microcenter(search_param)
    # Add more store handlers here as they are implemented
    else:
        print(f"Handler for {store} not implemented yet")
        return None

async def run_automated_mode():
    """Run the script in automated mode with default parameters."""
    processed_files = []
    
    # Process each store with each search parameter
    for store in DEFAULT_STORES:
        if DOES_STORE_HAVE_SEARCH_PARAMS[store]:
            for search_param in DEFAULT_SEARCH_PARAMS[store]:
                print(f"\nProcessing {store.title()} for {search_param}...")
                file_name = await process_store(store, search_param)
            if file_name:
                processed_files.append((file_name, search_param))
                print(f"Data written to src/data/{file_name}")

    return processed_files

async def run_interactive_mode():
    """Run the script in interactive mode with user input."""
    processed_files = []
    
    # First, let user select stores
    selected_stores = select_stores()
    print(f"\nSelected stores: {', '.join(store.title() for store in selected_stores)}")
    
    # Get search parameter
    search_param = input("\nEnter the search parameter: ")
    
    # Process each selected store
    for store in selected_stores:
        print(f"\nProcessing {store.title()}...")
        file_name = await process_store(store, search_param)
        if file_name:
            processed_files.append((file_name, search_param))
            print(f"Data written to src/data/{file_name}")

    return processed_files

async def send_telegram_alerts(processed_files):
    """Send processed files via Telegram if enabled."""
    if processed_files and TELEGRAM_ALERT_ENABLED and TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        telegram = TelegramAlert(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
        
        for file_name, search_param in processed_files:
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

async def main():
    # Check if running in automated mode (e.g., via CRON job)
    is_automated = os.environ.get('AUTOMATED_MODE', '').lower() == 'true'
    
    if is_automated:
        print("Running in automated mode...")
        processed_files = await run_automated_mode()
    else:
        print("Running in interactive mode...")
        processed_files = await run_interactive_mode()
    
    # Send alerts regardless of mode
    await send_telegram_alerts(processed_files)

if __name__ == "__main__":
    asyncio.run(main())
