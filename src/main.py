import asyncio
import os
from modes import automated, interactive
from alerts import telegram_handler

async def main():
    """Main entry point for the tech product tracker."""
    # Check if running in automated mode (e.g., via CRON job)
    is_automated = os.environ.get('AUTOMATED_MODE', '').lower() == 'true'
    
    if is_automated:
        print("Running in automated mode...")
        processed_files = await automated.run()
    else:
        print("Running in interactive mode...")
        processed_files = await interactive.run()
    
    # Send alerts regardless of mode
    await telegram_handler.send_alerts(processed_files)

if __name__ == "__main__":
    asyncio.run(main())
