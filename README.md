# A backtracking GUI for CSE150 PA5 @ UCSD
Demo: https://vimeo.com/333172369

## HOT TO SET UP? 
### Step1
    - import it

        from GUI import GUI

    - create GUI object after Grid(), before solve(). Use it after solve()

        g = Grid(easy[0])
        ...
        gui = GUI(g,doku=9)     # 9 means this GUI is for sudoku, use 16 for hexadoku
        ...
        s.solve()
        ...
        gui.start()

### Step2
    - keep track of how self.sigma changes, by adding this line after each sigma change

        self.grid.hist.append(('a',(x,y),value))

    - 'a' means assignment. (you can also use 'c' to track consistency checking history)
    - (x,y) is a tuple, the coordinate in the Grid to be updated with a new value
    - value is what's assigned to (x,y)). (use None or -1 to indicate you're deleting assignment for (x,y))

## HOW TO USE? 

1. run the python file
2. Press <Space> or <Return>

## WHAT DOES THE COLOR RED MEAN? 

the more red the fonts means the more recent decision.
the more red the grids means the more times backtracked.

## HOW DOES IT WORK?
It keeps track of what happens to self.sigma during the backtrack by appending each change to a history list.

**Tkinter Reference: http://newcoder.io/gui/part-4/**
