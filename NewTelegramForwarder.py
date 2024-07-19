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
        await self.client.connect()

        # Ensure you're authorized
        if not await self.client.is_user_authorized():
            await self.client.send_code_request(self.phone_number)
            await self.client.sign_in(self.phone_number, input('Enter the code: '))

        while True:
            for group in self.groups:
                source_chat_id = group["source_id"]
                destination_channel_id = group["dest_id"]
                keywords = group["criteria"]

                last_message_id = (await self.client.get_messages(source_chat_id, limit=1))[0].id

                # Get new messages since the last checked message
                messages = await self.client.get_messages(source_chat_id, min_id=last_message_id, limit=None)

                for message in reversed(messages):
                    # Check if the message text includes any of the keywords
                    if message.text and any(keyword.lower() in message.text.lower() for keyword in keywords):
                        print(f"Message contains a keyword: {message.text}")

                        # Forward the message to the destination channel
                        await self.client.send_message(destination_channel_id, message.text)

                        print("Message forwarded")

                    # Update the last message ID
                    last_message_id = max(last_message_id, message.id)

            # Add a delay before checking for new messages again
            await asyncio.sleep(5)  # Adjust the delay time as needed


# Function to read credentials from file
def read_credentials():
    try:
        with open("credentials.txt", "r") as file:
            lines = file.readlines()
            api_id = lines[0].strip()
            api_hash = lines[1].strip()
            phone_number = lines[2].strip()
            return api_id, api_hash, phone_number
    except FileNotFoundError:
        print("Credentials file not found.")
        return None, None, None

# Function to write credentials to file
def write_credentials(api_id, api_hash, phone_number):
    with open("credentials.txt", "w") as file:
        file.write(api_id + "\n")
        file.write(api_hash + "\n")
        file.write(phone_number + "\n")

async def main():
    # Attempt to read credentials from file
    api_id, api_hash, phone_number = read_credentials()

    # If credentials not found in file, prompt the user to input them
    if api_id is None or api_hash is None or phone_number is None:
        api_id = input("Enter your API ID: ")
        api_hash = input("Enter your API Hash: ")
        phone_number = input("Enter your phone number: ")
        # Write credentials to file for future use
        write_credentials(api_id, api_hash, phone_number)

    forwarder = TelegramForwarder(api_id, api_hash, phone_number)
    await forwarder.forward_messages()

# Start the event loop and run the main function
if __name__ == "__main__":
    asyncio.run(main())
