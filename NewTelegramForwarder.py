import time
import asyncio
from telethon.sync import TelegramClient
from telethon.errors import SessionPasswordNeededError

class TelegramForwarder:
    def __init__(self, api_id, api_hash, phone_number):
        self.api_id = api_id
        self.api_hash = api_hash
        self.phone_number = phone_number
        self.client = TelegramClient('session_' + phone_number, api_id, api_hash)

    async def list_chats(self):
        await self.client.connect()

        # Ensure you're authorized
        if not await self.client.is_user_authorized():
            await self.client.send_code_request(self.phone_number)
            try:
                await self.client.sign_in(self.phone_number, input('Enter the code: '))
            except SessionPasswordNeededError:
                password = input('Two-step verification enabled. Please enter your password: ')
                await self.client.sign_in(password=password)

        # Get a list of all the dialogs (chats)
        dialogs = await self.client.get_dialogs()
        with open("AllChatsIDs.txt", "w", encoding="utf-8") as chats_file:
            # Print information about each chat
            for dialog in dialogs:
                chats_file.write(f"Chat ID: {dialog.id}, Title: {dialog.title}\n")

        print("List of groups saved to AllChatsIDs.txt successfully!")

    async def forward_messages_to_channel(self, source_chat_id, destination_channel_id, keywords):
        await self.client.connect()

        # Ensure you're authorized
        if not await self.client.is_user_authorized():
            await self.client.send_code_request(self.phone_number)
            try:
                await self.client.sign_in(self.phone_number, input('Enter the code: '))
            except SessionPasswordNeededError:
                password = input('Two-step verification enabled. Please enter your password: ')
                await self.client.sign_in(password=password)

        last_message_id = (await self.client.get_messages(source_chat_id, limit=1))[0].id

        while True:
            print("Checking for messages and forwarding them...")
            # Get new messages since the last checked message
            messages = await self.client.get_messages(source_chat_id, min_id=last_message_id, limit=None)

            for message in reversed(messages):
                # Check if the message text includes any of the keywords
                if keywords:
                    if message.text and any(keyword in message.text.lower() for keyword in keywords):
                        print(f"Message contains a keyword: {message.text}")

                        # Forward the message to the destination channel
                        await self.client.send_message(destination_channel_id, message.text)

                        print("Message forwarded")
                else:
                    # Forward the message to the destination channel
                    await self.client.send_message(destination_channel_id, message.text)

                    print("Message forwarded")

                # Update the last message ID
                last_message_id = max(last_message_id, message.id)

            # Add a delay before checking for new messages again
            await asyncio.sleep(5)  # Adjust the delay time as needed


async def main():
    # Hardcoded credentials
    api_id = '22877272'
    api_hash = '7495591e1824a05f02b57d92c2d15bdd'
    phone_number = '+2348024427735'

    forwarder = TelegramForwarder(api_id, api_hash, phone_number)
    
    print("Choose an option:")
    print("1. List Chats")
    print("2. Forward Messages")
    
    choice = input("Enter your choice: ")
    
    if choice == "1":
        await forwarder.list_chats()
    elif choice == "2":
        source_chat_id = int(input("Enter the source chat ID: "))
        destination_channel_id = int(input("Enter the destination chat ID: "))
        print("Enter keywords if you want to forward messages with specific keywords, or leave blank to forward every message!")
        keywords = input("Put keywords (comma separated if multiple, or leave blank): ").split(",")

        # Remove empty keyword if no keywords are provided
        keywords = [keyword.strip() for keyword in keywords if keyword.strip()]

        await forwarder.forward_messages_to_channel(source_chat_id, destination_channel_id, keywords)
    else:
        print("Invalid choice")

# Start the event loop and run the main function
if __name__ == "__main__":
    asyncio.run(main())
