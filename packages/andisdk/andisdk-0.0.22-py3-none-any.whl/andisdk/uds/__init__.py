import clr
clr.AddReference('PrimaITestCaseLibrary')
from PrimaITestCaseLibrary import HSFZCtrlWordMapping
import queue
from udsoncan.connections import BaseConnection as _BaseConnection
from udsoncan.client import Client as _Client
from .exceptions import TimeoutException

class MessageConnection(_BaseConnection):

    def __init__(self, message):
        _BaseConnection.__init__(self, message.name)
        self.rxqueue = queue.Queue()
        self.opened = False
        self.message = message

    def open(self):
        self.message.on_message_received += self._on_message_received
        self.message.connect()
        self.opened = True
        return self

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        self.close()

    def is_open(self):
        return self.opened

    def close(self):
        self.message.on_message_received -= self._on_message_received
        self.message.disconnect()
        self.opened = False

    def specific_wait_frame(self, timeout=2):
        if not self.opened:
            raise RuntimeError("Connection is not open")

        timedout = False
        frame = None
        try:
            frame = self.rxqueue.get(block=True, timeout=timeout)

        except queue.Empty:
            timedout = True

        if timedout:
            raise TimeoutException("Did not receive frame in time (timeout=%s sec)" % timeout)

        return frame

    def empty_rxqueue(self):
        while not self.rxqueue.empty():
            self.rxqueue.get()

class HsfzConnection(MessageConnection):
    """
    Sends and receives data through a HSFZ message.
    """
    def _on_message_received(self, msg):
        if msg.ctr_word == HSFZCtrlWordMapping.CTRLWORD_ACK:
            return
        if msg.diag:
            self.rxqueue.put(bytes(msg.diag.data))

    def specific_send(self, payload):
        self.message.ctr_word = HSFZCtrlWordMapping.CTRLWORD_REQUEST_RESPONSE
        self.message.diag.data = tuple(payload)
        self.message.send()

class DoIpConnection(MessageConnection):
    """
    Sends and receives data through a DoIP message.
    """
    def open(self):
        super().open()
        self.__activate_routing()
        return self

    def __create_routing_activation_message(message):
        # 2 bytes source address, 1 byte activation type (0 for default), 4 bytes reserved (0x00000000)
        return tuple(message.payload)[0:2] +(0x00, 0x00, 0x00, 0x00, 0x00)

    def __create_diag_payload(message, payload):
        return  tuple(message.payload)[0:4] + tuple(payload)

    ROUTING_ACTIVATION_PAYLOAD_TYPE = 0x0005
    DIAG_PAYLOAD_TYPE = 0x8001

    def __activate_routing(self):
        # after establishing connection, send a routing activation request
        message = self.message
        message.payload_type = DoIpConnection.ROUTING_ACTIVATION_PAYLOAD_TYPE
        old_payload = message.payload
        message.payload = DoIpConnection.__create_routing_activation_message(message)
        message.send()
        message.payload = old_payload

    def _on_message_received(self, msg):
        # if message is diag payload save it
        if msg.payload_type == DoIpConnection.DIAG_PAYLOAD_TYPE:
            self.rxqueue.put(bytes(msg.payload))

    def specific_send(self, payload):
        self.message.payload_type = DoIpConnection.DIAG_PAYLOAD_TYPE
        self.message.payload = DoIpConnection.__create_diag_payload(self.message, payload)
        self.message.send()


class UdsClient(_Client):

    """
    Returns UDS client with specific target address target_addr.

    :param target_addr: Target address (e.g. ZGW=0x10)
    :type channel: int

    :return: The UDS client
    :rtype: :ref:`UdsClient`
    """
    def __call__(self, target_addr) -> _Client:
        if self.conn is HsfzConnection:
            self.conn.message.diag.target_address = target_addr
        if self.conn is DoIpConnection:
            self.conn.message.target_address = target_addr
        return self
