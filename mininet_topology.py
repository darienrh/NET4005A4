from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import RemoteController, OVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info

H2_MAC = "d3:13:1c:1b:76:a0"
H6_MAC = "b9:94:91:62:f1:65"

class Assign5Topo(Topo):
    def build(self):

        # making the hostss for the topology
        h1 = self.addHost("h1")
        h2 = self.addHost("h2", mac=H2_MAC)   # untrusted
        h3 = self.addHost("h3")
        h4 = self.addHost("h4")
        h5 = self.addHost("h5")
        h6 = self.addHost("h6", mac=H6_MAC)   # protected

        # these are the switches
        s1 = self.addSwitch("s1")
        s2 = self.addSwitch("s2")

        self.addLink(h1, s1)
        self.addLink(h2, s1)
        self.addLink(h3, s1)

        self.addLink(s1, s2)

        self.addLink(h4, s2)
        self.addLink(h5, s2)
        self.addLink(h6, s2)

def run():
    setLogLevel("info")

    topo = Assign5Topo()

    net = Mininet(
        topo=topo,
        controller=lambda name: RemoteController(name, ip="localhost", port=6633),
        switch=OVSSwitch,
        autoSetMacs=False
    )

    net.start()
    info("*** Network started.***\n")
    CLI(net)
    net.stop()

if __name__ == "__main__":
    run()
