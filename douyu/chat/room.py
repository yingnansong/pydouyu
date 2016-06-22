
import network.client
import thread
import time
import logging

RAW_BUFF_SIZE = 4096
KEEP_ALIVE_INTERVAL_SECONDS = 45

# Keep-Alive thread func
def keep_alive(client, delay):
    while True:
        current_ts = int(time.time())
        client.send({
            'type': 'keeplive',
            'tick': current_ts
        })
        time.sleep(delay)


class ChatRoom:

    client = None
    room_id = None
    channel_id = -9999  # Convention

    callbacks = {}

    def __init__(self, room_id):

        self.room_id = room_id

    def on(self, event_name, callback):
        callback_list = None
        try:
            callback_list = self.callbacks[event_name]
        except KeyError as e:
            callback_list = []
            self.callbacks[event_name] = callback_list
        callback_list.append(callback)

    def trigger_callbacks(self, event_name, message):
        callback_list = None

        try:
            callback_list = self.callbacks[event_name]
        except KeyError as e:
            logging.info('Message of type "%s" is not handled' % event_name)
            return

        if callback_list is None or len(callback_list) <= 0:
            return

        for callback in callback_list:
            callback(message)

    # Start running
    def knock(self):

        self.client = network.client.Client()

        # Send AUTH request
        self.client.send({'type': 'loginreq','roomid': self.room_id})

        # Start a thread to send KEEPALIVE messages separately
        thread.start_new_thread(keep_alive, (self.client, KEEP_ALIVE_INTERVAL_SECONDS))

        # Handle messages
        for message in self.client.receive():

            if not message:
                continue

            # print json.dumps(message.body)
            msg_type = message.attr('type')

            # Send JOIN_GROUP request
            if msg_type == 'loginres':
                self.client.send({'type': 'joingroup', 'rid': self.room_id, 'gid': self.channel_id})

            self.trigger_callbacks(msg_type, message)