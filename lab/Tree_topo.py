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
    # 'protocols' fixe la version d'OpenFlow annoncee par chaque commutateur a
    # la connexion. Par defaut 'OpenFlow13' (requis par Floodlight, etape 3).
    # Passer 'OpenFlow10' pour se connecter au controleur de reference de
    # Mininet (qui ne parle que OF 1.0), etape 2 :
    #   mn --custom Tree_topo.py --topo tree,protocols=OpenFlow10 --link tc
    def __init__(self, protocols='OpenFlow13', **opts):
        "Create tree Topology"
        Topo.__init__(self, **opts)

        # Section 1 : les 6 hotes (h1 a h6). Contrairement au comportement par
        # defaut de Mininet (adressage IP/MAC auto-attribue), chaque hote
        # recoit ici une IP et une adresse MAC fixes (10.0.0.X et
        # 10:00:00:00:00:0X) afin que les adresses restent previsibles d'une
        # execution a l'autre. defaultRoute=None desactive la route par defaut
        # auto-generee par Mininet : inutile ici puisque tous les hotes
        # partagent le meme sous-reseau (10.0.0.0/8) et se joignent
        # directement via les commutateurs, sans routeur.
        h1 = self.addHost('h1', cls=Host, ip='10.0.0.1',mac='10:00:00:00:00:01', defaultRoute=None)
        h2 = self.addHost('h2', cls=Host, ip='10.0.0.2', mac='10:00:00:00:00:02', defaultRoute=None)
        h3 = self.addHost('h3', cls=Host, ip='10.0.0.3', mac='10:00:00:00:00:03', defaultRoute=None)
        h4 = self.addHost('h4', cls=Host, ip='10.0.0.4', mac='10:00:00:00:00:04', defaultRoute=None)
        h5 = self.addHost('h5', cls=Host, ip='10.0.0.5', mac='10:00:00:00:00:05', defaultRoute=None)
        h6 = self.addHost('h6', cls=Host, ip='10.0.0.6', mac='10:00:00:00:00:06', defaultRoute=None)

        # Section 2 : les 7 commutateurs OpenFlow (s1 a s7) qui composent
        # l'arbre. Chacun recoit un dpid (datapath ID) unique pour que le
        # controleur puisse les distinguer les uns des autres, et annonce la
        # version de protocole OpenFlow recue en parametre (voir plus haut).
        s1 = self.addSwitch('s1', cls=OVSKernelSwitch, dpid='0000000000000001',protocols=protocols)
        s2 = self.addSwitch('s2', cls=OVSKernelSwitch, dpid='0000000000000002',protocols=protocols)
        s3 = self.addSwitch('s3', cls=OVSKernelSwitch, dpid='0000000000000003',protocols=protocols)
        s4 = self.addSwitch('s4', cls=OVSKernelSwitch, dpid='0000000000000004',protocols=protocols)
        s5 = self.addSwitch('s5', cls=OVSKernelSwitch, dpid='0000000000000005',protocols=protocols)
        s6 = self.addSwitch('s6', cls=OVSKernelSwitch, dpid='0000000000000006',protocols=protocols)
        s7 = self.addSwitch('s7', cls=OVSKernelSwitch, dpid='0000000000000007',protocols=protocols)

        # Section 3 : les liens, qui forment un arbre binaire a 3 niveaux :
        #   s1 (racine) --- s2 --- s4 --- h1, h2
        #                |      `- s5 --- h3
        #                `- s3 --- s6 --- h4
        #                       `- s7 --- h5, h6
        # bw (Mbps) et delay (latence de propagation) varient d'un lien a
        # l'autre pour simuler un reseau heterogene : le coeur (s1-s2, s1-s3,
        # s2-s4, s2-s5, s3-s6, s3-s7) est generalement plus rapide que les
        # liens d'acces vers les hotes.
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
