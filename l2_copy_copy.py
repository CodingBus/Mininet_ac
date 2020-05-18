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
mac_to_port = {"00:00:00:00:00:01": 2,
               "00:00:00:00:00:02": 4,
	       "00:00:00:00:00:03": 1,
	       "00:00:00:00:00:04": 3}
# To send out all ports, we can uue either of the special ports
# OFPP_FLOOD or OFPP_ALL.  We'd like to just use OFPP_FLOOD,
# but it's not clear if all switches support this, so we make
# it selectable.
all_ports = of.OFPP_FLOOD
"""
Hardcoded AC table to return whether or not a user is allowed to access a file.
"""

import datetime

ac_table = {("00:00:00:00:00:01", "00:00:00:00:00:02"): (6, 22),
            ("00:00:00:00:00:01", "00:00:00:00:00:04"): (12, 18),
            ("00:00:00:00:00:03", "00:00:00:00:00:02"): (0, 0),
            ("00:00:00:00:00:03", "00:00:00:00:00:04"): (0, 0)}

# Arguments are the hours of valid access. True if access granted
def getAccess(start, end):
  # Always have access
  if (start == 0 and end == 0):
    return True
  now = datetime.datetime.now()
  today_start = now.replace(hour=start, minute=0, second=0, microsecond=0)
  today_end = now.replace(hour=end, minute=0, second=0, microsecond=0)
  return today_start < now < today_end
"""
def main():
  start, end = ac_table[("00:00:00:00:00:03", "00:00:00:00:00:04")]
  print(getAccess(start, end))
  print(datetime.datetime.now())
  return
"""



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

def _handle_ConnectionUp(event):
  log.info("connected")

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
  msg.hard_timeout = 3
  msg.actions.append(of.ofp_action_output(port = dst_port))
  event.connection.send(msg)

def f():
  log.info("HERE")

def launch (disable_flood = False):
  global all_ports
  if disable_flood:
    all_ports = of.OFPP_ALL

  core.openflow.addListenerByName("PacketIn", _handle_PacketIn)
  log.info("Pair-Learning switch running.")
