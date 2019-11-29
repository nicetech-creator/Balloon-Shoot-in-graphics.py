from graphics import *
from time import *
import math
import random
import time
import threading

class Balloon(Circle):
	def __init__(self, win, center, radius):
		super().__init__(center, radius)
		self.speed = random.randint(1, 3) / 10
		self.win = win
		self.points = random.randint(1, 3)

	def draw_balloons(self):
		print ('hi')
		super().setFill(color_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
		super().setOutline(color_rgb(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
		super().draw(self.win)
		self.aLine = Line(Point(self.getCenter().getX(),self.getCenter().getY() - self.getRadius()),
			 Point(self.getCenter().getX(),self.getCenter().getY() - 2 * self.getRadius()))
		self.aLine.draw(self.win)

	def move_ballons(self):
		super().move(0, self.speed)
		self.aLine.move(0, self.speed)
		time.sleep(0.04)
	
	def is_hit(self, p):
		# get the distance between pt1 and circ using the
	    # distance formula
	    dx = p.getX() - self.getCenter().getX()
	    dy = p.getY() - self.getCenter().getY()
	    dist = math.sqrt(dx*dx + dy*dy)

	    # check whether the distance is less than the radius
	    return dist <= self.getRadius()

	def undraw_ballons(self):
		super().undraw()
		self.aLine.undraw()

class Bug:
	def __init__(self, win):
		self.win = win
		self.BugSpeedX = 0.7
		self.BugSpeedY = 0.5
		self.points = 5

	def loadGIF(self, img):
		self.Bug = Image(Point(random.randint(5, 35), random.randint(5, 25)), img)
		self.Bug.draw(self.win)

	def move_bug(self):
		BspeedX = ( (math.ceil( 0.5 - random.random() ) * 2) - 1 ) * self.BugSpeedX
		BspeedY = ( (math.ceil( 0.5 - random.random() ) * 2) - 1 ) * self.BugSpeedY
		self.Bug.move(BspeedX, BspeedY)
	
	def undraw_bug(self):
		self.Bug.undraw()

	def is_hit(self, p):
		c = self.Bug.getAnchor()
		dx = p.getX() - c.getX()
		dy = p.getY() - c.getY()
		dist = math.sqrt(dx*dx + dy*dy)
		return dist <= 1

def draw_cloud(win, x1,x2,y1,y2):
    cloud_list = []
    for i in range(11):
        x = random.randint(x1, x2)
        y = random.randint(y1, y2)
        p = Point(x,y)

        cloud = Circle(p,2)
        cloud.setFill("white")
        cloud.setOutline("white")
        cloud.draw(win)
        cloud_list.append(cloud)
    return cloud_list

def backGround(win):
	# set the background color  (width is 40, height is 30)
	BackGround = Rectangle(Point(0,15), Point(40, 30))
	BackGround.setFill("light blue")
	BackGround.draw(win)

	# set the Ground color
	Ground = Rectangle(Point(0,0) , Point(40, 15))
	Ground.setFill("light Green")
	Ground.draw(win)

	# draw the sun
	sun = Circle(Point(20,25), 2)
	sun.setFill("Yellow")
	sun.setOutline("Yellow")
	sun.draw(win)

	# draw the mountain1
	Mountain1 = Polygon(Point(0,15), Point(15, 28), Point(30,15))
	Mountain1.setFill("dark green")
	Mountain1.draw(win)

	# draw the mountain2
	Mountain2 = Polygon(Point(10,15), Point(23,26), Point(40,15))
	Mountain2.setFill("dark green")
	Mountain2.draw(win)

	m1 = draw_cloud(win, 5,10,20,21)

	# # === call draw_cloud function for the right side of the sky ===
	m2 = draw_cloud(win, 24,29,22,23)

def buttons(win):
	start =  Rectangle(Point(2,3), Point(6, 5))
	start.setFill("yellow")
	start.draw(win)

	ViewMsg = Text(Point(4, 4), "Start")
	ViewMsg.setStyle("bold")
	ViewMsg.setTextColor("black")
	ViewMsg.draw(win)

	exit = Rectangle(Point(7,3), Point(11, 5))
	exit.setFill("yellow")
	exit.draw(win)

	ViewMsg = Text(Point(9, 4), "Exit")
	ViewMsg.setStyle("bold")
	ViewMsg.setTextColor("black")
	ViewMsg.draw(win)
	
	inputBox = Entry(Point(15,4), 5)
	inputBox.setSize(24)
	inputBox.setText("1")
	inputBox.draw(win)

	ViewMsg = Text(Point(15, 6), "Bets $")
	ViewMsg.setStyle("bold")
	ViewMsg.setTextColor("black")
	ViewMsg.draw(win)

	ViewMsg = Text(Point(30, 4), "Balance $0")
	ViewMsg.setStyle("bold")
	ViewMsg.setTextColor("blue")
	ViewMsg.draw(win)

	return start, exit, inputBox, ViewMsg

def buttonClick(pt, button):
	if pt.getX() > button.getP1().getX() and pt.getY() > button.getP1().getY() and pt.getX() < button.getP2().getX() and pt.getY() < button.getP2().getY():
		return True
	return False


def main():
	win = GraphWin("Blue sky and green field!", 800, 600)
	win.setCoords(0, 0, 40, 30)

	backGround(win)
	start, exit, inputBox, ViewMsg = buttons(win)
	
	ballons = []
	bug = Bug(win)
	bug.loadGIF("bug.gif")

	bet = int(inputBox.getText())
	score = 0

	while True:
		time.sleep(0.04)
		for ballon in ballons:
			ballon.move_ballons()
		if bug != None:
			bug.move_bug()
		p = win.checkMouse()
		if p != None:
			if buttonClick(p, start):
				if bug != None:
					bug.undraw_bug()
				bug = Bug(win)
				bug.loadGIF("bug.gif")

				for ballon in ballons:
					ballon.undraw_ballons()
				ballons = []
				for i in range(random.randint(5, 10)):
					ballon = Balloon(win, Point(random.randint(5, 35), random.randint(6, 25)), random.randint(1, 4))
					ballon.draw_balloons()
					ballons.append(ballon)
				bet = int(inputBox.getText())
				score = 0
				ViewMsg.setText('Balance ${}'.format(score))
			elif buttonClick(p, exit):
				win.close()
			else:
				if bug != None and bug.is_hit(p):
					score = score + bug.points * bet
					bug.undraw_bug()
					bug = None
				for i, ballon in enumerate(ballons):
					if ballon.is_hit(p):
						ballon.undraw_ballons()
						ballons.pop(i)

						score = score + ballon.points * bet
						break
				ViewMsg.setText('Balance ${}'.format(score))


if __name__ == "__main__":
	main()