# GTI611 - Laboratoire 3 (SDN)
# Conteneur de remplacement pour la VM VirtualBox fournie.
#
# Base: Eclipse Temurin JDK 8 sur Ubuntu 22.04 (jammy).
#   - Le JDK 8 est requis pour COMPILER et EXECUTER Floodlight 1.2.
#   - jammy fournit Mininet 2.3.0 (python3) et un Open vSwitch recent.
FROM eclipse-temurin:8-jdk-jammy

ENV DEBIAN_FRONTEND=noninteractive

# Preseed: installe wireshark sans la question interactive sur le bit setuid.
RUN echo "wireshark-common wireshark-common/install-setuid boolean false" \
    | debconf-set-selections

# Outils du laboratoire. On garde les "recommends" pour que mininet tire
# ses dependances d'execution.
RUN apt-get update && apt-get install -y \
        mininet \
        openvswitch-switch \
        openvswitch-testcontroller \
        iproute2 net-tools iputils-ping \
        iperf tcpdump \
        xterm wireshark tshark x11-xserver-utils \
        python3 python3-pip python3-networkx \
        git ant \
        sudo ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Floodlight 1.2 compile depuis les sources. Le projet embarque ses
# dependances (build Ant autonome, pas de telechargement Maven a risque).
RUN git clone https://github.com/floodlight/floodlight.git /opt/floodlight \
    && cd /opt/floodlight \
    && git checkout v1.2 \
    && git submodule update --init || true \
    && ant \
    && test -f target/floodlight.jar

COPY entrypoint.sh /usr/local/bin/entrypoint.sh
RUN chmod +x /usr/local/bin/entrypoint.sh

# Copie de reference (lecture seule) du script fourni: disponible meme sans
# montage, et pratique pour 'diff' si le script monte est modifie.
COPY lab/Tree_topo.py /opt/lab-ref/Tree_topo.py

# Repertoire de travail: monte ton dossier hote ici pour partager
# Tree_topo.py, Test_topo.py et recuperer resultTCP/resultUDP/resultPing.
WORKDIR /lab

# 8080 = interface web Floodlight, 6653 = canal OpenFlow.
EXPOSE 8080 6653

ENTRYPOINT ["/usr/local/bin/entrypoint.sh"]
CMD ["bash"]
