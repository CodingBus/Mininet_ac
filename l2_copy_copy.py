# Copyright 2012 James McCauley
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
A super simple OpenFlow learning switch that installs rules for
each pair of L2 addresses.
"""

# These next two imports are common POX convention
from pox.core import core
import pox.openflow.libopenflow_01 as of
from pox.lib.revent import *
import time
# Even a simple usage of the logger is much nicer than print!
log = core.getLogger()


# This table maps (switch,MAC-addr) pairs to the port on 'switch' at
# which we last saw a packet *from* 'MAC-addr'.
# (In this case, we use a Connection object for the switch.)
table = {}
mac_to_port = {"00:00:00:00:01": 2,
               "00:00:00:00:02": 4,
	       "00:00:00:00:03": 1,
	       "00:00:00:00:04": 3}
# To send out all ports, we can uue either of the special ports
# OFPP_FLOOD or OFPP_ALL.  We'd like to just use OFPP_FLOOD,
# but it's not clear if all switches support this, so we make
# it selectable.
all_ports = of.OFPP_FLOOD




# Handle messages the switch has sent us because it has no
# matching rule.
def _handle_PacketIn (event):
  packet = event.parsed

  dst_port = mac_to_port[str(packet.dst)]
  log.info(dst_port)
  msg = of.ofp_flow_mod()
  msg.data = event.ofp 
  msg.match.dl_src = packet.src
  msg.match.dl_dst = packet.dst
  msg.actions.append(of.ofp_action_output(port = dst_port))
  event.connection.send(msg)


class DayTimeEvent(Event):
  def __init__(self):
    Event.__init__(self)
    
  def foo(self):
    return "Test event!"

class Handy(EventMixin):
  _eventMixin_events = set([DayTimeEvent])
 
def _handle_DayTimeEvent(event):
  pass
  #log.info(event.foo())

def launch (disable_flood = False):
  global all_ports
  if disable_flood:
    all_ports = of.OFPP_ALL

  core.openflow.addListenerByName("PacketIn", _handle_PacketIn)

  log.info("Pair-Learning switch running.")
  handy = Handy()
  handy.addListener(DayTimeEvent, _handle_DayTimeEvent)
  # regularly check time of day and update actions in the flow table
  while(True):
    time.sleep(2)
    dte = DayTimeEvent()
    handy.raiseEvent(dte)
