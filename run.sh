#!/usr/bin/env bash
# Lance le conteneur SDN avec les privileges requis par Mininet et l'acces X11
# pour xterm / Wireshark. A executer depuis le dossier du Dockerfile.
set -euo pipefail

IMAGE="gti611-sdn"
NAME="gti611-sdn"
LAB_DIR="$(pwd)/lab"

mkdir -p "$LAB_DIR"

# Charge le module noyau OVS sur l'hote (le conteneur partage ce noyau).
# Sans danger s'il est deja charge.
sudo modprobe openvswitch \
    || echo "modprobe openvswitch a echoue; voir README (datapath espace utilisateur)."

# Autorise le root local du conteneur a parler a ton serveur X.
xhost +local:root >/dev/null 2>&1 || true

# Notes:
#   --privileged        : requis par Mininet (namespaces reseau + datapath OVS).
#   -v /lib/modules:ro  : permet a ovs-ctl de charger le module du noyau hote.
#   -p 8080:8080        : interface web Floodlight (http://localhost:8080).
#   6653 non publie     : Floodlight tourne dans le meme conteneur (ip=127.0.0.1).
#   -v lab:/lab         : partage tes scripts et fichiers de resultats.
docker run -it --rm \
    --name "$NAME" \
    --privileged \
    -e DISPLAY="${DISPLAY:-:0}" \
    -v /tmp/.X11-unix:/tmp/.X11-unix:rw \
    -v /lib/modules:/lib/modules:ro \
    -v "$LAB_DIR":/lab \
    -p 8080:8080 \
    "$IMAGE" "$@"
