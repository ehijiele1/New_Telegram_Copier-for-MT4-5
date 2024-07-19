import os
import asyncio
from telethon.sync import TelegramClient

class TelegramForwarder:
    def __init__(self, api_id, api_hash, phone_number):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone_number = phone_number
        self.client = TelegramClient('session_' + phone_number, api_id, api_hash)
        self.groups = [
            {"source_id": -1001444264665, "dest_id": -4262620945, "criteria": ["buy", "sell"]},
            {"source_id": -1001251900924, "dest_id": -4228780769, "criteria": ["buy", "sell"]},
            {"source_id": -1001761740065, "dest_id": -4246706330, "criteria": ["buy", "sell"]},
            {"source_id": -1001350478111, "dest_id": -4265309118, "criteria": ["buy", "sell"]},
            {"source_id": -1001780474473, "dest_id": -4104558322, "criteria": ["buy now", "sell now"]},
            {"source_id": -1001240888164, "dest_id": -4242163102, "criteria": ["buy", "sell"]},
            {"source_id": -1001276577932, "dest_id": -4260221938, "criteria": ["sold", "bought"]},
            {"source_id": -1001276577932, "dest_id": -4228838041, "criteria": ["buy", "sell"]},
            {"source_id": -1001466079489, "dest_id": -1002159497316, "criteria": ["buy", "sell"]}
        ]

    async def forward_messages(self):
        await self
