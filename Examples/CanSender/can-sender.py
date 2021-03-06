import json
import time

import can
import os

# Function Definitions

def create_can_messages(raw_messages):
    """ Creates a list of CAN message objects

     Parameters:
     raw_messages (list): A list of can message objects as defined in the json schema

     Returns:
     can_messages (list): A list of python-can can.Message objects
     """
    can_messages = []
    for raw_message in raw_messages:
        can_message = can.Message(
            arbitration_id=raw_message["msgId"],
            is_extended_id=raw_message["isExtendedId"],
            data=raw_message["data"]
        )
        can_messages.append(can_message)
    return can_messages

if __name__ == "__main__":
    file_path = os.getcwd() + '/senderInfo.json'
    with open(file_path, mode='r') as json_config:
        can_config = json.load(json_config)
        can_bus = can.Bus(bustype=can_config["canInfo"]["busType"],
                          channel=can_config["canInfo"]["serialPort"],
                          bitrate=can_config["canInfo"]["bitrate"])
        can_messages_raw = [
            message for message in can_config["canInfo"]["messages"]]
        message_frequency = can_config["canInfo"]["messageFrequency"]
        can_messages = create_can_messages(can_messages_raw)
        while True:
            time.sleep(1.0 / message_frequency)
            for can_message in can_messages:
                try:
                    can_bus.send(can_message)
                    print(f"Message sent on {can_bus.channel_info}")
                except can.CanError:
                    print("Error, message not sent")
