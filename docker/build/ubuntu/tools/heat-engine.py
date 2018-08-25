import os
import logging
import eventlet
import oslo_messaging
from oslo_messaging.rpc import dispatcher
import datetime
from oslo_config import cfg
eventlet.monkey_patch()

CONF = cfg.CONF
CONF(default_config_files=['conf/heat.conf'])


oslo_messaging.set_transport_defaults('heat')
TRANSPORT = oslo_messaging.get_transport(CONF)
ENGINE_TOPIC = 'engine'


def get_rpc_server(target, endpoint):
    access_policy = dispatcher.DefaultRPCAccessPolicy
    return oslo_messaging.get_rpc_server(TRANSPORT, target, [endpoint],
                                         executor='eventlet',
                                         access_policy=access_policy)


class EngineService(object):

    RPC_API_VERSION = '1.35'

    def __init__(self, host, topic):
        self.host = host
        self.topic = topic

    def start(self):
        target = oslo_messaging.Target(
            version=self.RPC_API_VERSION, server=self.host,
            topic=self.topic)
        server = get_rpc_server(target, self)
        server.start()
        server.wait()

    def health_check(self, ctx, seqid, host, req):
        logging.info("### Request: id=[{0}], host=[{1}], content=[{2}]"
                    .format(seqid, host, req))
        myhost = os.uname()[1]
        response = "I'm fine!"
        return seqid, myhost, response




if __name__ == '__main__':
    logging.basicConfig(format='%(asctime)s:%(levelname)s:%(message)s',
                        level=logging.INFO)

    srv = EngineService("heat-engine", ENGINE_TOPIC)
    server = srv.start()
