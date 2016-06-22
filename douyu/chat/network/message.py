
from utils import deserialize, serialize

class Message:

    body = None
    _serialized_size = 0

    def __init__(self, body):
        self.body = body

    def to_text(self):
        return serialize(self.body)

    def size(self):
        return self._serialized_size

    def attr(self, attr_name):
        if self.body is None:
            return None
        try:
            result = self.body[attr_name]
            return result
        except KeyError as e:
            return None

    @staticmethod
    def sniff(buff):

        # print '[Message] Sniffing message'

        if buff is None or len(buff) <= 0:
            # print '[Message] Empty message buffer'
            return None

        msg_bodies = buff.split('\0')
        if len(msg_bodies) <= 1:
            # print '[Message] No messages detected'
            return None

        # print '[Message] Messages detected in buffer: Count %d' % len(msg_bodies)

        return Message.from_raw(msg_bodies[0])

    @staticmethod
    def from_raw(raw):
        result = Message(deserialize(raw))
        result._serialized_size = len(raw)
        return result
