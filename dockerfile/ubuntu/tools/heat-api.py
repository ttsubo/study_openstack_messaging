import os
import time
import logging
import oslo.messaging
from oslo.config import cfg

CONF = cfg.CONF
CONF(default_config_files=['conf/heat.conf'])



oslo.messaging.set_transport_defaults('heat')
TRANSPORT = oslo.messaging.get_transport(CONF)
ENGINE_TOPIC = 'engine'


def get_rpc_client(**kwargs):
    target = oslo.messaging.Target(**kwargs)
    return oslo.messaging.RPCClient(TRANSPORT, target)


class EngineClient(object):

    BASE_RPC_API_VERSION = '1.0'

    def __init__(self):
        self._client = get_rpc_client(
            topic=ENGINE_TOPIC,
            version=self.BASE_RPC_API_VERSION)

    @staticmethod
    def make_msg(method, **kwargs):
        return method, kwargs

    def call(self, ctxt, msg, version=None):
        method, kwargs = msg
        if version is not None:
            client = self._client.prepare(version=version)
        else:
            client = self._client
        return client.call(ctxt, method, **kwargs)

    def health_check(self, ctxt, seqid, host, content):
        return self.call(ctxt, self.make_msg('health_check',
                                              seqid=seqid,
                                              host=host,
                                              req=content))


class StackController(object):

    def __init__(self):
        self.rpc_client = EngineClient()

    def health_check(self, seqid, host, content):
        try:
            (id, hostname, response) = self.rpc_client.health_check({}, seqid, host, content)
            logging.info("### Response: id=[{0}], host=[{1}], content=[{2}]"
                        .format(id, hostname, response))
        except oslo.messaging.MessagingTimeout as e:
            logging.error("### {0}".format(e))


if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(name)s:%(message)s',
                        level=logging.DEBUG)

    sequence_id = 0
    myhost = os.uname()[1]
    client = StackController()
    while True:
        sequence_id += 1
        client.health_check(sequence_id, myhost, "How are you?")
        time.sleep(10)
