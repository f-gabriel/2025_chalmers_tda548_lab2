from gamemodel import *
from graphics import *

### Att göra: 
   
   ### lägg till text för att säga hur många poäng som behövs för att vinna
       ### ex. 'best of three'
       ### kan läggas i startfönstret, men är nog lättare att lägga i en ny metod, liknande drawScore()
   

### We've added our own code for a win-condition including a message to the winner and resetting the score for the current game.

class GameGraphics:
    def __init__(self, game):
        self.game = game

        # open the window
        self.win = GraphWin("Cannon game" , 640, 480, autoflush=False)
        self.win.setCoords(-110, -10, 110, 155)
        
        # draw the terrain
        p1 = Point(-110, 0)
        p2 = Point(110,0)
        self.draw_terrain = Line(p1, p2)
        self.draw_terrain.draw(self.win)

        self.draw_cannons = [self.drawCanon(0), self.drawCanon(1)]
        self.draw_scores  = [self.drawScore(0), self.drawScore(1)]
        self.draw_projs   = [None, None] ### sparar de ritade projektilerna
        self.draw_winCon  = self.drawWinCondition() ### Saves the win condition text.

    ### Ritar en kanon från punkt 1 till 2 (dvs p1 & p2) genom Rectangle-class och färgar den.
    def drawCanon(self,playerNr):
        x_pos = self.game.getPlayers()[playerNr].getX() 
        size = self.game.getCannonSize()
        p1 = Point(x_pos - size / 2, size)
        p2 = Point(x_pos + size / 2, 0)

        draw_cannon = Rectangle(p1, p2)
        draw_cannon.setFill(self.game.getPlayers()[playerNr].getColor()) 
        draw_cannon.setOutline(self.game.getPlayers()[playerNr].getColor()) 
        draw_cannon.draw(self.win)
       
        return draw_cannon

    ### skriver poängantalet under varje spelare
    def drawScore(self,playerNr):
        msg = f'Score: {self.game.getPlayers()[playerNr].getScore()}'  ### getScore()
        x_pos = self.game.getPlayers()[playerNr].getX()  ### getColor()
        y_pos = -5  ### Ett godtyckligt tal (mellan botten av window och cannon)
        draw_score = Text(Point(x_pos, y_pos), msg)
        draw_score.draw(self.win)
        return draw_score
    
    ### Tells the player about the win condition is called from
    def drawWinCondition(self):
        draw_message = Text(Point(0, -5), 'Game is best of three')
        draw_message.draw(self.win)
        return (draw_message)


    ### Ritar/animerar kanonkulan
    def fire(self, angle, vel):
        player = self.game.getCurrentPlayer()
        proj = player.fire(angle, vel)

        circle_X = proj.getX()
        circle_Y = proj.getY()

        if  not self.draw_projs[player.getNumber()] == None:
            self.draw_projs[player.getNumber()].undraw() 

        p = Point(circle_X, circle_Y)
        size = self.game.getBallSize() 
        circle = Circle(p, size)
        circle.setFill(player.getColor())
        circle.setOutline(player.getColor())
        circle.draw(self.win)

        while proj.isMoving():
            proj.update(1/50)

            # move is a function in graphics. It moves an object dx units in x direction and dy units in y direction
            circle.move(proj.getX() - circle_X, proj.getY() - circle_Y)

            circle_X = proj.getX()
            circle_Y = proj.getY()

            update(50)
        
        self.draw_projs[player.getNumber()] = circle
        return proj

    def updateScore(self,playerNr):
        self.draw_scores[playerNr].undraw()
        self.draw_scores[playerNr] = self.drawScore(playerNr)
        
    ### Animerar en explosion (kallas vid träff av kanonen)
    def explode(self, other, player):
        target = other.getX()
        color = player.getColor()
        diameter = self.game.getBallSize()
        maxExplosion = self.game.getCannonSize() * 2

        while diameter <= maxExplosion:
            explCircle = Circle(Point(target, 0), diameter)
            explCircle.setFill(color)
            explCircle.setOutline(color)
            explCircle.draw(self.win)
            diameter += 1

            update(50)
            explCircle.undraw()

    ### A new method that displays a message when a player wins the game.
    def congratulations(self, player):
        win = GraphWin("Winner", 600, 400, True)
        congratText = Text(Point(250,200), f'Congratulations {player.getColor()} player!')
        congratText.draw(win).setFill(player.getColor())
        newGameText = Text(Point(250,250), 'Click to go to new game').draw(win)
        newGameText.draw(win).setFill(player.getColor())
        win.getMouse()
        win.close()
        
    def play(self):
        while True:
            player = self.game.getCurrentPlayer()
            oldAngle,oldVel = player.getAim()
            wind = self.game.getCurrentWind()
            
            # InputDialog(self, angle, vel, wind) is a class in gamegraphics
            inp = InputDialog(oldAngle,oldVel,wind)
            # interact(self) is a function inside InputDialog. It runs a loop until the user presses either the quit or fire button
            if inp.interact() == "Fire!": 
                angle, vel = inp.getValues()
                inp.close()
            elif inp.interact() == "Quit":
                exit()

            player = self.game.getCurrentPlayer()
            other = self.game.getOtherPlayer()
            proj = self.fire(angle, vel)
            distance = other.projectileDistance(proj)
            
            if distance == 0.0:
                player.increaseScore()
                self.updateScore(self.game.getCurrentPlayerNumber())
                self.explode(other, player)
                self.game.newRound()

            ### Displays a message when a wincondition is met and then resets the game
            if player.getScore() >= 2:
                self.congratulations(player)
                self.game.newGame()
                self.updateScore(0) 
                self.updateScore(1)

            self.game.nextPlayer()


class InputDialog:
    def __init__ (self, angle, vel, wind):
        self.win = win = GraphWin("Fire", 200, 300)
        win.setCoords(0,4.5,4,.5)
        Text(Point(1,1), "Angle").draw(win)
        self.angle = Entry(Point(3,1), 5).draw(win)
        self.angle.setText(str(angle))
        
        Text(Point(1,2), "Velocity").draw(win)
        self.vel = Entry(Point(3,2), 5).draw(win)
        self.vel.setText(str(vel))
        
        Text(Point(1,3), "Wind").draw(win)
        self.height = Text(Point(3,3), 5).draw(win)
        self.height.setText("{0:.2f}".format(wind))
        
        self.fire = Button(win, Point(1,4), 1.25, .5, "Fire!")
        self.fire.activate()
        self.quit = Button(win, Point(3,4), 1.25, .5, "Quit")
        self.quit.activate()

    def interact(self):
        while True:
            pt = self.win.getMouse()
            if self.quit.clicked(pt):
                return "Quit"
            if self.fire.clicked(pt):
                return "Fire!"

    def getValues(self):
        a = float(self.angle.getText())
        v = float(self.vel.getText())
        return a,v

    def close(self):
        self.win.close()


class Button:

    def __init__(self, win, center, width, height, label):

        w,h = width/2.0, height/2.0
        x,y = center.getX(), center.getY()
        self.xmax, self.xmin = x+w, x-w
        self.ymax, self.ymin = y+h, y-h
        p1 = Point(self.xmin, self.ymin)
        p2 = Point(self.xmax, self.ymax)
        self.rect = Rectangle(p1,p2)
        self.rect.setFill('lightgray')
        self.rect.draw(win)
        self.label = Text(center, label)
        self.label.draw(win)
        self.deactivate()

    def clicked(self, p):
        return self.active and \
               self.xmin <= p.getX() <= self.xmax and \
               self.ymin <= p.getY() <= self.ymax

    def getLabel(self):
        return self.label.getText()

    def activate(self):
        self.label.setFill('black')
        self.rect.setWidth(2)
        self.active = 1

    def deactivate(self):
        self.label.setFill('darkgrey')
        self.rect.setWidth(1)
        self.active = 0


GameGraphics(Game(11,3)).play()

