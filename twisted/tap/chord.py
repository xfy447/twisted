
# Twisted, the Framework of Your Internet
# Copyright (C) 2001 Matthew W. Lefkowitz
#
# This library is free software; you can redistribute it and/or
# modify it under the terms of version 2.1 of the GNU Lesser General Public
# License as published by the Free Software Foundation.
#
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with this library; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

"""
I am the support module for making a chord service with mktap.
"""

from twisted.spread import chord, pb
from twisted.internet import tcp, passport
from twisted.python import usage
import sys


usage_message = """Usage: mktap chord [OPTIONS]

Options:
        --port <#>, -p:         set the port number to <#>.
        --user <name>, -u:      set the username to <name>. default 'user'
        --password <word>, -w:  set the password to <word>. default 'password'
        --ip <address>, -i:     set the public IP address to <address>.
"""

class Options(usage.Options):
    optStrings = [["password", "w", "admin"],
                  ["user", "u", "admin"],
                  ["ip", "i", "127.0.0.1"]]
    
    def opt_port(self, opt):
        try:
            self.portno = int(opt)
        except ValueError:
            raise usage.error("Invalid argument to 'port'!")
    opt_p = opt_port



def getPorts(app, config):
    try:
        portno = config.portno
    except AttributeError:
        portno = pb.portno

    svc = chord.ChordService(config.ip, portno, "twisted.chord", app)
    p = svc.createPerspective(config.user)
    p.makeIdentity(config.password)

    return [(portno, pb.BrokerFactory(pb.AuthRoot(app)))]
