"""TagBuilder Application
This application allow us to automate:
    1. Sitemap Builting.
    2. Pixel creating in Taboola, DV360, Minsights, Xandr, Google Ads, GA4 and Facebook.
    3. Tag creation in Google Tag Manager.
@author: Albeiro Jiménez López
@developed to: GroupM nexus at 2022
"""
import tkinter as tk
from tagGUI.tagGUI import FrameWork2D, tagFrontEnd

if __name__ == '__main__':
    root = tk.Tk()
    tagCalc = tagFrontEnd(root)
    tagCalc.mainloop()