from mininet.topo import Topo
from mininet.cli import CLI
from mininet.net import Mininet
from mininet.link import TCLink
from mininet.util import irange,dumpNodeConnections
from mininet.log import setLogLevel
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch

class Test_Topo(Topo):

    "Topologie maillee de l'etape 3 (figure 1 de l'enonce), pilotee par Floodlight"
    # 'protocols' fixe la version d'OpenFlow annoncee par chaque commutateur a
    # la connexion. Floodlight (etape 3) attend OpenFlow13 par defaut ; passer
    # 'OpenFlow10' resterait possible mais n'est pas necessaire ici puisque
    # aucun controleur de reference Mininet n'est utilise dans cette etape.
    def __init__(self, protocols='OpenFlow13', **opts):
        "Create the Test_topo mesh topology"
        Topo.__init__(self, **opts)

        # Hotes : h1 et h2 sont rattaches a s1, h3 et h4 a s8 (adresses IP/MAC
        # fixes, comme dans Tree_topo.py, pour rester previsibles).
        h1 = self.addHost('h1', cls=Host, ip='10.0.0.1', mac='00:00:00:00:00:01', defaultRoute=None)
        h2 = self.addHost('h2', cls=Host, ip='10.0.0.2', mac='00:00:00:00:00:02', defaultRoute=None)
        h3 = self.addHost('h3', cls=Host, ip='10.0.0.3', mac='00:00:00:00:00:03', defaultRoute=None)
        h4 = self.addHost('h4', cls=Host, ip='10.0.0.4', mac='00:00:00:00:00:04', defaultRoute=None)

        # Commutateurs : s1 (cote h1/h2) et s8 (cote h3/h4) sont relies par
        # TROIS chemins paralleles (s2 seul ; s3-s4-s5 ; s6-s7), ce qui rend le
        # reseau maille (2 boucles independantes) plutot qu'un simple arbre.
        s1 = self.addSwitch('s1', cls=OVSKernelSwitch, dpid='0000000000000001', protocols=protocols)
        s2 = self.addSwitch('s2', cls=OVSKernelSwitch, dpid='0000000000000002', protocols=protocols)
        s3 = self.addSwitch('s3', cls=OVSKernelSwitch, dpid='0000000000000003', protocols=protocols)
        s4 = self.addSwitch('s4', cls=OVSKernelSwitch, dpid='0000000000000004', protocols=protocols)
        s5 = self.addSwitch('s5', cls=OVSKernelSwitch, dpid='0000000000000005', protocols=protocols)
        s6 = self.addSwitch('s6', cls=OVSKernelSwitch, dpid='0000000000000006', protocols=protocols)
        s7 = self.addSwitch('s7', cls=OVSKernelSwitch, dpid='0000000000000007', protocols=protocols)
        s8 = self.addSwitch('s8', cls=OVSKernelSwitch, dpid='0000000000000008', protocols=protocols)

        # Liens d'acces hote-commutateur (bw en Mbps, delay = latence de
        # propagation), valeurs prises telles quelles sur la figure 1.
        self.addLink(h1, s1, bw=10, delay='5ms')
        self.addLink(h2, s1, bw=10, delay='4ms')
        self.addLink(h3, s8, bw=10, delay='6ms')
        self.addLink(h4, s8, bw=10, delay='3ms')

        # Chemin A : s1-s2-s8 (2 sauts, 12+4 = 16 ms)
        self.addLink(s1, s2, bw=10, delay='12ms')
        self.addLink(s2, s8, bw=10, delay='4ms')

        # Chemin B : s1-s3-s4-s5-s8 (4 sauts, 3+6+3+2 = 14 ms -- le plus long
        # en nombre de sauts mais le plus court en latence cumulee)
        self.addLink(s1, s3, bw=10, delay='3ms')
        self.addLink(s3, s4, bw=10, delay='6ms')
        self.addLink(s4, s5, bw=10, delay='3ms')
        self.addLink(s5, s8, bw=10, delay='2ms')

        # Chemin C : s1-s6-s7-s8 (3 sauts, 5+10+1 = 16 ms)
        self.addLink(s1, s6, bw=10, delay='5ms')
        self.addLink(s6, s7, bw=10, delay='10ms')
        self.addLink(s7, s8, bw=10, delay='1ms')

topos = { 'test': Test_Topo }
