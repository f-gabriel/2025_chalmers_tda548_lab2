from math import sin,cos,radians
import random

### är det ok att ha objekt.attribut, eller objekt.getAttributA.attribubtB, eller ska det vara objekt.getAttributA().getattribubtB()

### We've added Game.newGame() and Player.resetScore() for our own implimentation of a win-condition. 

""" This is the model of the game"""
class Game:
    """ Create a game with a given size of cannon (length of sides) and projectiles (radius) """
    def __init__(self, cannonSize, ballSize):
        self.cannonSize = cannonSize
        self.ballSize = ballSize
        self.players = [
            Player(self, 0, 'blue', -90, False), 
            Player(self, 1, 'red', 90, True)
            ]
        self.currentPlayerNumber = 0
        self.newRound() ### sätter vinden för första rundan
        

    """ A list containing both players """
    def getPlayers(self):
        return self.players

    """ The height/width of the cannon """
    def getCannonSize(self):
        return self.cannonSize

    """ The radius of cannon balls """
    def getBallSize(self):
        return self.ballSize

    """ The current player, i.e. the player whose turn it is """
    def getCurrentPlayer(self):
        return self.getPlayers()[self.currentPlayerNumber] 

    """ The opponent of the current player """
    def getOtherPlayer(self):
        otherPlayerNumber = 1 - self.currentPlayerNumber ### (ger motsatt nr (0 eller 1) mot nuvarande player-nr)
        return self.getPlayers()[otherPlayerNumber] 
    
    """ The number (0 or 1) of the current player. This should be the position of the current player in getPlayers(). """
    def getCurrentPlayerNumber(self):
        return self.currentPlayerNumber
    
    """ Switch active player """
    def nextPlayer(self):
        self.currentPlayerNumber = self.getOtherPlayer().nr ### Se ovan: 

    """ Set the current wind speed, only used for testing """
    def setCurrentWind(self, wind):
        self.wind = wind
    
    def getCurrentWind(self):
        return self.wind

    """ Start a new round with a random wind value (-10 to +10) """
    def newRound(self):
        self.wind = random.random() * 20 - 10

    ### Method is called from graphicsMain when a player has won a game calls, and then calls Player.resetScore() for both players 
    def newGame(self):
        self.getCurrentPlayer().resetScore()
        self.getOtherPlayer().resetScore()

""" Models a player """
class Player:
    def __init__(self, game, player_nr, color, x_pos, isReversed):
        self.game = game
        self.nr = player_nr
        self.color = color
        self.x_pos = x_pos
        self.isReversed = isReversed
        
        self.score = 0
        self.angle = 45
        self.velocity = 40
        

    """ Create and return a projectile starting at the centre of this players cannon. Replaces any previous projectile for this player. """
    def fire(self, angle, velocity):
        self.angle = angle ### self.angle, self.velocity = angle, velocity
        self.velocity = velocity
        wind = self.game.getCurrentWind()
        yPos = self.game.getCannonSize() / 2
        
        if self.isReversed:
            angle = 180 - angle

        proj = Projectile(angle, velocity, wind, self.x_pos, yPos, -110, 110)

        return proj

    """ Gives the x-distance from this players cannon to a projectile. If the cannon and the projectile touch (assuming the projectile is on the ground and factoring in both cannon and projectile size) this method should return 0"""
    def projectileDistance(self, proj):
        cannonsEdge = self.game.getCannonSize() / 2
        ballSize = self.game.getBallSize()
        distance = proj.getX() - self.getX()
        distance -= (distance / abs(distance)) * (ballSize + cannonsEdge) ### distance / abs(distance) = tecknet för distance
        
        ### om projectile är inuti cannon.
        if (
            self.getX() - (cannonsEdge + ballSize) 
            <= proj.getX() 
            <= (self.getX() + (cannonsEdge + ballSize))
            ): 
            distance = 0

        return distance

    """ The current score of this player """
    def getScore(self):
        return self.score
    
    """ Increase the score of this player by 1."""
    def increaseScore(self):
        self.score += 1

    """ Returns the color of this player (a string)"""
    def getColor(self):
        return self.color
    
    ### returns number of player
    def getNumber(self):
        return self.nr

    """ The x-position of the centre of this players cannon """
    def getX(self):
        return self.x_pos
    
    """ The angle and velocity of the last projectile this player fired, initially (45, 40) """
    def getAim(self):
        return (self.angle, self.velocity)

    ### is called from Game.newGame() when the scores need to be reset before a new game
    def resetScore(self):
        self.score = 0



""" Models a projectile (a cannonball, but could be used more generally) """
class Projectile: 
    """
        Constructor parameters:
        angle and velocity: the initial angle and velocity of the projectile 
            angle 0 means straight east (positive x-direction) and 90 straight up
        wind: The wind speed value affecting this projectile
        xPos and yPos: The initial position of this projectile
        xLower and xUpper: The lowest and highest x-positions allowed
    """
    def __init__(self, angle, velocity, wind, xPos, yPos, xLower, xUpper):
        self.yPos = yPos
        self.xPos = xPos
        self.xLower = xLower
        self.xUpper = xUpper
        theta = radians(angle)
        self.xvel = velocity*cos(theta)
        self.yvel = velocity*sin(theta)
        self.wind = wind


    """ 
        Advance time by a given number of seconds
        (typically, time is less than a second, 
         for large values the projectile may move erratically)
    """
    def update(self, time):
        # Compute new velocity based on acceleration from gravity/wind
        yvel1 = self.yvel - 9.8*time
        xvel1 = self.xvel + self.wind*time
        
        # Move based on the average velocity in the time period 
        self.xPos = self.xPos + time * (self.xvel + xvel1) / 2.0
        self.yPos = self.yPos + time * (self.yvel + yvel1) / 2.0
        
        # make sure yPos >= 0
        self.yPos = max(self.yPos, 0)
        
        # Make sure xLower <= xPos <= mUpper   
        self.xPos = max(self.xPos, self.xLower)
        self.xPos = min(self.xPos, self.xUpper)
        
        # Update velocities
        self.yvel = yvel1
        self.xvel = xvel1
        
    """ A projectile is moving as long as it has not hit the ground or moved outside the xLower and xUpper limits """
    def isMoving(self):
        return 0 < self.getY() and self.xLower < self.getX() < self.xUpper

    def getX(self):
        return self.xPos

    """ The current y-position (height) of the projectile". Should never be below 0. """
    def getY(self):
        return self.yPos


