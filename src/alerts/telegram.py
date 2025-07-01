import logging
from telegram import Bot
from telegram.error import TelegramError
from typing import Optional, Union
from pathlib import Path

logger = logging.getLogger(__name__)

class TelegramAlert:
    def __init__(self, bot_token: str, chat_id: str):
        """
        Initialize Telegram alert system
        
        Args:
            bot_token (str): Telegram bot token obtained from BotFather
            chat_id (str): Telegram chat ID where messages will be sent
        """
        self.bot = Bot(token=bot_token)
        self.chat_id = chat_id

    async def send_message(self, message: str) -> bool:
        """
        Send a text message via Telegram
        
        Args:
            message (str): Message to send
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            await self.bot.send_message(
                chat_id=self.chat_id,
                text=message,
                parse_mode='HTML'
            )
            return True
        except TelegramError as e:
            logger.error(f"Failed to send Telegram message: {e}")
            return False

    async def send_file(self, file_path: Union[str, Path], caption: Optional[str] = None) -> bool:
        """
        Send a file via Telegram
        
        Args:
            file_path (Union[str, Path]): Path to the file to send
            caption (Optional[str]): Optional caption for the file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            with open(file_path, 'rb') as file:
                await self.bot.send_document(
                    chat_id=self.chat_id,
                    document=file,
                    caption=caption
                )
            return True
        except (TelegramError, FileNotFoundError) as e:
            logger.error(f"Failed to send file via Telegram: {e}")
            return False 