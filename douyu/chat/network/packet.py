
from struct import pack, unpack

MESSAGE_TYPE_FROM_CLIENT = 689
MESSAGE_TYPE_FROM_SERVER = 690


class Packet:

    body = None

    def __init__(self, body):
        self.body = body

    def to_raw(self):
        raw_length = len(self.body) + 9
        msg_type = MESSAGE_TYPE_FROM_CLIENT
        return pack('<llhbb%ds' % (len(self.body) + 1), raw_length, raw_length, msg_type, 0, 0, self.body + '\0')

    # Returns frame size for this packet
    def size(self):
        if self.body is None:
            return 0
        return len(self.body) + 12

    @staticmethod
    def sniff(buff):

        # Packet Part 1: Bytes[0-3] Packet length in little endian
        # Packet Part 2: Bytes[4-7] Same packet length in little endian
        # Packet Part 3: Bytes[8-9] Message type, 689(FromClient), 690(FromServer)
        # Packet Part 4: Bytes[10] Encryption Field - Reserved
        # Packet Part 5: Bytes[11] Reserved
        # Packet Part 6: Bytes[12-] Messege body in UTF8

        # print '[Packet] Sniffing packet'

        buff_len = len(buff)
        # print '[Packet] Packet buffer length %d' % buff_len

        if buff_len < 12:
            return None

        packet_length_1, packet_length_2, msg_type, encryption, reserved, body = unpack('<llhbb%ds' % (buff_len - 12), buff)

        # print '[Packet] Packet length 1: %d' % packet_length_1
        # print '[Packet] Packet length 2: %d' % packet_length_2
        # print '[Packet] Packet msg_type: %s' % msg_type
        # print '[Packet] Packet encryption: %d' % encryption
        # print '[Packet] Packet reserved: %d' % reserved
        # print '[Packet] Packet body: %s' % body

        if packet_length_1 != packet_length_2:
            print '[Packet] Unmatched packet length fields!'
            raise Exception()

        needed_body_length = packet_length_1 - 8
        current_body_length = len(body)

        if current_body_length < needed_body_length:
            # print '[Packet] Insufficient packet body data'
            return None

        if current_body_length > needed_body_length:
            body = body[0:needed_body_length]
            # print '[Packet] Packet body trimmed: %s' % body

        # print '[Packet] Packet detected: %s' % body
        return Packet(body)