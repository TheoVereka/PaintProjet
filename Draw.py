import tkinter as tk
import math

class DrawCanvas():
    def __init__(self, canvas, update_current):
        self.canvas = canvas
        self.update_current = update_current

        self.selectOption = 'Brush'

        self.line_new=[(100,100),(140,96),(200,110)]
        self.line_new=[]
        self.t=0

        self.x_old=-1
        self.y_old=-1
        self.x_older=-1
        self.y_older=-1

    def draw_circle(self,event, color='black'):
        if self.selectOption == 'Brush':
            if False:
                print('???')
                dist_modified=math.sqrt((event.x-self.x_old)**2+(event.y-self.y_old)**2)/50-2
                point_size=-dist_modified/math.sqrt(1+dist_modified**2)*5+7
                drawed_point=self.canvas.create_oval((event.x, event.y, event.x, event.y), outline='red',width=int(point_size))
                self.canvas.create_line([self.x_old,self.y_old,event.x,event.y], fill='blue', width=int(point_size))

            if self.x_older!=-1:
                print('!!!')
                x1,y1=self.x_older,self.y_older
                x2,y2=self.x_old,self.y_old
                x3,y3=event.x,event.y

                A=x1*y2-y1*x2+x2*y3-y2*x3+x3*y1-y3*x1
                A*=2
                B=-((x1**2+y1**2)*(y3-y2)+(x2**2+y2**2)*(y1-y3)+(x3**2+y3**2)*(y2-y1))
                C=(x1**2+y1**2)*(x3-x2)+(x2**2+y2**2)*(x1-x3)+(x3**2+y3**2)*(x2-x1)
                D=(x1**2+y1**2)*(x2*y3-x3*y2)+(x2**2+y2**2)*(x3*y1-x1*y3)+(x3**2+y3**2)*(x1*y2-x2*y1)
                if A==0:
                    if D>0: A=0.1
                    else: A=-0.1
                x_cen=int(B/A)
                y_cen=int(C/A)
                R=int(math.sqrt(B**2+C**2+2*A*D)/A)

                dist_modified=math.sqrt((x1-x3)**2+(y1-y3)**2)/50-2
                arc_size=-dist_modified/math.sqrt(1+dist_modified**2)*6+9
                cadre=(x_cen-R,y_cen-R,x_cen+R,y_cen+R)
                angle0=-math.atan2(y1+y2-2*y_cen,x1+x2-2*x_cen)/math.pi*180
                angle1=-math.atan2(y3+y2-2*y_cen,x3+x2-2*x_cen)/math.pi*180
                angle=angle1-angle0
                if angle>200: angle-=360
                if angle<-200: angle+=360
                if A!=0.1 and A!=-0.1:self.canvas.create_arc(cadre, start=angle0, extent=angle, outline=color, style="arc",width=arc_size)

            self.t+=1
            self.line_new.append((event.x,event.y))
            self.x_older=self.x_old
            self.y_older=self.y_old
            self.x_old=event.x
            self.y_old=event.y

            self.update_current()

    def update_new_line(self,event):
        if self.selectOption == 'Brush':
            #line2draw=self.fit_line(self.line_new)
            #self.canvas.create_line(100,100,110,106,120,110,fill="green",width=5)



            print(self.line_new)
            self.line_new=[]
            self.t=0
            self.x_older=-1
            self.y_older=-1
            self.x_old=-1
            self.y_old=-1

            self.update_current()

    #def fit_line(point):
    # Draw a line
    def start_line(self, event, color='black', size=2):
        if self.selectOption == 'Line':
            self.select_start = (event.x, event.y)
            self.line = self.canvas.create_line(event.x, event.y, event.x, event.y, fill=color, width=size)

            self.update_current()

    def draw_line(self, event):
        if self.selectOption == 'Line':
            self.select_end = (event.x, event.y)
            self.canvas.coords(self.line, self.select_start[0], self.select_start[1], event.x, event.y)

    # Draw rectangle
    def start_rect(self, event, color='black', size=2):
        if self.selectOption == 'Rectangle':
            self.select_start = (event.x, event.y)
            self.rect = self.canvas.create_rectangle(event.x, event.y, event.x, event.y, outline=color, width=size)

            self.update_current()

    def draw_rect(self, event):
        if self.selectOption == 'Rectangle':
            self.select_end = (event.x, event.y)
            self.canvas.coords(self.rect, self.select_start[0], self.select_start[1], event.x, event.y)

            self.update_current()

    def end_select(self, event):
        self.update_current()

    # Draw oval
    def start_oval(self, event, color='black', size=2):
        if self.selectOption == 'Oval':
            self.select_start = (event.x, event.y)
            self.oval = self.canvas.create_oval(event.x, event.y, event.x, event.y, outline=color, width=size)

            self.update_current()

    def draw_oval(self, event):
        if self.selectOption == 'Oval':
            self.select_end = (event.x, event.y)
            self.canvas.coords(self.oval, self.select_start[0], self.select_start[1], event.x, event.y)

            self.update_current()

"""
        for i in range(1,len(self.line_new)-1):

            x1,y1=self.line_new[i-1]
            x2,y2=self.line_new[i]
            x3,y3=self.line_new[i+1]

            A=x1*y2-y1*x2+x2*y3-y2*x3+x3*y1-y3*x1
            A*=2
            B=-((x1**2+y1**2)*(y3-y2)+(x2**2+y2**2)*(y1-y3)+(x3**2+y3**2)*(y2-y1))
            C=(x1**2+y1**2)*(x3-x2)+(x2**2+y2**2)*(x1-x3)+(x3**2+y3**2)*(x2-x1)
            D=(x1**2+y1**2)*(x2*y3-x3*y2)+(x2**2+y2**2)*(x3*y1-x1*y3)+(x3**2+y3**2)*(x1*y2-x2*y1)
            if A==0: 
                if D>0: A=0.1
                else: A=-0.1
            x_cen=int(B/A)
            y_cen=int(C/A)
            R=int(math.sqrt(B**2+C**2+2*A*D)/A)

            dist_modified=math.sqrt((x1-x3)**2+(y1-y3)**2)/50-2
            arc_size=-dist_modified/math.sqrt(1+dist_modified**2)*5+7
            cadre=(x_cen-R,y_cen-R,x_cen+R,y_cen+R)
            angle0=-math.atan2(y1+y2-2*y_cen,x1+x2-2*x_cen)/math.pi*180
            angle1=-math.atan2(y3+y2-2*y_cen,x3+x2-2*x_cen)/math.pi*180
            angle=angle1-angle0
            if angle>200: angle-=360
            if angle<-200: angle+=360
            if A!=0.1 and A!=-0.1:self.canvas.create_arc(cadre, start=angle0, extent=angle, style="arc",width=arc_size)
"""
