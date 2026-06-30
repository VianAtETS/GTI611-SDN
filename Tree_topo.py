from mininet.topo import Topo
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch

class Tree_Topo(Topo):

    "Tree Topology"
    # 'protocols' fixe la version OpenFlow appliquee a chaque commutateur.
    # Defaut 'OpenFlow13' (Floodlight, etape 3). Passer 'OpenFlow10' pour que
    # les commutateurs se connectent au controleur de reference par defaut
    # (ovs-testcontroller, OF 1.0) a l'etape 2 :
    #   mn --custom Tree_topo.py --topo tree,protocols=OpenFlow10 --link tc
    def __init__(self, protocols='OpenFlow13', **opts):
        "Create tree Topology"
        Topo.__init__(self, **opts)

        # Section 1: commentez cette section
        h1 = self.addHost('h1', cls=Host, ip='10.0.0.1',mac='10:00:00:00:00:01', defaultRoute=None)
        h2 = self.addHost('h2', cls=Host, ip='10.0.0.2', mac='10:00:00:00:00:02', defaultRoute=None)
        h3 = self.addHost('h3', cls=Host, ip='10.0.0.3', mac='10:00:00:00:00:03', defaultRoute=None)
        h4 = self.addHost('h4', cls=Host, ip='10.0.0.4', mac='10:00:00:00:00:04', defaultRoute=None)
        h5 = self.addHost('h5', cls=Host, ip='10.0.0.5', mac='10:00:00:00:00:05', defaultRoute=None)
        h6 = self.addHost('h6', cls=Host, ip='10.0.0.6', mac='10:00:00:00:00:06', defaultRoute=None)

        # Section 2: commentez cette section
        s1 = self.addSwitch('s1', cls=OVSKernelSwitch, dpid='0000000000000001',protocols=protocols)
        s2 = self.addSwitch('s2', cls=OVSKernelSwitch, dpid='0000000000000002',protocols=protocols)
        s3 = self.addSwitch('s3', cls=OVSKernelSwitch, dpid='0000000000000003',protocols=protocols)
        s4 = self.addSwitch('s4', cls=OVSKernelSwitch, dpid='0000000000000004',protocols=protocols)
        s5 = self.addSwitch('s5', cls=OVSKernelSwitch, dpid='0000000000000005',protocols=protocols)
        s6 = self.addSwitch('s6', cls=OVSKernelSwitch, dpid='0000000000000006',protocols=protocols)
        s7 = self.addSwitch('s7', cls=OVSKernelSwitch, dpid='0000000000000007',protocols=protocols)

        # Section 3: commentez cette section
        self.addLink(s1, s2, port1=1, bw=15, delay='2ms')
        self.addLink(s1, s3, port1=2, bw=4, delay='10ms')
        self.addLink(s2, s4, port1=2, bw=7, delay='5ms')
        self.addLink(s2, s5, port1=3, bw=7, delay='6ms')
        self.addLink(s3, s6, port1=2, bw=15, delay='4ms')
        self.addLink(s3, s7, port1=3, bw=4, delay='15ms')
        self.addLink(h1, s4, port2=2, bw=2, delay='0ms')
        self.addLink(h2, s4, port2=3, bw=2, delay='0ms')
        self.addLink(h3, s5, port2=2, bw=2, delay='0ms')
        self.addLink(h4, s6, port2=2, bw=2, delay='0ms')
        self.addLink(h5, s7, port2=2, bw=2, delay='0ms')
        self.addLink(h6, s7, port2=3, bw=7, delay='0ms')

topos = { 'tree': Tree_Topo }
