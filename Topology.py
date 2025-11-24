from mininet.topo import Topo

MAC_H2 = "d2:13:1c:1b:76:a0"
MAC_H6 = "b8:94:91:62:f1:65"


class Topology(Topo):
    def build(self):

        h1 = self.addHost('h1')
        h2 = self.addHost('h2', mac=MAC_H2)
        h3 = self.addHost('h3')
        h4 = self.addHost('h4')
        h5 = self.addHost('h5')
        h6 = self.addHost('h6', mac=MAC_H6)

        s1 = self.addSwitch('s1')
        s2 = self.addSwitch('s2')
        s3 = self.addSwitch('s3')
        s4 = self.addSwitch('s4')
        s5 = self.addSwitch('s5')
        s6 = self.addSwitch('s6')
        s7 = self.addSwitch('s7')

        self.addLink(h1, s4)
        self.addLink(h2, s4)
        self.addLink(h3, s5)
        self.addLink(h4, s6)
        self.addLink(h5, s7)
        self.addLink(h6, s7)

        self.addLink(s4, s2)
        self.addLink(s5, s2)
        self.addLink(s6, s3)
        self.addLink(s7, s3)
        self.addLink(s2, s1)
        self.addLink(s3, s1)


topos = {'Topology' : (lambda: Topology())}
