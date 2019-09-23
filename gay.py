import sys
from panda3d.core import ConfigVariableString, loadPrcFile, loadPrcFileData, ConfigVariableManager

config = loadPrcFile("Config.prc")
loadPrcFileData('', 'fullscreen true')

myGameServer = ConfigVariableString('my-game-server', '127.0.0.1')
print('Server specified in config file: ', myGameServer.getValue())

cvMgr = config.getGlobalPtr()
cvMgr.listVariables()
