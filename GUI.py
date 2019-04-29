from __future__ import print_function
from tkinter import Tk, Canvas, Frame, Button, BOTH, TOP, BOTTOM
import threading
from math import log2
from collections import defaultdict

MARGIN = 20
SIDE = 50
play_speed = 100 # in ms
smooth = True

class GUI(Frame):
    def __init__(self,grid,doku=9):
        self.WIDTH = self.HEIGHT = MARGIN * 2 + SIDE * doku
        self.root = Tk()
        self.doku = doku
        self.grid = grid
        self.root.geometry("%dx%d" % (self.WIDTH, self.HEIGHT + 40))
        self.game = [[] for i in range(doku)]
        self.trying = [[] for i in range(doku)]
        for coor in self.grid.spots:
            d = list(self.grid.domains[coor])
            self.trying[coor[0]-1].append(-1)
            if len(d) == 1:
                self.game[coor[0]-1].append(d[0])
            else:
                self.game[coor[0]-1].append(-1)
        Frame.__init__(self,width=self.WIDTH, height=self.HEIGHT, bg="", colormap="new")
        self.root.bind('<Return>',self.run)
        self.root.bind('<Right>',self.next_step)
        self.root.bind('<space>',self.step)
        self.row, self.col = 0, 0

        # set up the history for GUI
        self.grid.hist = []
        self.ptr_hist = 0
        self.assignments = {}
        self.backtrak_count = defaultdict(int)

    def start(self):
        self.initGUI()
        self.root.mainloop()

    def initGUI(self):
        self.root.title("GUIdoku")
        self.pause = True
        self.pack(fill=BOTH, expand=1)
        self.canvas = Canvas(self,width=self.WIDTH,height=self.HEIGHT)
        self.canvas.pack(fill=BOTH, side=TOP)
        run_button = Button(self,text="run",command=self.run)
        run_button.pack(fill=BOTH, side=BOTTOM)
        step_btn = Button(self,text="next",command=self.step,height = 300 ,width = 100)
        step_btn.pack( side=BOTTOM)
        self.draw_board()
        self.draw_grid()

    def run(self,event=None):
        self.pause = False
        self.next_step()

    def step(self, event=None):
        self.pause = True
        self.next_step()

    def next_step(self,event=None):
        '''interpret self.hist'''
        try:
            now = self.grid.hist[self.ptr_hist]
        except:
            self.pause = True
            print('done')
            return
        coord1,coord2 = now[1][0]-1,now[1][1]-1
        if now[0] == 'c': # checking consistency
            self.update_board(coord1,coord2,now[2])
        elif now[0] == 'b': # making assignment
            print(now)
            self.update_board(coord1,coord2,now[2],assign = True, backtrack = True)
        else:
            self.update_board(coord1,coord2,now[2],assign = True)
        self.ptr_hist+=1
        if smooth:    # # skip the duplicates
            while self.ptr_hist < len(self.grid.hist) and self.grid.hist[self.ptr_hist] == now:
                self.ptr_hist+=1
        # auto run
        if self.ptr_hist < len(self.grid.hist) and not self.pause:
            self.root.after(play_speed, self.next_step)

    def draw_grid(self):
        for i in range(self.doku+1):
            if i % int(log2(self.doku)) == 0:
                color = "black"
                w = 4
            else:
                color = "LightSteelBlue4"
                w = 1
            x0 = MARGIN + i * SIDE
            y0 = MARGIN
            x1 = MARGIN + i * SIDE
            y1 = self.HEIGHT - MARGIN
            self.canvas.create_line(x0, y0, x1, y1, fill=color,width=w,tags='grid')
            x0 = MARGIN
            y0 = MARGIN + i * SIDE
            x1 = self.WIDTH - MARGIN
            y1 = MARGIN + i * SIDE
            self.canvas.create_line(x0, y0, x1, y1, fill=color,width=w,tags='grid')

    def update_board(self,x,y,value,assign = False,backtrack = False):
        ''' put this on the board with tag '''
        if backtrack:
            if value:
                self.backtrak_count[(x,y)] += 1
            else:
                self.backtrak_count[(x,y)] = 0
            self.put_backtrack_color(x,y)
        else:
            # assignment
            if self.game[x][y] != -1:
                if assign:
                    del self.assignments[(x,y)]
            if assign:
                self.assignments[(x,y)] = len(self.assignments)
                self.game[x][y] = value
            else:
                # consistency
                self.assignments[(x,y)] = 0
                self.trying[x][y] = value
        self.highlight(x,y)
        self.udpate_board()

    def rgb_to_color(self,r,g,b):
        return "#%02x%02x%02x" % (r,g,b)
    def fade_red(self,i,j):
        color = 'black'
        if (i,j) in self.assignments:
            color_offset = (len(self.assignments) - self.assignments[(i,j)]) * 8
            gb = abs(60-color_offset//2)
            color_offset = 255 - color_offset
            if color_offset > 0:
                color = self.rgb_to_color(color_offset,gb,gb)
        return color

    def put_word(self,i,j):
        tag = "word"+str(i)+str(j)
        self.canvas.delete(tag)
        x = MARGIN + j * SIDE + SIDE / 2
        y = MARGIN + i * SIDE + SIDE / 2
        value = self.game[i][j]
        if value is not None and int(value) != -1:
            original = hex(int(value))[-1].upper()
            self.canvas.create_text(x, y, text=original,
                tags=tag,fill=self.fade_red(i,j),font=("Courier", 30))
        else:
            value = self.trying[i][j]
            if value is not None and int(value) != -1:
                original = hex(int(value))[-1].upper()
                self.canvas.create_text(x, y, text=original,
                    tags=tag, fill="snow3",font=("Courier", 30))

    def udpate_board(self):
        # draw the new board
        for i,j in self.assignments:
            self.put_word(i,j)

    def square_locs(self, i,j):
        x0 = MARGIN + j * SIDE
        y0 = MARGIN + i * SIDE
        x1 = x0 + SIDE
        y1 = y0 + SIDE
        return x0,y0,x1,y1

    def draw_board(self):
        # draw the default ones
        for i in range(self.doku):
            for j in range(self.doku):
                x = MARGIN + j * SIDE + SIDE / 2
                y = MARGIN + i * SIDE + SIDE / 2
                value = int(self.game[i][j])
                if value != -1:
                    x0,y0,x1,y1=self.square_locs(i,j)
                    self.canvas.create_rectangle(x0, y0, x1, y1, fill="grey90", tags="")
                    self.canvas.create_text(x, y,
                        text=hex(value)[-1].upper(),
                        tags="default"+str(i)+str(j), fill="black",font=("Courier", 30))


    def fade_pink(self,x,y):
        minus = self.backtrak_count[(x,y)] * (240//self.doku)
        return self.rgb_to_color(255, 241-minus, 241 - minus)

    def put_backtrack_color(self,y,x):
        print('putting color')
        tag = "btcolor"+str(x)+str(y)+"btcolor"
        self.canvas.delete(tag)
        x0,y0,x1,y1=self.square_locs(y,x)
        self.canvas.create_rectangle(x0+3, y0+3, x1-2, y1-2, fill=self.fade_pink(x,y), tags=tag, width =0 )

    def highlight(self,y,x):
        '''blank = True is to make it blank'''
        self.canvas.delete("highlight")
        x0,y0,x1,y1=self.square_locs(y,x)
        self.canvas.create_rectangle(x0, y0, x1, y1, outline="red", tags="highlight", width = 2)
