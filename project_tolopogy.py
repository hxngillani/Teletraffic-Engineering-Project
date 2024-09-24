from mininet.topo import Topo
from mininet.net import Mininet
from mininet.node import OVSSwitch
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import setLogLevel

class InterVLANRoutingTopo(Topo):
    def build(self):
        # Create one switch
        switch = self.addSwitch('s1')

        # Create the router (r1 will act as a router for inter-VLAN routing)
        router = self.addHost('r1')  # Router with two internal interfaces

        # Create hosts in the first subnet (192.168.10.0/24)
        host1 = self.addHost('h1', ip='192.168.10.1/24')
        host2 = self.addHost('h2', ip='192.168.10.2/24')

        # Create hosts in the second subnet (192.168.20.0/24)
        host3 = self.addHost('h3', ip='192.168.20.1/24')
        host4 = self.addHost('h4', ip='192.168.20.2/24')

        # Add links between router and switch (router will have 2 internal interfaces)
        self.addLink(router, switch, cls=TCLink, intfName1='r1-eth0')  # Connect r1-eth0 to switch (VLAN 10)
        self.addLink(router, switch, cls=TCLink, intfName1='r1-eth1')  # Connect r1-eth1 to switch (VLAN 20)

        # Add links between hosts and switch with bandwidth limits
        self.addLink(host1, switch, cls=TCLink, bw=10)  # 10 Mbps for h1
        self.addLink(host2, switch, cls=TCLink, bw=10)  # 10 Mbps for h2
        self.addLink(host3, switch, cls=TCLink, bw=0.1)  # 0.1 Mbps for h3
        self.addLink(host4, switch, cls=TCLink, bw=0.1)  # 0.1 Mbps for h4

def start_mininet():
    setLogLevel('info')

    # Setup Mininet topology
    topo = InterVLANRoutingTopo()
    net = Mininet(topo=topo, switch=OVSSwitch, link=TCLink)
    net.start()

    # Get the hosts and router
    router = net.get('r1')
    host1 = net.get('h1')
    host2 = net.get('h2')
    host3 = net.get('h3')
    host4 = net.get('h4')
    switch = net.get('s1')

    # Apply VLAN settings
    switch.cmd('ovs-vsctl set port s1-eth1 tag=10')  # h1 on VLAN 10
    switch.cmd('ovs-vsctl set port s1-eth2 tag=10')  # h2 on VLAN 10
    switch.cmd('ovs-vsctl set port s1-eth3 tag=20')  # h3 on VLAN 20
    switch.cmd('ovs-vsctl set port s1-eth4 tag=20')  # h4 on VLAN 20
    switch.cmd('ovs-vsctl set port s1-eth5 tag=10')  # r1-eth0 (VLAN 10 interface for the router)
    switch.cmd('ovs-vsctl set port s1-eth6 tag=20')  # r1-eth1 (VLAN 20 interface for the router)

    # Assign IP addresses to the router's interfaces (internal VLANs)
    router.cmd('ifconfig r1-eth0 192.168.10.254 netmask 255.255.255.0')  # VLAN 10 gateway
    router.cmd('ifconfig r1-eth1 192.168.20.254 netmask 255.255.255.0')  # VLAN 20 gateway

    # Enable IP forwarding on the router (r1)
    print("Enabling IP forwarding on the router (r1)...")
    router.cmd('sysctl -w net.ipv4.ip_forward=1')

    # Set up default routes on the hosts to point to the router
    print("Configuring routes on hosts...")
    host1.cmd('ip route add default via 192.168.10.254')  # Route through r1 for VLAN 10
    host2.cmd('ip route add default via 192.168.10.254')  # Route through r1 for VLAN 10
    host3.cmd('ip route add default via 192.168.20.254')  # Route through r1 for VLAN 20
    host4.cmd('ip route add default via 192.168.20.254')  # Route through r1 for VLAN 20

    # Test inter-VLAN connectivity with ping
    print("Ping Test: h1 to h3 (VLAN 10 -> VLAN 20)")
    net.ping([host1, host3])

    print("Ping Test: h2 to h4 (VLAN 10 -> VLAN 20)")
    net.ping([host2, host4])

    print("Ping Test: h1 to h2 (same VLAN 10)")
    net.ping([host1, host2])

    print("Ping Test: h3 to h4 (same VLAN 20)")
    net.ping([host3, host4])

    # Enter CLI for manual testing
    CLI(net)

    net.stop()

if __name__ == '__main__':
    start_mininet()

