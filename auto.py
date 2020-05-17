#!/usr/bin/python

"""
Run with 'sudo python ./auto.py'

Automate topology setup.
"""

from mininet.log import setLogLevel
from mininet.net import Mininet
from mininet.topo import SingleSwitchTopo, Topo
from mininet.cli import CLI
from mininet.node import Controller, RemoteController, OVSKernelSwitch

# We assume you are in the same directory as pox.py
# or that it is loadable via PYTHONPATH
# from pox import POX

class MyTopo(Topo):
    def __init__(self):
        Topo.__init__(self)
        host1 = self.addHost('OWNER')
        host2 = self.addHost('GUEST')
        host3 = self.addHost('SMARTTV')
        host4 = self.addHost('LIGHTS')
        switch = self.addSwitch('s1')


        self.addLink(switch, host1)
        self.addLink(switch, host2)
        self.addLink(switch, host3)
        self.addLink(switch, host4)

topos = { 'mytopo': ( lambda: MyTopo() ) }



setLogLevel( 'info' )

#net = Mininet( topo=SingleSwitchTopo( 4 ),
#               controller=POX )
mycontroller = RemoteController('c1')
net = Mininet( topo=MyTopo(), controller=mycontroller, cleanup=True, 
		autoSetMacs=True, autoStaticArp=True )
# This controller cannot be named 'c0' since that is the default and will
# confuse the network. Need a remote controller for POX to set up a learning
# switch.
#net.addController('c1', controller=RemoteController)

net.start()
CLI( net )
net.stop()
