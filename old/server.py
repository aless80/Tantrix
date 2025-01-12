import sys
#sys.path.insert(0, '/home/kinkyboy/tantrix/PodSixNet')
sys.path.insert(0, './PodSixNet')
from PodSixNet.Channel import Channel
#import PodSixNet.Server
from PodSixNet.Server import Server
from time import sleep
import random

class ClientChannel(Channel, object):
    """Receive messages from client.
    NB: self._server refers to tantrixServer ie the instance of TantrixServer"""
    def Network_serverListener(self, data):
        command = data.pop('command')
        data.pop('action')
        print("\nReceiving for " + command + ":\n  " + str(data))
        method = getattr(self, command)
        method(data)

    def test(self, data):
        """Print the remaining connections"""
        print("\n" + str(self._server.allConnections))
        self._server.sendUpdateTreeview()

    def chat(self, data):
        msgList = data['msgList']
        sendername = self._server.allConnections.getNameFromAddr(data['sender'])
        msgList[0] = sendername + ": " + msgList[0]
        self._server.sendChatToWRoom(msgList)

    def solitaire(self, data):
        """Mark players who are going solitaire in allConnections"""
        for ind in range(self._server.allConnections.count()):
            if not self._server.allConnections.addr[ind] == data['sender']:
                continue
            else:
                self._server.allConnections.ready[ind] = -2
                self._server.allConnections.ready[ind] = -2
        """Send the updated connection"""
        self._server.sendUpdateTreeview()
        """Send message to wroom that players have started a game so that they update the logbox"""
        player1 = self._server.allConnections.name[ind]
        self._server.sendGameStarted(player1, 'Solitaire')

    def toggleReady(self, data):
        addr = data["sender"]
        #print("\nReceiving in server.ClientChannel.Network_toggleReady() from player {}:\n  {}".format(str(addr), str(data)))
        ready = self._server.allConnections.toggleReadyFromAddr(addr)
        ind_game = self._server.checkConnections()
        """Send the updated connection"""
        self._server.sendUpdateTreeview()
        #"""Print the remaining connections"""
        #print("\n" + str(self._server.allConnections))
        """Send message to wroom that player has toggled ready so that they update the logbox"""
        player = self._server.allConnections.getNameFromAddr(addr)
        self._server.sendPlayerToggledReady(player, ready)
        """Send to wroom that players have started a game"""
        if ind_game:
            player1 = self._server.allConnections.name[ind_game[0]]
            player2 = self._server.allConnections.name[ind_game[0]]
            self._server.sendGameStarted(player1, 'Game', player2 = player2)

    def confirm(self, data):
        #deconsolidate all of the data from the dictionary
        #rowcolnum = data["rowcolnum"] not used
        #player number (1 or 0)
        sender = data["sender"]
        #tells server to place line
        data['action'] = "clientListener"
        data['command'] = "playConfirmedMove"
        self._server.placeMove(data, sender)

    def name(self, data):
        """Name changed"""
        sender = data["sender"]
        newname = data["newname"]
        self._server.updateName(sender, newname)

    def color(self, data):
        """Color changed"""
        sender = data["sender"]
        newcolor = data["newcolor"]
        self._server.updateColor(sender, newcolor)


    def quit(self, data):
        """One player has quit"""
        quitter = data['sender']
        #ind = self._server.allConnections.getIndexFromAddr(quitter)
        #gametype = self._server.allConnections.ready[ind]
        """Tell other players that one has quit. Must do it inside TantrixServer"""
        self._server.tellToQuit(data)
        """Delete the quitter from allConnections"""
        self._server.allConnections.removeConnection(quitter)
        self._server.sendUpdateTreeview()
        #"""Send message to wroom that one player has quit a game so that they update the logbox"""
        #self._server.sendGameQuit(quitter, gametype)

class TantrixServer(Server, object):
    """Send message to clients"""
    channelClass = ClientChannel  #needed!

    def __init__(self, *args, **kwargs):
        Server.__init__(self, *args, **kwargs)
        self.gameIndex = 0
        self.allConnections = WaitingConnections()

    def sendChatToWRoom(self, msgList):
        data = {"action": "clientListener", "command": "receiveChat", "msgList": msgList}
        self.sendToAllWRoom(data)

    def sendGameStarted(self, player1, gametype, player2 = None):
        data = {"action": "clientListener", "command": "hasstartedgame", "player1": player1, "gametype": gametype, 'player2': player2 }
        self.sendToAllWRoom(data)

    """def sendGameQuit(self, quitter, gametype):
        data = {"action": "clientListener", "command": "hasstartedgame", "player1": player1, "gametype": gametype, 'player2': player2 }
        self.sendToAllWRoom(data)\
            (quitter, gametype)
    """
    def sendPlayerToggledReady(self, player, ready):
        data = {"action": "clientListener", "command": "hastoggledready", "player": player, "ready": ready}
        self.sendToAllWRoom(data)

    def sendUpdateTreeview(self):
        listVal = self.allConnections.getAsList()
        data = {"action": "clientListener", "command": "updateTreeview", "listVal": listVal}
        self.sendToAllWRoom(data)

    def checkConnections(self):
        """Check if there are 2 connection ready. In that case start the games"""
        #print("\n" + str(self.allConnections))
        """Check if at least two players are ready"""
        players_ready = 0
        ind_game = []
        for ind in range(self.allConnections.count()):
            if self.allConnections.ready[ind] == 1:
                players_ready += 1
                #tempind = ind
                ind_game.append(ind)
        #TODO: currently the first two players who are ready will start the game. add a confirmation popup?
        if players_ready < 2:
            return False
        else:
            self.sendStartgame(ind_game)
            return ind_game

    def sendStartgame(self, ind_game):
        """Initialize a game with two players"""
        self.gameIndex += 1  #TODO Needed? I think so
        game = Game(self.allConnections.players[ind_game[0]], self.gameIndex)
        """Add all players to game"""
        game.addPlayer(self.allConnections.players[ind_game[1]])
        """Start the game. Add game to both connections (self.allConnections.game), set ready = -1"""
        for ind in ind_game:
            self.allConnections.addGame(game, self.allConnections.addr[ind])
            self.allConnections.ready[ind] = -1
        self.doSendStartingGame(ind_game)

    def Connected(self, player, addr):
        """self.game  contains the array .players"""
        print("\nReceiving a new connection: \nchannel = {},address = {}".format(player, addr))
        """Create or edit a game""" #TODO move this once players in wroom confirm each other
        if not self.allConnections.game:
            self.gameIndex += 1
        #name = "Player" + str(addr[1])
        name = "Player" + str(self.allConnections.count() + 1)
        colors = ["red", "blue", "yellow", "green"]
        color = colors.pop(self.allConnections.count() % 4)
        self.allConnections.addConnection(player, addr, 0, name = name, color = color)
        """Send confirmation that client has connected. send back the client's address"""
        data = {"action": "clientListener", "command": "clientIsConnected", "addr": addr, "color": color, "yourname": name}
        self.sendToPlayer(player, data)
        """Send an update to Treeview"""
        self.sendUpdateTreeview()

    def sendToAllWRoom(self, data):
        """Send to all players that are in wroom, ie are not playing"""
        [self.sendToPlayer(self.allConnections.players[ind], data) for ind in range(self.allConnections.count()) if self.allConnections.ready[ind] >= 0]

    def sendToPlayer(self, player, data):
        player.Send(data)
        """Print to terminal"""
        datacp = data.copy() #so that I can edit it
        name = self.allConnections.getNameFromPlayer(player)
        datacp.pop('action')
        command = datacp.pop('command')
        print("\nSent to " + name + " for " + command + ":  " + str(datacp))
        #TODO merge with clientIsConnected?

    def doSendStartingGame(self, ind_game):
        playernames = [self.allConnections.name[j] for j in ind_game]
        playercolors = [self.allConnections.color[j] for j in ind_game]
        rndgen = random.Random()
        seed = rndgen.randint(0,1000)
        for i, ind in enumerate(ind_game):
            """Get the opponent's name"""
            playernamescp = list(playernames)
            playercolorscp = list(playercolors)
            playernamescp.pop(i) #because there are two players
            playercolor = playercolorscp.pop(i) #because there are two players
            opponentname = playernamescp[0]
            opponentcolor = playercolorscp[0]
            """Send stargame"""
            data = {"action": "clientListener", "command": "startgame", "player_num": i+1,
                 "gameid": self.allConnections.game[ind].gameid, "changecolor": False,
                    "opponentname": opponentname, "opponentcolor": opponentcolor, "playerIsTabUp": i==0, "seed": seed}
            if playercolor == opponentcolor:
                data['changecolor'] = True
                self.allConnections.game[ind] = None
            self.sendToPlayer(self.allConnections.players[ind], data)

    def placeMove(self, data, sender): #TODO gameid not needed as argument
        game = self.allConnections.getGameFromAddr(sender)
        #data['turnUpDown'] = data['turnUpDown'] + 1
        game.placeLine(data, sender)

    def tellToQuit(self, data):
        quitter = data["sender"]
        ind = self.allConnections.addr.index(quitter)
        dataAll = {"action": "clientListener", "command": "hasquit", "quitter": quitter,
                   "quitterName": self.allConnections.name[ind]}
        for i in range(self.allConnections.count()):
            if i != ind and self.allConnections.game[i] == self.allConnections.game[ind]:
                p = self.allConnections.players[i]
                a = self.allConnections.addr[i]
                n = self.allConnections.name[i]
                print("\nSending to client {}:\n  {}".format(n, str(dataAll)))
                p.Send(dataAll)

    def updateName(self, sender, newname):
        """Edit name stored in allConnection"""
        index = self.allConnections.getIndexFromAddr(sender)
        """Check that name is valid"""
        def validName(newname):
            """Check that name has an allowed format"""
            """Check that name is not already taken"""
            if newname in [conn for conn in self.allConnections.name]:
                return False
            """Check that newname begins with non-numeric character"""
            import re
            if re.match('^[a-zA-Z]+', newname) is None:
                return False
            return True
        """Send to clients new name if valid or old name"""
        if validName(newname):
            data = {"action": "clientListener", "command": "newname", "name": newname}
            self.sendToPlayer(self.allConnections.players[index], data)
            self.allConnections.name[index] = newname
            """Send update to all in Waiting Room"""
            self.sendUpdateTreeview()
        else:
            name = self.allConnections.getNameFromAddr(sender)
            data = {"action": "clientListener", "command": "newname", "name": name}
            self.sendToPlayer(self.allConnections.players[index], data)


    def updateColor(self, sender, newcolor):
        """Edit color stored in allConnection"""
        index = self.allConnections.getIndexFromAddr(sender)
        self.allConnections.color[index] = newcolor
        """Send update to all in Waiting Room"""
        self.sendUpdateTreeview()  #TODO: make sure client gets the color as well

class Game(object):
    def __init__(self, player, gameIndex):
        # whose turnUpDown (1 or 0)
        self.turn = 1
        #Storage
        self._confirmedgame = []
        #initialize the players including the one who started the game
        self.players = []
        self.addPlayer(player)
        #gameid of game
        self.gameid = gameIndex

    def __str__(self):
        string= str(self.gameid)
        return string

    def addPlayer(self, player):
        if player is not None and player not in self.players:
            self.players.append(player)
        else:
            print("Game.addPlayer failed: player is None or was already added")

    def placeLine(self, data, sender):
        #make sure it's their turnUpDown TODO
        turnUpDown = data['turnUpDown']
        if self.turn is not turnUpDown:
            print("       \n\n>>>>>>>>>>placeLine: self.turn is not data['turnUpDown']: {}~={}".format(self.turn, turnUpDown))
        self.turn += 1
        data['turnUpDown'] =self.turn
        print("       \n\n>>>>>>>>self.turnUpDown="+str(self.turn) + "\n\n")
        ####
        if 1 or sender == self.turn + 1: #TODO
            self.turn = 0 if self.turn else 1
            #place line in game
            #?? NEEDED? self._confirmedgame.append(rowcolnum)
            #send data and turnUpDown to the opponent
            #TODO mv everythiong to TantrixServer
            opponents = tantrixServer.allConnections.getOpponentsFromAddress(sender)
            for o in opponents:
                print("\nSending to other player:\n  " + str(data))
                o.Send(data)

class WaitingConnections(object):
    def __init__(self):
        """Initialize the players"""
        self.players = []
        self.addr = []
        self.game = []
        self.ready = []
        self.name = []
        self.color = []

    def getAsList(self):
        """Return the connections as list for Treeview in wroom eg:
        [('Alessandro', 0, 43932, None, 'red'),('Mararie', -1, 2, 1, 'yellow'), ..] """
        return [list([self.name[ind], self.ready[ind], self.addr[ind][1], str(self.game[ind]), self.color[ind]]) for ind in range(self.count())]

    def addConnection(self, player, addr, ready = 0, game = None, name = "unknown", color = "cyan"):
        self.players.append(player)
        self.addr.append(addr)
        self.ready.append(ready)
        self.game.append(game)
        self.name.append(name)
        self.color.append(color)

    def addGame(self, game, addr):
        ind = self.addr.index(addr)
        self.game[ind] = game

    def removeConnection(self, addr):
        ind = self.addr.index(addr)
        self.addr.pop(ind)
        self.players.pop(ind)
        self.game.pop(ind)
        self.ready.pop(ind)
        self.name.pop(ind)
        self.color.pop(ind)

    def count(self):
        return len(self.players)

    def getIndexFromAddr(self, addr):
        return self.addr.index(addr)

    def getNameFromAddr(self, addr):
        ind = self.getIndexFromAddr(addr)
        return self.name[ind]

    def getGameFromPlayer(self, player):
        ind = self.players.index(player)
        return self.game[ind]

    def getNameFromPlayer(self, player):
        ind = self.players.index(player)
        return self.name[ind]

    def getGameFromAddr(self, addr):
        ind = self.addr.index(addr)
        return self.game[ind]

    def getPlayerFromAddr(self, addr):
        ind = self.addr.index(addr)
        return self.players[ind]

    def getColorFromAddr(self, addr):
        ind = self.addr.index(addr)
        return self.color[ind]

    def getOpponentsFromAddress(self, addr):
        """Given a player, return a list of players in the game"""
        game = self.getGameFromAddr(addr)
        ind_sender = self.getIndexFromAddr(addr)
        opponents = []
        for ind in range(self.count()):
            if ind != ind_sender and self.game[ind] == game:
                opponents.append(self.players[ind])
        return opponents
        #return [x for i, x in enumerate(self.players) if x == player and self.addr[i] is not addr]

    def toggleReadyFromAddr(self, addr):
        """Toggle ready flag for a certain address. return the 'ready' status"""
        try:
            ind = self.addr.index(addr)
        except:
            import inspect
            print("Unexpected error at :", inspect.stack()[0][3])
            print("addr="+ str(addr) + " is not contained in self.addr="+ str(self.addr))
            raise
        self.ready[ind] = (self.ready[ind] + 1) %2
        return self.ready[ind]

    def __str__(self):
        string = "Connections:\n<======================"
        string += "\nname, ready, addr, players, game:\n"
        for ind in range(self.count()):
            string += "{}, {}, {}, {}, {}\n".format(
                str(self.name[ind]),
                str(self.ready[ind]),
                str(self.addr[ind]),
                str(self.players[ind]),
                str(self.game[ind]),
                self.color[ind])
        string += "======================>\n"
        return string

"""Get command line argument of server, port"""
if len(sys.argv) != 2:
    print("Usage:", sys.argv[0], "host:port")
    print("  e.g.", sys.argv[0], "localhost:31425")
    #Launch anyway
    host = "localhost"
    port = 31425
    print("Launcing with host, port = %s , %d" % (host, port))
else:
    host, port = sys.argv[1].split(":")

print("STARTING SERVER ON LOCALHOST")
try:
    tantrixServer = TantrixServer(localaddr=(host, int(port)))  #'localhost', 1337
except:
    print("Address '" + host + "' already in use")
    raise

while True:
    tantrixServer.Pump()
    sleep(0.01)

