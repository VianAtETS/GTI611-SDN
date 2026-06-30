# GTI611 - Laboratoire 3 (SDN) : environnement conteneurisé

Remplace la VM VirtualBox `SDN-Lab` par un conteneur Docker léger
(Mininet 2.3.0 + Open vSwitch + Floodlight 1.2). Conçu pour un hôte
**Ubuntu natif** : pas de VM imbriquée, démarrage en quelques secondes.

## Prérequis (hôte Ubuntu)

```sh
sudo apt-get install -y docker.io
sudo usermod -aG docker "$USER"   # puis reconnecte-toi (ou: newgrp docker)
```

Un serveur X (X11 ou XWayland, présent par défaut sous GNOME) est requis
pour `xterm` et Wireshark.

## Construction

```sh
docker build -t gti611-sdn .
```

La compilation de Floodlight prend quelques minutes (c'est le gros morceau).

## Lancement

```sh
chmod +x run.sh entrypoint.sh
./run.sh
```

Tu obtiens un shell **root** dans le conteneur, Open vSwitch déjà démarré.
Le dossier `./lab` (hôte) est monté sur `/lab` (conteneur). **`Tree_topo.py`
y est déjà inclus**, donc disponible à `/lab/Tree_topo.py` dès le démarrage ;
ajoutes-y `Test_topo.py` (étape 3) et récupères-y `resultTCP`, etc. Une copie
de référence en lecture seule est aussi conservée dans l'image à
`/opt/lab-ref/Tree_topo.py` (utile pour `diff` si tu modifies le script).

> [!IMPORTANT]
> `sudo` :** dans le conteneur tu es déjà root. `sudo` est
> installé, donc les commandes du laboratoire (`sudo mn ...`) fonctionnent
> telles quelles, mais tu peux aussi l'omettre.

## Plusieurs terminaux

Le laboratoire demande souvent « ouvrez un autre terminal ». Avec Docker,
ouvre d'autres shells dans le **même** conteneur depuis l'hôte :

```sh
docker exec -it gti611-sdn bash
```

## Déroulement par étape

**Étape 1 — flux manuels (sans contrôleur)**

```sh
mn --topo=tree,2,3 --mac --controller=none
# net, dump, sh ovs-ofctl dump-flows s2, sh ovs-ofctl add-flow s2 ...
```

**Étape 2 — contrôleur local Mininet**

```sh
mn --custom /lab/Tree_topo.py --topo tree --link tc
# Les commutateurs sont en OpenFlow 1.3 par défaut. Pour qu'ils se connectent
# au contrôleur de référence par défaut (OF 1.0), passe l'argument protocols :
mn --custom /lab/Tree_topo.py --topo tree,protocols=OpenFlow10 --link tc
```

**Étape 3 — contrôleur externe Floodlight**

Terminal A (un `docker exec` dédié) :

```sh
cd /opt/floodlight && java -jar target/floodlight.jar
```

Terminal B :

```sh
mn --custom /lab/Test_topo.py --topo <topo-name> \
   --controller=remote,ip=127.0.0.1,port=6653 --link tc
```

Interface web (navigateur de l'hôte) :
`http://localhost:8080/ui/index.html`

**Étape 4 — performances**

`wireshark &` ouvre la fenêtre sur ton bureau Ubuntu via X11.
`iperf` (version 2, comme dans l'énoncé) et `ping` sont disponibles.

**Nettoyage entre deux essais**

```sh
mn -c
```

## Dépannage

### Le module noyau / les commutateurs échouent
`./run.sh` exécute `sudo modprobe openvswitch` sur l'hôte. Si le module est
absent du noyau, installe-le :

```sh
sudo apt-get install -y openvswitch-switch   # fournit le module sur l'hôte
sudo modprobe openvswitch
```

### Datapath en espace utilisateur (repli sans module noyau)
Si tu ne peux pas charger le module, force le datapath userspace d'OVS en
ajoutant à **chaque** commande `mn` :

```sh
mn ... --switch ovsk,datapath=user
```

C'est plus lent mais ne dépend d'aucun module noyau.

### `Tree_topo.py` en Python 2
L'énoncé est ancien : le script du cours peut utiliser la syntaxe Python 2
(`print "x"`). Mininet 2.3.0 exécute le `--custom` en **Python 3**. Si tu
obtiens une `SyntaxError`, il faut adapter le script (ex. `print("x")`).

### Les fenêtres X11 n'apparaissent pas
Essaie une autorisation plus large : `xhost +local:` sur l'hôte. Sous
Wayland, XWayland gère le forwarding via le socket `/tmp/.X11-unix` (déjà
monté).

## Note de sécurité
`--privileged` est requis par Mininet (manipulation de namespaces réseau et
datapath OVS) ; c'est acceptable ici car le conteneur est local, éphémère
(`--rm`) et sous ton contrôle, et non un service exposé. La pile réseau
virtuelle reste isolée dans le conteneur (on n'utilise pas `--network host`,
ce qui évite de polluer le réseau de l'hôte).

## Ce que je n'ai pas pu vérifier
La compilation de Floodlight 1.2 et le comportement exact de son interface
web (vieux JavaScript) n'ont pas pu être testés dans mon environnement.
Si le `ant` échoue (tag introuvable, codegen manquant), dis-le-moi : on
ajustera (tag, JDK, ou repli sur un Floodlight pré-compilé).
