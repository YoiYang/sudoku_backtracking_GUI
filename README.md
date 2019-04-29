# A backtracking GUI for CSE150 PA5 @ UCSD
Demo: https://vimeo.com/333172369

## HOT TO SET UP? 
### Step1
Import it at the top of sudoku.py
```
        from GUI import GUI
```
Create GUI object after creating the Grid() object and before solve(). Start it after solve()
```
        g = Grid(easy[0])
        ...
        gui = GUI(g,doku=9)     # 9 means this GUI is for sudoku, use 16 for hexadoku
        ...
        s.solve()
        ...
        gui.start()
```
### Step2
Let GUI keep track of all changes, by adding the following line at where self.sigma changes
```
        self.grid.hist.append(('a',(x,y),value))

        # 'a' means assignment. (you can also use 'c' to track consistency checking history)
        # (x,y) is a tuple, the coordinate in the Grid to be updated with a new value
        # value is what's assigned to (x,y)). (use None or -1 to indicate you're deleting assignment for (x,y))
```
## HOW TO USE? 

1. python sudoku.py
2. Press SPACE (to see the next step) or RETURN (to speed up)

## WHAT DOES THE COLOR RED MEAN? 
The redder on the number means the more recent this choice is made.
The redder on the grids means the more backtracking have happened at this grid.

## HOW DOES IT WORK?
It keeps track of what happens to self.sigma during the backtrack by appending each change to a history list.

**Tkinter Reference: http://newcoder.io/gui/part-4/**
