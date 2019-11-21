from panda3d.core import QueuedConnectionManager
from panda3d.core import QueuedConnectionListener
from panda3d.core import QueuedConnectionReader
from panda3d.core import ConnectionWriter
from panda3d.core import NetDatagram
from panda3d.core import PointerToConnection
from panda3d.core import NetAddress


from direct.task.TaskManagerGlobal import taskMgr

cManager = QueuedConnectionManager()
cListener = QueuedConnectionListener(cManager, 0)
cReader = QueuedConnectionReader(cManager, 0)
cWriter = ConnectionWriter(cManager, 0)

activeConnections = []  # We'll want to keep track of these later

port_address = 9099  # No-other TCP/IP services are using this port
backlog = 1000  # If we ignore 1,000 connection attempts, something is wrong!
tcpSocket = cManager.openTCPServerRendezvous(port_address, backlog)

cListener.addConnection(tcpSocket)

def tskListenerPolling(taskdata):
    if cListener.newConnectionAvailable():

        rendezvous = PointerToConnection()
        netAddress = NetAddress()
        newConnection = PointerToConnection()

        if cListener.getNewConnection(rendezvous, netAddress, newConnection):
            newConnection = newConnection.p()
            activeConnections.append(newConnection)  # Remember connection
            cReader.addConnection(newConnection)  # Begin reading connection
    return Task.cont

def tskReaderPolling(taskdata):
  if cReader.dataAvailable():
    datagram=NetDatagram()  # catch the incoming data in this instance
    # Check the return value; if we were threaded, someone else could have
    # snagged this data before we did
    if cReader.getData(datagram):
      myProcessDataFunction(datagram)
  return Task.cont


taskMgr.add(tskListenerPolling, "Poll the connection listener",-39)
taskMgr.add(tskReaderPolling, "Poll the connection reader",-40)

port_address = 9099  # same for client and server

# a valid server URL. You can also use a DNS name
# if the server has one, such as "localhost" or "panda3d.org"
ip_address = "localhost"

# how long until we give up trying to reach the server?
timeout_in_miliseconds = 3000  # 3 seconds

myConnection = cManager.openTCPClientConnection(ip_address, port_address, timeout_in_miliseconds)
if myConnection:
    cReader.addConnection(myConnection)  # receive messages from server

