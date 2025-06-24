from typing import List, Tuple
from .telegram import TelegramAlert
from ..config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, TELEGRAM_ALERT_ENABLED

async def send_alerts(processed_files: List[Tuple[str, str]]) -> None:
    """Send processed files via Telegram if enabled."""
    if processed_files and TELEGRAM_ALERT_ENABLED and TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID:
        telegram = TelegramAlert(TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID)
        
        for file_name, search_param in processed_files:
            caption = (f"Product data for search: {search_param} from "
                      f"{file_name.replace('.csv', '').title()}" if search_param
                      else f"Product data from {file_name.replace('.csv', '').title()}")
            
            success = await telegram.send_file(
                f"src/data/{file_name}",
                caption=caption
            )
            
            if success:
                print(f"File {file_name} sent successfully via Telegram")
            else:
                print(f"Failed to send file {file_name} via Telegram")
    elif processed_files:
        print("Telegram alerts are disabled or not configured") 