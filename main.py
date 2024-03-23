import os
import json
from dotenv import load_dotenv
from azure.eventhub import EventHubProducerClient, EventData
import asyncio

# Load environment variables from .env file
load_dotenv()

# Event Hub connection string
connection_str = os.getenv("EVENT_HUB_CONNECTION_STRING")
print(connection_str)

# Event Hub name
eventhub_name = os.getenv("EVENT_HUB_NAME")
print(eventhub_name)

#exit()

# Open the file
with open('local/id.txt', 'r') as file:
    # Read each line
    ids = [line.strip() for line in file]

# Now 'ids' is a list containing all IDs
print(ids)

exit()

async def send_message_to_eventhub(id):
    # Create a producer client to send messages to the event hub
    producer = EventHubProducerClient.from_connection_string(conn_str=connection_str, eventhub_name=eventhub_name)

    async with producer:
        # Create a batch
        event_data_batch = await producer.create_batch()

        # Create the message
        data = {
            "Id": "",
            "Key": id,
        }

        # Add the message to the batch
        event_data_batch.add(EventData(json.dumps(data)))

        # Send the batch of messages to the event hub
        await producer.send_batch(event_data_batch)

# Call the function for each ID
loop = asyncio.get_event_loop()
for id in ids:
    loop.run_until_complete(send_message_to_eventhub(id))
loop.close()