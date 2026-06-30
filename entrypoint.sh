#!/usr/bin/env bash
set -e

mkdir -p /var/run/openvswitch /var/log/openvswitch /etc/openvswitch

# Start ovsdb-server + ovs-vswitchd. ovs-ctl creates the DB on first run and
# loads the openvswitch kernel module (requires --privileged and the host
# /lib/modules mount). --delete-bridges gives a clean slate on each run.
if ! /usr/share/openvswitch/scripts/ovs-ctl --system-id=random --delete-bridges start; then
    echo "WARN: Open vSwitch did not start cleanly." >&2
    echo "      If Mininet switches fail, the host kernel module is likely missing." >&2
    echo "      See README.md, section 'Datapath en espace utilisateur'." >&2
fi

exec "$@"
