from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.packet.ethernet import ethernet
from pox.lib.addresses import EthAddr

log = core.getLogger()

H2_MAC = EthAddr("d3:13:1c:1b:76:a0")
H6_MAC = EthAddr("b9:94:91:62:f1:65")

class LearningSwitch(object):

    def __init__(self, connection):
        self.connection = connection
        self.mac_to_port = {}
        connection.addListeners(self)
        log.info("LearningSwitch activated for switch %s" % connection)

    def _handle_PacketIn(self, event):
        packet = event.parsed
        in_port = event.port

        if not packet:
            return

        src = packet.src
        dst = packet.dst

        self.mac_to_port[src] = in_port

        if src == H2_MAC and dst == H6_MAC:
            log.info("FIREWALL DROP: H2 → H6 (%s → %s)" % (src, dst))

            fm = of.ofp_flow_mod()
            fm.match = of.ofp_match.from_packet(packet, in_port)

            self.connection.send(fm)
            return

        # this will forward packets based on known MACs
        if dst in self.mac_to_port:
            out_port = self.mac_to_port[dst]

            fm = of.ofp_flow_mod()
            fm.match = of.ofp_match.from_packet(packet, in_port)
            fm.actions.append(of.ofp_action_output(port=out_port))
            fm.idle_timeout = 30
            self.connection.send(fm)

            po = of.ofp_packet_out(data=event.ofp)
            po.actions.append(of.ofp_action_output(port=out_port))
            po.in_port = in_port
            self.connection.send(po)

        else:
            po = of.ofp_packet_out(data=event.ofp)
            po.actions.append(of.ofp_action_output(port=of.OFPP_FLOOD))
            po.in_port = in_port
            self.connection.send(po)

def launch():
    
    def start_switch(event):
        LearningSwitch(event.connection)

    core.openflow.addListenerByName("ConnectionUp", start_switch)
    log.info("Custom L2 learning switch with firewall loaded.")
