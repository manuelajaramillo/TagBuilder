import tkinter as tk
from tagGUI.tagGUI import FrameWork2D, tagFrontEnd

if __name__ == '__main__':
    root = tk.Tk()
    tagCalc = tagFrontEnd(root)
    tagCalc.mainloop()