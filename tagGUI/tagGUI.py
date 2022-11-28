import tkinter as tk
from tkinter import filedialog, messagebox, ttk, simpledialog
from threading import Thread
import time, sys, subprocess
import json
import re

from os import closerange, path as p
from urllib.parse import urlparse
from tkinter import font
from tkinter.constants import OFF

from tagModules.GTM import AudienceTag, BasicVariable, ButtonTag, CustomTemple, GA4Event, GA4Setting, GTM, ClickTrigger, PageviewTrigger, ScrollTrigger, TimerTrigger
from tagModules.urlExtractor import urlDomains as webDOM
from tagModules.tagBuilderTools import Naming, stringMethods as sM
from tagModules.pixelBot import pixelBot
from tagModules.handleFile import xlsxFile
from googleapiclient.errors import HttpError

MENU_DEFINITION = (
            'File- &New/Ctrl+N/self.newFile, Save/Ctrl+S/self.save_file, SaveAs/Ctrl+Shift+S/self.save_as, sep, Exit/Ctrl+Q/self.askQuit',
            'Edit- Settings/Ctrl+Z/self.setting, sep, Advanced Settings/Alt+F5/self.advancedSetting',
            'View- SiteMap Builder//self.show_siteMapTab, Pixel Creator//self.show_PixelTab, GTM Integrator//self.show_GTMTab',
            'Help- Documentation/F2/self.documentation, About/F1/self.aboutTagBuilder'
        )

LOGIN_PAGES     = (
    'https://invest.xandr.com/', 
    'https://displayvideo.google.com/',
    'https://ads.taboola.com/',
    'https://amerminsights.mplatform.com/',
    'https://tagmanager.google.com/',
    'https://business.facebook.com/latest/home'
)

TABS_DEFINITION = (
    'SiteMap',
    'Pixels',
    'GTM',
    'CAPI'
    )

SPECIAL_CELLS = (
    'C31', 'D31', 'G31'
)

COLUMNS = (
    'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N'
)

PLATFORMS_ADS = (
    'programmatic', 'tik-tok', 'twitter', 'ga4', 'ads', 'meta'
)

PLATFORMS_BASE = (
    'Xandr Seg', 'Xandr Conv', 'DV360', 'Taboola Seg', 'Taboola Conv', 'Minsights'
)

PLATFORM_COLORS = {
    'programmatic':'DDDDDD', 'tik-tok':'F8DAE9', 'twitter':'B9D6F3', 'ga4':'F1E8D9', 'ads':'F4C2D7', 'meta':'A1C9F1', 'microconvertion':'F4C2D7'
}

TYPE_MS = (
    'Branding', 'Conversions', 'E-commerce', 'Traffic'
)

PIXEL_SETTING_COLUMNS = [4, 14]

MONTHS          = [
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
]

PLATFORM_CREDENTIALS = 'resources/credentials/platform_credentials.json'

PROGRAM_NAME = 'TagBuilder'

class FrameWork2D(ttk.Frame):
    """This class implement the base structure of TagBuilder GUI.

    Args:
        ttk (Frame): Canvas from ttk.Frame where we build the TagBuilder Interfaz.
    """    
    def __init__(self, root, *args, **kwargs):
        """Contructor method that initializes and implement the GUI elements in TagBuilder.

        Args:
            root (tk.Tk()): Main Window of TagBuilder Interface.
        """        
        super().__init__(*args, **kwargs)
        self.root = root
        self.tabPages = ttk.Notebook(self.root)
        self.build_menu(MENU_DEFINITION)
        self.build_tabs(TABS_DEFINITION)
        self.sitemapTab = True
        self.pixelTab   = False
        self.GTMTab     = False
        self.CAPITab    = False
        self.set_CCS()
        
    def set_CCS(self):
        """This method defines the main style features of TagBuilder GUI elements.
        """        
        self.root.title(PROGRAM_NAME)
        self.root.iconbitmap('resources/xaxis32x32.ico')
        self.root.protocol("WM_DELETE_WINDOW", self.askQuit)
        self.root.geometry("795x415+300+100")
        self.root.resizable(False,False)
        self.root.configure(bg='white')
        style = ttk.Style()
        if 'xpnative' in style.theme_names():
            style.theme_use('xpnative')
        elif 'vista' in style.theme_names():
            style.theme_use('vista')
        elif 'clam' in style.theme_names():
            style.theme_use('clam')
        else:
            style.theme_use('default')
        style.configure('.', padding=3, font=('Arial',9,'bold'))
    
    def build_menu(self, menu_definitions):
        """This method implement the Menu building in TagBuilder main Interface.

        Args:
            menu_definitions (tuple): Array tuple with the definitions and settings to implement the main menu in TagBuilder.
        """        
        menu_bar = tk.Menu(self.root)
        for definition in menu_definitions:
            menu = tk.Menu(menu_bar, tearoff=0)
            top_level_menu, pull_down_menus = definition.split('-')
            menu_items = map(str.strip, pull_down_menus.split(','))
            for item in menu_items:
                self._add_menu_command(menu, item)
            menu_bar.add_cascade(label=top_level_menu, menu=menu)
        self.root.config(menu=menu_bar)

    def _add_menu_command(self, menu, item):
        """This method associative the menu option with the right method in TagBuilder

        Args:
            menu (tk.Menu): Menu object as File, Edit, View...
            item (string) : String format with the settings require to implement the diferent option of each Menu.
        """        
        if item == 'sep':
            menu.add_separator()
        else:
            menu_label, accelrator_key, command_callback = item.split('/')
            try:
                underline = menu_label.index('&')
                menu_label = menu_label.replace('&', '', 1)
            except ValueError:
                underline = None
            menu.add_command(label=menu_label, underline=underline, accelerator=accelrator_key, command=eval(command_callback))
            type
            
    # Array of Frames that is in the Notebook: Array of tabs.       
    def build_tabs(self, tabs_definition):
        """This method implement the diferent tabs of each functionality in TagBuilder
        as SiteMap, Pixel, and so on.

        Args:
            tabs_definition (tuple): Array tuple with the name of each functionality in TagBuilder.
        """        
        self.tabs = [] # Frame
        for definition in tabs_definition:
            self.tabs.append(ttk.Frame(self.tabPages))
            self.tabPages.add(self.tabs[-1], text = definition)
        for index in range(1,len(tabs_definition)):
            self.tabPages.hide(index)
        self.tabPages.pack(expand=1, fill="both")
    
    def newFile(self):
        pass
    
    def save_file(self):
        pass

    def save_as(self):
        pass
    
    def askQuit(self):
        if messagebox.askokcancel("Closing TagBuilder", "Are you sure to close TagBuilder?\n\nPress Ok or Cancel."):
            self.exitCalcTag()

    def exitCalcTag(self):
        self.root.quit()
        self.root.destroy()
        exit()
    
    def setting(self):
        pass
    
    def advancedSetting(self):
        pass
    
    def show_siteMapTab(self):              
        self.sitemapTab = not self.sitemapTab
        if self.sitemapTab:
            self.tabPages.add(self.tabs[0])
            self.tabPages.select(0)
        else:
            self.tabPages.hide(0)
    
    def show_PixelTab(self):
        self.pixelTab = not self.pixelTab
        if self.pixelTab:
            self.tabPages.add(self.tabs[1])
            self.tabPages.select(1)
        else:
            self.tabPages.hide(1)
            
    def show_GTMTab(self):
        self.GTMTab = not self.GTMTab
        if self.GTMTab:
            self.tabPages.add(self.tabs[2])
            self.tabPages.select(2)
        else:
            self.tabPages.hide(2)
    
    def show_CAPITab(self):
        self.CAPITab = not self.CAPITab
        if self.CAPITab:
            self.tabPages.add(self.tabs[3])
            self.tabPages.select(3)
        else:
            self.tabPages.hide(3)
    
    def documentation(self):
        subprocess.Popen(p.abspath('resources/documentation/TagBuilder_Manual.pdf'), shell=True)
    
    def aboutTagBuilder(self):
        pass
    
class tagFrontEnd(FrameWork2D):
    """This Class implement the creation of diferents elements of TagBuilder GUI

    Args:
        FrameWork2D (ttk.Frame): Framework base that TagBuilder application uses to build its interfaz.
    """    
    #def __init__(self, root, webDOM, xlsxFile, pixelBot, *args, **kwargs):
    def __init__(self, root, *args, **kwargs):
        super().__init__(root, *args, **kwargs)
        self.webDOM        = webDOM('https://www.xaxis.com/')
        self.xlsxFile      = xlsxFile()
        self.pixelBot      = pixelBot()
        self.gtmService    = None
        self.gtmSharing    = True
        self.gtmAccounts   = []
        self.gtmContainers = []
        self.gtmWorkspaces = []
        self.container     = {}
        self.workspace     = {}
        self.arrayPixels   = []
        self.xandrSeg      = []
        self.xandrConv     = []
        self.DV360         = []
        self.minsights     = []
        self.taboolaSeg    = []
        self.taboolaConv   = []
        self.gtmTags       = []
        self.gtmVariables  = []
        self.platformList  = []
        self.platformAdsList   = []
        self.typeContainer = tk.StringVar()
        self.pathTR        = tk.StringVar()  
        self.directoryTR   = tk.StringVar()
        self.directoryTRF  = tk.StringVar()
        self.urlAdvertiser = tk.StringVar()
        self.advertiser    = tk.StringVar()
        self.advertiser_   = tk.StringVar()
        self.advertiserId  = tk.StringVar()
        self.fixedPath     = tk.StringVar()
        self.scrollDeep    = tk.StringVar()
        self.timerLast     = tk.StringVar()
        self.scheme        = tk.StringVar()
        self.builtBy       = tk.StringVar()
        self.searchXML     = tk.BooleanVar()
        self.mss           = tk.BooleanVar()
        self.show          = tk.BooleanVar()
        self.show_         = tk.BooleanVar()
        self.marionette    = tk.BooleanVar()
        self.seleniumDelay = tk.IntVar()
        self.waitings      = tk.IntVar()
        self.users         = [tk.StringVar()]
        self.passwords     = [tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()]
        self.other_passwds = [tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar(), tk.StringVar()]
        self.maxCategory   = tk.IntVar()
        self.minSizeWord   = tk.IntVar()
        self.maxLandings   = tk.IntVar()
        self.viewProgress  = tk.IntVar()
        self.pixelProgress = tk.IntVar()
        self.tagProgress   = tk.IntVar()
        self.GTM_ID        = tk.StringVar()
        self.createAttr()
        self._init_params()
        self._set_credentials_threaded()
        
    def createAttr(self):
        for platform in PLATFORMS_ADS:
            self.__setattr__('platform%s'%platform.capitalize(), tk.BooleanVar())
            self.__getattribute__('platform%s'%platform.capitalize()).set(False)
        self.__getattribute__('platform%s'%PLATFORMS_ADS[0].capitalize()).set(True)

    def _init_params(self):
        self.typeContainer.set('')
        self.pathTR.set(self.xlsxFile.PATH)
        self.directoryTR.set("")
        self.directoryTRF.set("")
        self.urlAdvertiser.set(self.webDOM.url_target)
        self.advertiser.set(self.xlsxFile.readCell('C13'))
        self.advertiser_.set('')
        self.advertiserId.set(self.xlsxFile.readCell('C14'))
        self.fixedPath.set('/')
        self.maxCategory.set(15)
        self.platformAdsList.append('Programmatic')
        self.webDOM.setMaxCategories(self.maxCategory.get())
        self.minSizeWord.set(3)
        self.webDOM.setSizeWord(self.minSizeWord.get())
        self.maxLandings.set(50)
        self.webDOM.setMaxLandings(self.maxLandings.get())
        self.searchXML.set(False)
        #self.programmatic.set(True)
        self.show.set(False)
        self.show_.set(False)
        self.marionette.set(False)
        self.mss.set(False)
        self.webDOM.setSearchXML(self.searchXML.get())
        self.viewProgress.set(0)
        self.pixelProgress.set(0)
        self.tagProgress.set(0)
        self.seleniumDelay.set(2)
        self.waitings.set(6)
        self.scrollDeep.set('50')
        self.timerLast.set('30')
        self.scheme.set('https')
        self.builtBy.set('path')
        self.GTM_ID.set(self.xlsxFile.readCell('C23'))
        self.codeVerify = None
        self.closeTopW  = False
        self.users[0].set("")
        self.pixelBot.setSeleniumDelay(self.seleniumDelay.get())
        self.pixelBot.setWaitings(self.waitings.get())
        for platform in PLATFORMS_BASE:
            self.platformList.append(platform)
        for passwd in self.passwords:
            passwd.set("")
        for passwd in self.other_passwds:
            passwd.set("")
        self.setWindow = tk.Toplevel()
        self.setWindow.destroy()
        for index in range(len(TABS_DEFINITION)):
            self.buildTab(index)
            
    def get_gtm_id(self):
        self.xlsxFile.setSheet('Home')
        return self.xlsxFile.readCell('C23')
    
    def get_homepage(self):
        self.xlsxFile.setSheet('Home')
        return self.xlsxFile.readCell('F31')
    
    def _set_credentials_threaded(self):
        """This function allows to get the DSP's credentials without
            blocking the main GUI at the start the program TagBuilder.

        Returns:
            None: None
        """
        thread = Thread(target=self._set_credentials)
        thread.start()
    
    """
    This function initialize the credentials of the DSP Platforms.
        Return:
            None: None
    """
    def _set_credentials(self):
        try:
            with open(PLATFORM_CREDENTIALS) as credentials_file:
                credentials = json.load(credentials_file)
                self.users[0].set(credentials['user'])
                for passwd, password in zip(credentials['passwords'].values(), self.passwords):
                    password.set(passwd)
                for passwd, password in zip(credentials['otherPasswords'].values(), self.other_passwds):
                    password.set(passwd)
        except FileNotFoundError:
            while not self.existAllCredentials() or self.setWindow.winfo_exists():
                if not self.setWindow.winfo_exists():
                    self.settingWindow() 
        except:
            pass 

    def existAllCredentials(self):
        if self.users[0].get() == "":
            return False
        for passwd in self.passwords:
            if passwd.get() == "":
                return False
        else:
            return True

    """
    This function valid if a string is or not a URL valid.
        Return:
            Boolean: True or False
    """
    def validURL(self, url):
        url_ = re.compile(r"^(https?:\/\/)?([\da-z\.-]+)\.([a-z\.]{2,6})([\/\w \.-]*)*\/?$")
        if url_.search(url) == None:
            return False
        else:
            return True
    
    """
    This function valid if a advertiser Name field is valid or not.
        Return:
            Boolean: True or False
    """   
    def validAdvertiserName(self):
        if self.advertiser.get() == '' or self.advertiser.get().casefold() == 'none' or self.advertiser.get() == None:
            return False
        else:
            return True

    """
    This function valid if a advertiser ID field is valid or not.
        Return:
            Boolean: True or False
    """    
    def validAdvertiserID(self):
        if self.advertiserId.get().isdigit():
            return True
        else:
            return False
   
    """
    This function valid if a Container ID field is valid or not.
        Return:
            Boolean: True or False
    """     
    def validGTMID(self):
        if self.GTM_ID.get() == '' or self.GTM_ID.get() == None or self.GTM_ID.get().casefold() == 'None' or not re.findall(r'^GTM-\w{7}$', self.GTM_ID.get()):
            return False
        else:
            return True

    # Function to build diferents tabs: Sitemap and GTM
    def buildTab(self, indexTab):
        if   indexTab == 0:
            self.createParameterSection(indexTab)
            self.createDataSection(indexTab)
        elif indexTab == 1:
            self.createParameterSection(indexTab)
            self.createPixelSection(indexTab)
        elif indexTab == 2:
            self.createParameterSection(indexTab)
            self.createGTMSection(indexTab)
        elif indexTab == 3:
            self.createParameterSection(indexTab)
            self.createCAPISection(indexTab)
        
    def loadTemple(self):
        self.pathTR.set(filedialog.askopenfilename(title = 'Select a Tagging Request Temple', filetypes=[('XLSX', '*.xlsx *.XLSX')]))
        self.xlsxFile.setPATH(self.pathTR.get())
        self.xlsxFile.setBook()
        self.xlsxFile.setSheet()
        self.advertiser.set(self.xlsxFile.readCell('C13'))
        
    def loadTR(self):
        self.btn_create.configure(state='disable')
        self.btn_save_pixels.configure(state='disable')
        tempDir = filedialog.askopenfilename(title = 'Select a Tagging Request Temple', filetypes=[('XLSX', '*.xlsx *.XLSX')])
        try:
            if tempDir.split('/')[-1].startswith('TagReq_') and (tempDir.split('/')[-1][-12:-9] in MONTHS) and tempDir.split('/')[-1][-9:-5].isnumeric():
                self.directoryTR.set(tempDir)
                self.xlsxFile.setPATH(self.directoryTR.get())
                self.xlsxFile.setBook()
                self.xlsxFile.setSheet('Home')
                self.advertiser_.set(self.xlsxFile.readCell('C13'))
                self.advertiserId.set(self.xlsxFile.readCell('C14'))
                self.btn_pixels.configure(state='active')
            else:
                self.lanchPopUps('Invalid File', 'You must choice a valid file!', 'Press "Ok" to exit.')
        except:
            self.lanchPopUps('Invalid File', 'You must choice a valid file!', 'Press "Ok" to exit.')
            
    def loadTRFinal(self):
        tempDir = filedialog.askopenfilename(title = 'Select a Tagging Request Temple', filetypes=[('XLSX', '*.xlsx *.XLSX')])
        try:
            if tempDir.split('/')[-1].startswith('TagReqFinal_') and (tempDir.split('/')[-1][-12:-9] in MONTHS) and tempDir.split('/')[-1][-9:-5].isnumeric():
                self.disableGTMBTN()
                self.directoryTRF.set(tempDir)
                self.xlsxFile.setPATH(self.directoryTRF.get())
                self.xlsxFile.setBook()
                self.xlsxFile.setSheet('Home')
                self.btn_loadTags.configure(state='active')
            else:
                print(tempDir)
                self.lanchPopUps('Invalid File', 'You must choice a valid file!', 'Press "Ok" to exit.')
        except:
            print('Queeeeeeeee?')
            print(sys.exc_info())
            self.lanchPopUps('Invalid File', 'You must choice a valid file!', 'Press "Ok" to exit.')
            
    def disableGTMBTN(self):
        self.btn_loadTags.configure(state='disable')
        self.btn_gtmConnect.configure(state='disable')
        self.btn_tagging.configure(state='disable')
        #self.btn_save_tags.configure(state='disable')
    
    def setTemple(self):
        self.xlsxFile.setPATH(self.pathTR.get())
        self.xlsxFile.setBook()
        self.xlsxFile.setSheet()
        
    def loadAdvertiser(self):
        pass
    
    def createParameterSection(self, indexTab):
        """This GUI method implement the diferents parameters sections in each funcionality of TagBuilder. 

        Args:
            indexTab (int): ID that identify each functionality in TagBuilder. 
                            0 - Sitemap Builder.
                            1 - Pixel Creator.
                            2 - GTM Integrator.
                            3 - CAPI INtegrator.
        """
        #Parameter Section
        parameters_label_frame = ttk.LabelFrame(self.tabs[indexTab], text='Parameters', width=780, height=100)
        parameters_frame       = ttk.Frame(parameters_label_frame)
        parameters_label_frame.grid(column = 0, row=0)
        
        parameters_label_frame.grid_propagate(0)
        parameters_frame.grid(column = 0, row=0)
        
        if indexTab == 0:
            ttk.Label(parameters_frame, text="URL Target: ").grid(column=0, row=0, sticky=tk.W)
            tk.Entry(parameters_frame, width=30, textvariable = self.urlAdvertiser, font=('Arial',8,'italic'), relief=tk.SUNKEN, borderwidth=2).grid(column=1, row=0, sticky=tk.W)
            ttk.Label(parameters_frame, text="Advertiser: ").grid(column=2, row=0, sticky=tk.W)
            tk.Entry(parameters_frame, textvariable = self.advertiser, font=('Arial',8,'italic'), relief=tk.SUNKEN, borderwidth=2).grid(column=3, row=0, sticky=tk.W)
            ttk.Label(parameters_frame, text='Platform Ads: ').grid(column=4, row=0)
            self.listPlatformAds = ttk.Combobox(parameters_frame, state='readonly', font=('Arial',8,'italic'))
            self.listPlatformAds['values'] = self.platformAdsList
            self.listPlatformAds.set('Programmatic')
            self.listPlatformAds.grid(column=5, row=0)
            
            ttk.Label(parameters_frame, text="Container ID: ").grid(column=0, row=1, sticky=tk.W)
            tk.Entry(parameters_frame, width=30, textvariable = self.GTM_ID, font=('Arial',8,'italic'), relief=tk.SUNKEN, borderwidth=2).grid(column=1, row=1, sticky=tk.W)
            ttk.Label(parameters_frame, text="Progress: ").grid(column=2, row=1, sticky=tk.W)
            self.progressbar = ttk.Progressbar(parameters_frame, variable=self.viewProgress, orient = tk.HORIZONTAL, length=125, maximum=100)
            self.progressbar.grid(column=3, row=1, sticky=tk.W)
            ttk.Label(parameters_frame, text="Only HomePV: ").grid(column=4, row=1, sticky=tk.W)
            ttk.Checkbutton(parameters_frame, command=self.set_search, variable=self.searchXML, onvalue=False, offvalue=True).grid(column=5, row=1)
            
            ttk.Label(parameters_frame, text="Fixed Paths: ").grid(column=0, row=2, sticky=tk.W)
            self.fixedPaths = ttk.Spinbox(parameters_frame, from_=0, to=3, command=self.set_fixedPaths, wrap=True, width=14, state='readonly')
            self.fixedPaths.set(0)
            self.fixedPaths.grid(column=1, row=2, sticky=tk.W)
            ttk.Label(parameters_frame, text="Paths: ").grid(column=2, row=2, sticky=tk.W)
            tk.Entry(parameters_frame, textvariable = self.fixedPath, font=('Arial',8,'italic'), relief=tk.SUNKEN, borderwidth=2, state='readonly').grid(column=3, row=2, sticky=tk.W)
        elif indexTab == 1:
            ttk.Label(parameters_frame, text="T. Request File: ", style = 'BW.TLabel').grid(column=0, row=0)
            tk.Entry(parameters_frame, width=75, textvariable = self.directoryTR, font=('Arial',8,'italic'), relief=tk.SUNKEN, borderwidth=2).grid(column=1, row=0, columnspan=4)
            ttk.Button(parameters_frame, text='...', command=self.loadTR, width=2).grid(column=5, row=0, sticky=tk.NW)  
            
            ttk.Label(parameters_frame, text='Advertiser: ').grid(column=0, row=1, sticky=tk.W) 
            tk.Entry(parameters_frame, textvariable = self.advertiser_, font=('Arial',8,'italic'), relief=tk.SUNKEN, borderwidth=2).grid(column=1, row=1, sticky=tk.W)     
            ttk.Label(parameters_frame, text= 'Advertiser ID: ').grid(column=2, row=1, sticky=tk.W)
            tk.Entry(parameters_frame, textvariable=self.advertiserId, font=('Arial',8,'italic'), relief=tk.SUNKEN, borderwidth=2).grid(column=3, row=1, sticky=tk.W) 
            ttk.Label(parameters_frame, text="Progress:").grid(column=4, row=1, sticky=tk.W)
            ttk.Progressbar(parameters_frame, variable=self.pixelProgress, orient = tk.HORIZONTAL, length=125, maximum=100).grid(column=5, row=1, sticky=tk.W)
            ttk.Label(parameters_frame, text='Agency: ').grid(column=0, row=2, sticky=tk.W)
            self.agencies = ttk.Combobox(parameters_frame, state='readonly', font=('Arial',8,'italic'))
            self.agencies['values'] = ['Xaxis', 'Ford', 'Colgate']
            self.agencies.set('Xaxis')
            self.agencies.grid(column=1, row=2)
            ttk.Label(parameters_frame, text='Market: ').grid(column=2, row=2, sticky=tk.W)
            self.countries = ttk.Combobox(parameters_frame, state='readonly', font=('Arial',8,'italic'))
            self.countries['values'] = ['Argentina', 'Brazil', 'Chile', 'Colombia', 'Ecuador', 'Mexico', 'Miami', 'Peru', 'Puerto Rico', 'Uruguay', 'US', 'Venezuela']
            self.countries.set('Colombia')
            self.countries.grid(column=3, row=2)
            ttk.Label(parameters_frame, text="Platform: ").grid(column=4, row=2, sticky=tk.W)
            self.platforms = ttk.Combobox(parameters_frame, state='readonly', font=('Arial',8,'italic'))
            self.platforms['values'] = ['Xandr Seg', 'Xandr Conv', 'DV360', 'Taboola Seg', 'Taboola Conv', 'Minsights']
            self.platforms.set('Xandr Seg')
            self.platforms.grid(column=5, row=2)
        elif indexTab == 2:
            ttk.Label(parameters_frame, text="T.R Final File: ", style = 'BW.TLabel').grid(column=0, row=0)
            tk.Entry(parameters_frame, width=75, textvariable = self.directoryTRF, font=('Arial',8,'italic'), relief=tk.SUNKEN, borderwidth=2).grid(column=1, row=0, columnspan=4)
            ttk.Button(parameters_frame, text='...', command=self.loadTRFinal, width=2).grid(column=5, row=0, sticky=tk.NW) 
            
            ttk.Label(parameters_frame, text='Client Account: ').grid(column=0, row=1, sticky=tk.W) 
            self.listAccounts = ttk.Combobox(parameters_frame, state='readonly', font=('Arial',8,'italic'))
            self.listAccounts['values'] = self.gtmAccounts
            self.listAccounts.bind("<<ComboboxSelected>>", self.set_gtmAccount_threaded)
            self.listAccounts.grid(column=1, row=1)
            ttk.Label(parameters_frame, text= 'Container ID: ').grid(column=2, row=1, sticky=tk.W)
            self.listContainers = ttk.Combobox(parameters_frame, state='readonly', font=('Arial',8,'italic'))
            self.listContainers['values'] = self.gtmContainers
            self.listContainers.bind("<<ComboboxSelected>>", self.set_gtmContainer_threaded)
            self.listContainers.grid(column=3, row=1)
            ttk.Label(parameters_frame, text="Workspace: ").grid(column=4, row=1, sticky=tk.W)
            self.listWorkspaces = ttk.Combobox(parameters_frame, state='readonly', font=('Arial',8,'italic'))
            self.listWorkspaces['values'] = self.gtmWorkspaces
            self.listWorkspaces.bind("<<ComboboxSelected>>", self.set_gtmWorkspace_threaded)
            self.listWorkspaces.grid(column=5, row=1, sticky=tk.W)
            ttk.Label(parameters_frame, text="Progress:").grid(column=0, row=2, sticky=tk.W)
            ttk.Progressbar(parameters_frame, variable=self.tagProgress, orient = tk.HORIZONTAL, length=125, maximum=100).grid(column=1, row=2, sticky=tk.W)
        elif indexTab == 3:
            pass  
         
    def createDataSection(self, indexTab):
        data_label_frame  = ttk.LabelFrame(self.tabs[indexTab], text='Data', width=780, height=295)
        data_label_frame.grid(column = 0, row=1)
        data_label_frame.grid_propagate(0)
        # Frame's child data_label_frame
        self.data_table_frame  = ttk.Frame(data_label_frame, borderwidth=3, relief='ridge', width=780, height=230)
        self.data_table_frame.grid(column = 0, row=0)
        self.data_table_frame.grid_propagate(0)
        # Frame's child data_label_frame
        data_button_frame = ttk.Frame(data_label_frame)
        data_button_frame.grid(column = 0, row=1)
        
        self.btn_find = ttk.Button(data_button_frame, text='Find', command = self.find_threaded)
        self.btn_find.grid(column=0, row=0)

        self.btn_stop = ttk.Button(data_button_frame, text='Stop', command = self.stopSearch, state = 'disable')
        self.btn_stop.grid(column=1, row=0)

        self.btn_sections = ttk.Button(data_button_frame, text='Sections', command = self.draw_threaded, state = 'disable')
        self.btn_sections.grid(column=2, row=0)
        self.btn_save = ttk.Button(data_button_frame, text='Save', command = self.save_threaded, state = 'disable')
        self.btn_save.grid(column=3, row=0)
        
        ttk.Button(data_button_frame, text='exit', command = self.askQuit).grid(column=4, row=0)
        
        self.createTableData()
        
    """
        This method implement de Pixels Area in the Pixels Tab.
        Make up by two Frames: Table to show Pixels details and
        Section we allocate the control buttons.
        Return:
            None:   None
    """ 
    def createPixelSection(self, indexTab):
        pixel_label_frame  = ttk.LabelFrame(self.tabs[indexTab], text='Pixels', width=780, height=295)
        pixel_label_frame.grid(column = 0, row=1)
        pixel_label_frame.grid_propagate(0)
        
        self.pixel_table_frame  = ttk.Frame(pixel_label_frame, borderwidth=3, relief='ridge', width=780, height=230)
        self.pixel_table_frame.grid(column = 0, row=0)
        self.pixel_table_frame.grid_propagate(0)
        # Frame's child data_label_frame
        pixel_button_frame = ttk.Frame(pixel_label_frame)
        pixel_button_frame.grid(column = 0, row=1)

        self.btn_pixels = ttk.Button(pixel_button_frame, text='Pixels', command = self.pixels_threaded, state = 'disable')
        self.btn_pixels.grid(column=0, row=0)
        
        self.btn_create = ttk.Button(pixel_button_frame, text='Create', command = self.createPixels_threaded, state = 'disable')
        self.btn_create.grid(column=1, row=0)
        
        self.btn_save_pixels = ttk.Button(pixel_button_frame, text='Save', command = self.savePixels_threaded, state = 'disable')
        self.btn_save_pixels.grid(column=2, row=0)
        
        ttk.Button(pixel_button_frame, text='exit', command = self.askQuit).grid(column=3, row=0)
        self.createTableData(1)
        
    def createGTMSection(self, indexTab):
        GTM_label_frame  = ttk.LabelFrame(self.tabs[indexTab], text='Tags', width=780, height=295)
        GTM_label_frame.grid(column = 0, row=1)
        GTM_label_frame.grid_propagate(0)
        
        self.GTM_table_frame  = ttk.Frame(GTM_label_frame, borderwidth=3, relief='ridge', width=780, height=230)
        self.GTM_table_frame.grid(column = 0, row=0)
        self.GTM_table_frame.grid_propagate(0)
        # Frame's child data_label_frame
        GTM_button_frame = ttk.Frame(GTM_label_frame)
        GTM_button_frame.grid(column = 0, row=1)
        
        self.btn_loadTags = ttk.Button(GTM_button_frame, text='Load', command = self.tags_threaded, state = 'disable')
        self.btn_loadTags.grid(column=0, row=0)
        
        self.btn_gtmConnect = ttk.Button(GTM_button_frame, text='Connect', command = self.gtmConnect_threaded, state = 'disable')
        self.btn_gtmConnect.grid(column=1, row=0)
        
        self.btn_tagging = ttk.Button(GTM_button_frame, text='Create', command = self.createTags_threaded, state = 'disable')
        self.btn_tagging.grid(column=2, row=0)
        
        #self.btn_save_tags = ttk.Button(GTM_button_frame, text='Save', command = self.saveTags_threaded, state = 'disable')
        #self.btn_save_tags.grid(column=3, row=0)
        
        ttk.Button(GTM_button_frame, text='exit', command = self.askQuit).grid(column=4, row=0)
        self.createTableData(2)
    
    def createCAPISection(self, indexTab):
        CAPI_label_frame  = ttk.LabelFrame(self.tabs[indexTab], text='Events', width=780, height=295)
        CAPI_label_frame.grid(column = 0, row=1)
        CAPI_label_frame.grid_propagate(0)
        
        self.CAPI_table_frame  = ttk.Frame(CAPI_label_frame, borderwidth=3, relief='ridge', width=780, height=230)
        self.CAPI_table_frame.grid(column = 0, row=0)
        self.CAPI_table_frame.grid_propagate(0)
        # Frame's child data_label_frame
        CAPI_button_frame = ttk.Frame(CAPI_label_frame)
        CAPI_button_frame.grid(column = 0, row=1)

        self.btn_load = ttk.Button(CAPI_button_frame, text='Events', command = self.events_threaded)
        self.btn_load.grid(column=0, row=0)
        
        self.btn_createEvents = ttk.Button(CAPI_button_frame, text='Create', command = self.createPixels_threaded, state = 'disable')
        self.btn_createEvents.grid(column=1, row=0)
        
        self.btn_save_events = ttk.Button(CAPI_button_frame, text='Save', command = self.savePixels_threaded, state = 'disable')
        self.btn_save_events.grid(column=2, row=0)
        
        ttk.Button(CAPI_button_frame, text='exit', command = self.askQuit).grid(column=3, row=0)
        self.createTableData(3)
    
    """This method implement a visualization field of data in the diferent funcionalities as Sitemap, Pixels, GTM and CAPI.
       Parameters:
            indexTab:   Index that corresponds to the funcionality in each that want to implement the visualization field.
       Return:
            None:   None
    """    
    def createTableData(self, indexTab=0):
        if indexTab == 0:
            dataFrame  = ttk.Frame(self.data_table_frame, width=754.5, height=210)
            dataFrame.grid(column=0, row=0, sticky='NESW')
            dataFrame.grid_propagate(0)
            self.dataTable = ttk.Treeview(dataFrame, columns=['Landing', 'Path'], selectmode='extended')
            self.dataTable.heading('#0', text='Category', anchor='w')
            self.dataTable.heading('Landing', text='Landing', anchor='w')
            self.dataTable.heading('Path', text='Path', anchor='w')
            self.dataTable.column('#0', stretch=True, width=200)
            self.dataTable.column('Landing', stretch=True, width=450)
            self.dataTable.column('Path', stretch=True, width=150)
            self.dataTable.bind("<KeyPress-Delete>",self.deleteBranch)
            self.dataTable.grid(column=0, row=0, sticky='NESW')
            scrollbar = ttk.Scrollbar(self.data_table_frame, orient = 'vertical', command=self.dataTable.yview)
            self.dataTable.configure(yscrollcommand=scrollbar.set)
            scrollbar.grid(column=1, row=0, sticky = 'NS', in_=self.data_table_frame)
            
            scrollbarx = ttk.Scrollbar(self.data_table_frame, orient = 'horizontal', command=self.dataTable.xview)
            self.dataTable.configure(xscrollcommand=scrollbarx.set)
            scrollbarx.grid(column=0, row=1, columnspan=2, sticky = 'EW', in_=self.data_table_frame)
        elif indexTab == 1:
            self.pixelTable = ttk.Treeview(self.pixel_table_frame, columns=['Pixel Name', 'Trigger', 'Variables', 'URL/PATH'], selectmode='extended')
            self.pixelTable.heading('#0', text='Category', anchor='w')
            self.pixelTable.heading('Pixel Name', text='Pixel Name', anchor='w')
            self.pixelTable.heading('Trigger', text='Trigger', anchor='w')
            self.pixelTable.heading('Variables', text='Variables', anchor='w')
            self.pixelTable.heading('URL/PATH', text='URL/PATH', anchor='w')
            self.pixelTable.column('#0', stretch=True, width=180)
            self.pixelTable.column('Pixel Name', stretch=True, width=260)
            self.pixelTable.column('Trigger', stretch=True, width=75)
            self.pixelTable.column('Variables', stretch=True, width=75)
            self.pixelTable.column('URL/PATH', stretch=True, width=160)
            self.pixelTable.bind("<KeyPress-Delete>",self.deleteBranch)
            self.pixelTable.grid(column=0, row=0, sticky='NESW')
            scrollbar = ttk.Scrollbar(self.pixel_table_frame, orient = 'vertical', command=self.pixelTable.yview)
            self.pixelTable.configure(yscrollcommand=scrollbar.set)
            scrollbar.grid(column=1, row=0, sticky = 'NS', in_=self.pixel_table_frame)
        elif indexTab == 2:
            self.GTMTable = ttk.Treeview(self.GTM_table_frame, columns=['Tag Name', 'Trigger', 'Variables', 'URL/PATH'], selectmode='extended')
            self.GTMTable.heading('#0', text='Category', anchor='w')
            self.GTMTable.heading('Tag Name', text='Tag Name', anchor='w')
            self.GTMTable.heading('Trigger', text='Trigger', anchor='w')
            self.GTMTable.heading('Variables', text='Variables', anchor='w')
            self.GTMTable.heading('URL/PATH', text='URL/PATH', anchor='w')
            self.GTMTable.column('#0', stretch=True, width=180)
            self.GTMTable.column('Tag Name', stretch=True, width=260)
            self.GTMTable.column('Trigger', stretch=True, width=75)
            self.GTMTable.column('Variables', stretch=True, width=75)
            self.GTMTable.column('URL/PATH', stretch=True, width=160)
            self.GTMTable.bind("<KeyPress-Delete>",self.deleteBranch)
            self.GTMTable.grid(column=0, row=0, sticky='NESW')
            scrollbar = ttk.Scrollbar(self.GTM_table_frame, orient = 'vertical', command=self.GTMTable.yview)
            self.GTMTable.configure(yscrollcommand=scrollbar.set)
            scrollbar.grid(column=1, row=0, sticky = 'NS', in_=self.GTM_table_frame)
        elif indexTab == 3:
            self.CAPITable = ttk.Treeview(self.CAPI_table_frame, columns=['Event Name', 'Trigger', 'Variables', 'URL/PATH'], selectmode='extended')
            self.CAPITable.heading('#0', text='Category', anchor='w')
            self.CAPITable.heading('Event Name', text='Event Name', anchor='w')
            self.CAPITable.heading('Trigger', text='Trigger', anchor='w')
            self.CAPITable.heading('Variables', text='Variables', anchor='w')
            self.CAPITable.heading('URL/PATH', text='URL/PATH', anchor='w')
            self.CAPITable.column('#0', stretch=True, width=180)
            self.CAPITable.column('Event Name', stretch=True, width=260)
            self.CAPITable.column('Trigger', stretch=True, width=75)
            self.CAPITable.column('Variables', stretch=True, width=75)
            self.CAPITable.column('URL/PATH', stretch=True, width=180)
            self.CAPITable.bind("<KeyPress-Delete>",self.deleteBranch)
            self.CAPITable.grid(column=0, row=0, sticky='NESW')

    def settingWindow(self, advanced=False):
        """
            This method implements the building of setting's window.
            
        Args:
            advanced (bool, optional): If True, advanced setting window is built. Defaults the basic setting is built.
        """        
                        
        if not advanced:      
            self.setWindow = tk.Toplevel(self.root)
            TITLE = PROGRAM_NAME+' Settings'
            self.setWindow.title(TITLE)
            self.setWindow.iconbitmap('resources/xaxis32x32.ico')
            self.setWindow.geometry("600x330+300+100")
            #General Section
            general_label_frame = ttk.LabelFrame(self.setWindow, text='General', width=595, height=100)
            general_frame       = ttk.Frame(general_label_frame)
            general_label_frame.grid(column=0, row=0)
            general_label_frame.grid_propagate(0)
            general_frame.grid(column=0, row=0)
            #SiteMap Section
            sitemap_label_frame = ttk.LabelFrame(self.setWindow, text='SiteMap', width=595, height=100)
            sitemap_frame       = ttk.Frame(sitemap_label_frame)
            sitemap_label_frame.grid(column=0, row=1)
            sitemap_label_frame.grid_propagate(0)
            sitemap_frame.grid(column = 0, row=0)
            #Pixels Section
            pixels_label_frame = ttk.LabelFrame(self.setWindow, text='Pixels', width=595, height=100)
            pixels_frame       = ttk.Frame(pixels_label_frame)
            pixels_label_frame.grid(column=0, row=2)
            pixels_label_frame.grid_propagate(0)
            pixels_frame.grid(column = 0, row=0)
            #GTM Section
            # gtm_label_frame = ttk.LabelFrame(self.setWindow, text='GTM', width=595, height=100)
            # gtm_frame       = ttk.Frame(gtm_label_frame)
            # gtm_label_frame.grid(column = 0, row=3)
            # gtm_label_frame.grid_propagate(0)
            # gtm_frame.grid(column = 0, row=0)
        
            #Buttons Section
            btn_frame       = ttk.Frame(self.setWindow)
            btn_frame.grid(column = 0, row=4)
            
            ttk.Button(btn_frame, text='Save', command = self.saveSettings).grid(column=0, row=0)
            self.setExit = ttk.Button(btn_frame, text='exit', command = self.setWindow.destroy, state = 'disable')
            self.setExit.grid(column=1, row=0)
            
            ttk.Label(general_frame, text='User: ').grid(column=0, row=0, sticky=tk.W)
            ttk.Label(general_frame, text='Xandr: ').grid(column=0, row=1, sticky=tk.W)
            ttk.Label(general_frame, text='DV360: ').grid(column=2, row=1, sticky=tk.W)
            ttk.Label(general_frame, text='Taboola: ').grid(column=4, row=1, sticky=tk.W)
            ttk.Label(general_frame, text='Minsights: ').grid(column=0, row=2, sticky=tk.W)
            ttk.Label(general_frame, text='Show: ').grid(column=2, row=2, sticky=tk.W)
            tk.Entry(general_frame, textvariable=self.users[0], font=('Arial',8,'italic'), relief=tk.SUNKEN, borderwidth=2).grid(row=0, column=1, columnspan=2, sticky='WE')
            self.xandr_passwd = tk.Entry(general_frame, textvariable=self.passwords[0], show='*', font=('Arial',8,'italic'), relief=tk.SUNKEN, borderwidth=2)
            self.xandr_passwd.grid(column=1, row=1, sticky=tk.W)
            self.dv360_passwd = tk.Entry(general_frame, textvariable=self.passwords[1], show='*', font=('Arial',8,'italic'), relief=tk.SUNKEN, borderwidth=2)
            self.dv360_passwd.grid(column=3, row=1, sticky=tk.W)
            self.taboo_passwd = tk.Entry(general_frame, textvariable=self.passwords[2], show='*', font=('Arial',8,'italic'), relief=tk.SUNKEN, borderwidth=2)
            self.taboo_passwd.grid(column=5, row=1, sticky=tk.W)
            self.minsi_passwd = tk.Entry(general_frame, textvariable=self.passwords[3], show='*', font=('Arial',8,'italic'), relief=tk.SUNKEN, borderwidth=2)
            self.minsi_passwd.grid(column=1, row=2, sticky=tk.W)
            #self.meta_passwd  = tk.Entry(general_frame, textvariable=self.passwords[4], show='*', font=('Arial',8,'italic'), relief=tk.SUNKEN, borderwidth=2)
            #self.meta_passwd.grid(column=3, row=2, sticky=tk.W)
            ttk.Checkbutton(general_frame, command=self.show_credentials, variable=self.show_, onvalue=True, offvalue=False).grid(column=3, row=2, sticky=tk.W)
        
            """
                Sitemap Settings
            """
            ttk.Label(sitemap_label_frame, text='Schemes: ').grid(column=0, row=0, sticky=tk.W)
            schemes = ttk.Combobox(sitemap_label_frame, textvariable=self.scheme, state='readonly', font=('Arial',8,'italic'))
            schemes['values'] = ['https', 'http', 'ftp']
            schemes.set(self.scheme.get())
            schemes.grid(column=1, row=0)
            ttk.Label(sitemap_label_frame, text='Build By: ').grid(column=2, row=0, sticky=tk.W)
            builtBy = ttk.Combobox(sitemap_label_frame, textvariable=self.builtBy, state='readonly', font=('Arial',8,'italic'))
            builtBy['values'] = ['path', 'fragment', 'query', 'parameters']
            builtBy.set(self.builtBy.get())
            builtBy.grid(column=3, row=0)
            #Minimun of Landins By Category
            ttk.Label(sitemap_label_frame, text="MLS: ").grid(column=4, row=0, sticky=tk.W)
            self.landingsBy = ttk.Spinbox(sitemap_label_frame, from_=0, to=100, command=self.set_landingsBy, wrap=True, width=14, state='readonly')
            self.landingsBy.set(self.webDOM.landingsBy)
            self.landingsBy.grid(column=5, row=0)
            #MSD: Maximo Sections Desirable
            ttk.Label(sitemap_label_frame, text="MSD: ").grid(column=0, row=2, sticky=tk.W)
            self.maxCategories = ttk.Scale(sitemap_label_frame, from_=10, to=50, command=self.set_maxCategories, variable=self.maxCategory)
            self.maxCategories.grid(column=1, row=3, sticky=tk.W)
            ttk.Label(sitemap_label_frame, textvariable=self.maxCategory, font=('Arial',8,'italic')).grid(column=1, row=2, sticky=tk.W)
            #MPW: Minimo Path Word
            ttk.Label(sitemap_label_frame, text="MPW: ").grid(column=2, row=2, sticky=tk.W)
            self.sizeWord = ttk.Scale(sitemap_label_frame, from_=2, to=15, command=self.set_sizeWord, variable=self.minSizeWord)
            self.sizeWord.grid(column=3, row=3)
            self.sizeWord.set(3)
            ttk.Label(sitemap_label_frame, textvariable=self.minSizeWord, font=('Arial',8,'italic')).grid(column=3, row=2, sticky=tk.W)
            #Minimo URL Deserable
            ttk.Label(sitemap_label_frame, text="MUD: ").grid(column=4, row=2, sticky=tk.W)
            self.landings = ttk.Scale(sitemap_label_frame, from_=10, to=500, command=self.set_maxLandings, variable=self.maxLandings)
            self.landings.grid(column=5, row=3, sticky=tk.W)
            ttk.Label(sitemap_label_frame, textvariable=self.maxLandings, font=('Arial',8,'italic')).grid(column=5, row=2, sticky=tk.W)
            """
                Pixels Settings
            """
            ttk.Label(pixels_label_frame, text='Scroll Deep: ').grid(column=0, row=0, sticky=tk.W)
            scrollDeep = ttk.Combobox(pixels_label_frame, state='readonly', textvariable=self.scrollDeep, font=('Arial',8,'italic'))
            scrollDeep.bind('<<ComboboxSelected>>', self.set_scrollDeep)
            scrollDeep['values'] = ['30', '50', '70', '100']
            scrollDeep.set(self.scrollDeep.get())
            scrollDeep.grid(column=1, row=0)
            ttk.Label(pixels_label_frame, text='Timer Last: ').grid(column=2, row=0, sticky=tk.W)
            timerLast = ttk.Combobox(pixels_label_frame, state='readonly', textvariable=self.timerLast, font=('Arial',8,'italic'))
            timerLast.bind('<<ComboboxSelected>>', self.set_timerLast)
            timerLast['values'] = ['30', '60', '120', '150']
            timerLast.set(self.timerLast.get())
            timerLast.grid(column=3, row=0)
            ttk.Label(pixels_label_frame, text="Delay Execution: ").grid(column=0, row=2, sticky=tk.W)
            delaySelenium = ttk.Scale(pixels_label_frame, from_=1, to=20, command=self.set_seleniumDelay, variable=self.seleniumDelay)
            delaySelenium.grid(column=1, row=3, sticky=tk.W)
            ttk.Label(pixels_label_frame, textvariable=self.seleniumDelay, font=('Arial',8,'italic')).grid(column=1, row=2, sticky=tk.W)
            ttk.Label(pixels_label_frame, text="Waitings: ").grid(column=2, row=2, sticky=tk.W)
            waitings = ttk.Scale(pixels_label_frame, from_=1, to=20, command=self.set_waitings, variable= self.waitings)
            waitings.grid(column=3, row=3, sticky=tk.W)
            ttk.Label(pixels_label_frame, textvariable=self.waitings, font=('Arial',8,'italic')).grid(column=3, row=2, sticky=tk.W)
        else:
            self.setWindow = tk.Toplevel(self.root)
            TITLE = PROGRAM_NAME+' Advanced Settings'
            self.setWindow.title(TITLE)
            self.setWindow.iconbitmap('resources/xaxis32x32.ico')
            self.setWindow.geometry("600x330+300+100")
            #Additional Platforms Section
            platform_label_frame = ttk.LabelFrame(self.setWindow, text='Additional Platforms', width=595, height=100)
            platform_frame       = ttk.Frame(platform_label_frame)
            platform_label_frame.grid(column=0, row=0)
            platform_label_frame.grid_propagate(0)
            platform_frame.grid(column=0, row=0)
            #Measument Strategy Section
            MS_label_frame = ttk.LabelFrame(self.setWindow, text='Measurement Strategy', width=595, height=100)
            MS_frame       = ttk.Frame(MS_label_frame)
            MS_label_frame.grid(column=0, row=1)
            MS_label_frame.grid_propagate(0)
            MS_frame.grid(column = 0, row=0)
            #Others Section
            pixels_label_frame = ttk.LabelFrame(self.setWindow, text='Others', width=595, height=100)
            pixels_frame       = ttk.Frame(pixels_label_frame)
            pixels_label_frame.grid(column=0, row=2)
            pixels_label_frame.grid_propagate(0)
            pixels_frame.grid(column = 0, row=0)
            #Buttons Section
            btn_frame       = ttk.Frame(self.setWindow)
            btn_frame.grid(column = 0, row=4)
            
            """Additional Platforms"""
            
            ttk.Label(platform_frame, text="Tik-Tok: ").grid(column =0, row=0, sticky=tk.W)
            ttk.Label(platform_frame, text="Twitter: ").grid(column =0, row=1, sticky=tk.W)
            ttk.Label(platform_frame, text="GA4: ").grid(column =3, row=0, sticky=tk.W)
            ttk.Label(platform_frame, text="Ads: ").grid(column =3, row=1, sticky=tk.W)
            ttk.Label(platform_frame, text="Meta: ").grid(column =6, row=0, sticky=tk.W)
            ttk.Label(platform_frame, text='Show: ').grid(column=6, row=1, sticky=tk.W)
            
            self.tiktok_passwd  = tk.Entry(platform_frame, textvariable=self.other_passwds[0], show='*', font=('Arial',8,'italic'), relief=tk.SUNKEN, borderwidth=2, width=17)
            self.tiktok_passwd.grid(column=1, row=0)
            self.twitter_passwd = tk.Entry(platform_frame, textvariable=self.other_passwds[3], show='*', font=('Arial',8,'italic'), relief=tk.SUNKEN, borderwidth=2, width=17)
            self.twitter_passwd.grid(column=1, row=1)
            self.ga4_passwd     = tk.Entry(platform_frame, textvariable=self.other_passwds[1], show='*', font=('Arial',8,'italic'), relief=tk.SUNKEN, borderwidth=2, width=17)
            self.ga4_passwd.grid(column=4, row=0)
            self.ads_passwd     = tk.Entry(platform_frame, textvariable=self.other_passwds[4], show='*', font=('Arial',8,'italic'), relief=tk.SUNKEN, borderwidth=2, width=17)
            self.ads_passwd.grid(column=4, row=1)
            self.meta_passwd    = tk.Entry(platform_frame, textvariable=self.other_passwds[2], show='*', font=('Arial',8,'italic'), relief=tk.SUNKEN, borderwidth=2, width=17)
            self.meta_passwd.grid(column=7, row=0)
            ttk.Checkbutton(platform_frame, command=lambda:self.show_credentials(True), variable=self.show, onvalue=True, offvalue=False).grid(column=7, row=1, sticky=tk.W)
            
            ttk.Checkbutton(platform_frame, command=lambda:self.set_programmatic(1), variable=self.__getattribute__('platform%s'%PLATFORMS_ADS[1].capitalize()), onvalue=True, offvalue=False).grid(column=2, row=0, sticky=tk.W)
            ttk.Checkbutton(platform_frame, command=lambda:self.set_programmatic(2), variable=self.__getattribute__('platform%s'%PLATFORMS_ADS[2].capitalize()), onvalue=True, offvalue=False).grid(column=2, row=1, sticky=tk.W)
            ttk.Checkbutton(platform_frame, command=lambda:self.set_programmatic(3), variable=self.__getattribute__('platform%s'%PLATFORMS_ADS[3].capitalize()), onvalue=True, offvalue=False).grid(column=5, row=0, sticky=tk.W)
            ttk.Checkbutton(platform_frame, command=lambda:self.set_programmatic(4), variable=self.__getattribute__('platform%s'%PLATFORMS_ADS[4].capitalize()), onvalue=True, offvalue=False).grid(column=5, row=1, sticky=tk.W)
            ttk.Checkbutton(platform_frame, command=lambda:self.set_programmatic(5), variable=self.__getattribute__('platform%s'%PLATFORMS_ADS[5].capitalize()), onvalue=True, offvalue=False).grid(column=8, row=0, sticky=tk.W)
            
            """Measurement Strategy"""
            ttk.Label(MS_frame, text='Type MS: ').grid(column=0, row=0, sticky=tk.W)
            ttk.Label(MS_frame, text='Type Tagging: ').grid(column=2, row=0, sticky=tk.W)
            ttk.Label(MS_frame, text="Unique Domain: ").grid(column =4, row=0, sticky=tk.W)
            ttk.Label(MS_frame, text="Program.: ").grid(column =0, row=1, sticky=tk.W)
            
            MS = ttk.Combobox(MS_frame, state='readonly', font=('Arial',8,'italic'))
            MS['values'] = TYPE_MS
            MS.set(TYPE_MS[1])
            MS.grid(column=1, row=0)
            taggingTypes = ttk.Combobox(MS_frame, state='readonly', font=('Arial',8,'italic'))
            taggingTypes['values'] = ['Web', 'Server', 'Hybrid']
            taggingTypes.set('Web')
            taggingTypes.grid(column=3, row=0)
            ttk.Checkbutton(MS_frame, command=lambda:self.set_programmatic(0), variable=self.__getattribute__('platform%s'%PLATFORMS_ADS[0].capitalize()), onvalue=True, offvalue=False).grid(column=5, row=0, sticky=tk.W)
            ttk.Checkbutton(MS_frame, command=lambda:self.set_programmatic(0), variable=self.__getattribute__('platform%s'%PLATFORMS_ADS[0].capitalize()), onvalue=True, offvalue=False).grid(column=1, row=1, sticky=tk.W)
            
            """Others Settings"""
            ttk.Label(pixels_frame, text='Marionette: ').grid(column=0, row=0, sticky=tk.W)
            ttk.Label(pixels_frame, text='Manual Scan: ').grid(column=2, row=0, sticky=tk.W)
            
            ttk.Checkbutton(pixels_frame, command=self.showMarionette, variable=self.marionette, onvalue=True, offvalue=False).grid(column=1, row=0, sticky=tk.W)
            ttk.Checkbutton(pixels_frame, command=self.setMSS, variable=self.mss, onvalue=True, offvalue=False).grid(column=3, row=0, sticky=tk.W)
            
            ttk.Button(btn_frame, text='Save', command = lambda:self.saveSettings(True)).grid(column=0, row=0)
            self.setExit = ttk.Button(btn_frame, text='exit', command = self.setWindow.destroy, state = 'disable')
            self.setExit.grid(column=1, row=0)
        
    def set_seleniumDelay(self, event=None):
        self.pixelBot.setSeleniumDelay(int(self.seleniumDelay.get()))
        print(self.pixelBot.seleniumDelay)
        
    def set_waitings(self, event=None):
        self.pixelBot.setWaitings(int(self.waitings.get()))
        print(self.pixelBot.waitings)
    
    def set_scrollDeep(self, event):
        pass
    
    def set_timerLast(self, event):
        pass
    
    def saveSettings(self, advanced=False):
        credentials = {'user':self.users[0].get(), 'passwords':{'Xandr':self.passwords[0].get(), 'DV360':self.passwords[1].get(), 'Taboola':self.passwords[2].get(), 'Minsights':self.passwords[3].get()}}
        credentials['otherPasswords'] = {'TikTok':self.other_passwds[0].get(), 'GA4':self.other_passwds[1].get(), 'Meta':self.other_passwds[2].get(), 'Twitter':self.other_passwds[3].get(), 'Ads':self.other_passwds[4].get()}
        if not advanced:
            if self.existAllCredentials:
                self.setExit.configure(state='active')  
        else:
            self.setExit.configure(state='active')
        with open(PLATFORM_CREDENTIALS, "w") as credentials_file:
            json.dump(credentials, credentials_file)
            
    def show_credentials(self, advanced=False):
        if not advanced:
            if self.show_.get():
                self.xandr_passwd.configure(show='')
                self.dv360_passwd.configure(show='')
                self.taboo_passwd.configure(show='')
                self.minsi_passwd.configure(show='')
            else:
                self.xandr_passwd.configure(show='*')
                self.dv360_passwd.configure(show='*')
                self.taboo_passwd.configure(show='*') 
                self.minsi_passwd.configure(show='*') 
        else:
            if self.show.get():
                self.tiktok_passwd.configure(show='')
                self.twitter_passwd.configure(show='')
                self.ga4_passwd.configure(show='')
                self.ads_passwd.configure(show='')
                self.meta_passwd.configure(show='') 
            else:   
                self.tiktok_passwd.configure(show='*')
                self.twitter_passwd.configure(show='*')
                self.ga4_passwd.configure(show='*')
                self.ads_passwd.configure(show='*')
                self.meta_passwd.configure(show='*')
                
    def setMSS(self):
        if self.mss.get():
            self.marionette.set(True)
            self.showMarionette()
            
    def showMarionette(self):
        if not self.marionette.get():
            self.mss.set(False)
        self.webDOM.setMarionette(self.marionette.get()) 
        self.pixelBot.setMarionette(self.marionette.get())     
         
    def addItem(self, parent, itemID, data, numTree=0):
        if numTree == 0:
            try:
                self.dataTable.insert(parent, 'end', iid=itemID, text=data[0], values=data[1:])
                print("Se ha agregado correctamente")
                return True
            except:
                print("No se ha agregado.")
                return False
        elif numTree == 1:
            try:
                self.pixelTable.insert(parent, 'end', iid=itemID, text=data[0], values=data[1:])
                return True
            except:
                return False
        elif numTree == 2:
            try:
                self.GTMTable.insert(parent, 'end', iid=itemID, text=data[0], values=data[1:])
                return True
            except:
                return False

    def deleteItemsTreeView(self, numTree=0):
        if numTree == 0:
            for mainSection in self.webDOM.mainSections:
                if self.dataTable.exists(mainSection):
                    try:
                        self.dataTable.delete(mainSection)
                    except:
                        continue
            if self.dataTable.exists('Borrar'):
                try:
                    self.dataTable.delete('Borrar')
                except:
                    pass  
        elif numTree == 1:
            for pixel in self.arrayPixels:
                if self.pixelTable.exists(pixel[0]):
                    try:
                        self.pixelTable.delete(pixel[0])
                    except:
                        continue
        elif numTree == 2:
            for pixel in self.arrayPixels:
                if self.GTMTable.exists(pixel[0]):
                    try:
                        self.GTMTable.delete(pixel[0])
                    except:
                        continue

    def addItemTreeView(self, arraySections):
        self.deleteItemsTreeView()
        index_section = 0
        idd = 0
        for mainSection in self.webDOM.mainSections:
            if mainSection == '':
                if self.dataTable.exists('MainDomain'):
                    self.dataTable.item('MainDomain', values=[self.webDOM.getUrlTarget(),''])
                else:
                    self.addItem('', 'Main', ['/Home','',''])
                    self.addItem('Main', 'MainDomain', ['', self.webDOM.getUrlTarget(),''])
            else:
                print("Index Section: "+str(index_section)+'  '+mainSection)
                parent = '/'+self.fitNameSection(mainSection)
                self.addItem('', mainSection, [parent,'',''])
                for subDomain in arraySections[index_section]:
                    #iid = subDomain.split('/')[-2] + subDomain.split('/')[-3]
                    print(mainSection+' '+str(idd)+' '+subDomain)
                    self.addItem(mainSection, idd,['', subDomain,''])
                    idd+=1
                index_section+=1
        else:
            if len(self.webDOM.subDomains)>1:
                self.addItem('', 'Borrar', ['/'+'Borrar','',''])
                self.addItem('Borrar', idd,['', 'subDomain',''])
                self.dataTable.delete('Borrar')
                
    def addItemTreeViewII(self, arrayPixels, numTree=1):
        """This method allows us to build the category tree of the pixels that we need in the Measurement
           Strategy to the data visualization of the functionalities of Pixel Creator and GTM integrator.

        Args:
            arrayPixels (_type_): _description_
            numTree (int, optional): _description_. Defaults to 1.
        """        
        categories = []
        idd = 0
        self.deleteItemsTreeView(numTree)
        for pixel in arrayPixels:
            if pixel[0] not in categories:
                categories.append(pixel[0])
        #time.sleep(10)
        for category in categories:
            self.addItem('', category, ['/'+category,'','','',''], numTree)
            for pixel in arrayPixels:
                if pixel[0] == category:
                    self.addItem(category, idd, ['',pixel[1],pixel[2],pixel[3],pixel[4]], numTree)
                idd+=1
        self.arrayPixels = arrayPixels
                
    def fitNameSection(self, nameSection):
        category = ''
        words = nameSection.split('/')
        self.webDOM.deleteItemList(words, '')
        if len(words)>1:
            if not words[0].isnumeric():
                words = words[0]
            else:
                words = words[1]
        else:
            words = words[0]
        #words = nameSection.replace('-', ' ')
        words = words.split('-')
        self.webDOM.deleteItemList(words, '')
        for word in words:
            if not word.isnumeric():
                category = category+word.capitalize()
        return category
        
    def createSectionSheets(self, mainSections):
        self.xlsxFile.setSheet('Sections')
        cell = 'C31'
        for platform in PLATFORMS_ADS:
            if self.__getattribute__('platform%s'%platform.capitalize()).get():
                cell, row, column = self.xlsxFile.nextFreeCell(cell)
                self.xlsxFile.writeCell('C'+str(row), 'Section')
                self.xlsxFile.writeCell('D'+str(row), 'Page View')
                self.xlsxFile.writeCell('G'+str(row), 'u/p')
        for mainSection in mainSections:
            mainSection_ = self.fitNameSection(mainSection)
            self.xlsxFile.duplicateSheet('Sections', mainSection_)
            self.xlsxFile.insertImage(mainSection_, 'B3')
        self.xlsxFile.setSheet('Tagging Request')
        self.xlsxFile.sheet = self.xlsxFile.book['Tagging Request']
        self.xlsxFile.sheet.title = 'Home'

    def aligmentCells(self):
        pass
            
    def loadData(self, dataSections):
        index_sheet = 5 #before 4
        for dataSection in dataSections:
            self.xlsxFile.setSheet(self.xlsxFile.book.sheetnames[index_sheet])
            nameSection = self.xlsxFile.book.sheetnames[index_sheet]
            nameSection = nameSection.split('-')
            self.webDOM.deleteItemList(nameSection, '')
            nameSection.sort(key=len, reverse=True)
            if len(nameSection)>1:
                nameSection = nameSection[0]+'-'+nameSection[1]
            else:
                nameSection = nameSection[0] 
            #if self.__getattribute__('platform%s'%PLATFORMS_ADS[3].capitalize()).get(): self.xlsxFile.writeCell('C24', self.__getattribute__('%sMeasurementID'%PLATFORMS_ADS[3]))   
            cell = 'E31'
            for platform in PLATFORMS_ADS:
                if self.__getattribute__('platform%s'%platform.capitalize()).get():
                    cell, row, column = self.xlsxFile.nextFreeCell(cell)
                    platform = '' if platform == 'programmatic' else platform
                    if platform == PLATFORMS_ADS[3] and self.__getattribute__('platform%s'%PLATFORMS_ADS[3].capitalize()).get(): self.xlsxFile.writeCell('I'+str(row), self.__getattribute__('%sMeasurementID'%PLATFORMS_ADS[3]))
                    self.xlsxFile.writeCell('E'+str(row), self.xlsxFile.getNameSection(self.advertiser.get(), nameSection+platform.capitalize()))
            self.xlsxFile.loadList(dataSection, 'F30')
            index_sheet += 1
        self.xlsxFile.setSheet(self.xlsxFile.book.sheetnames[2]) #before 1
        self.xlsxFile.loadList([self.urlAdvertiser.get()], 'F30')
        
    def find_threaded(self):
        thread = Thread(target = self.find)
        thread.start()
        
    def draw_threaded(self):
        thread = Thread(target = self.draw)
        thread.start()
        
    def pixels_threaded(self):
        #thread = Thread(target = self.loginAllPlatforms)
        thread = Thread(target = self.pixels)
        thread.start()
        
    def save_threaded(self):
        thread = Thread(target = self.save)
        thread.start()
        
    def savePixels_threaded(self):
        thread = Thread(target = self.savePixels)
        thread.start()

    def createPixels_threaded(self): 
        thread = Thread(target = self.createPixels)
        thread.start()
        
    def events_threaded(self):
        #self.logInPlatform(LOGIN_PAGES[5], self.users[0].get(), self.passwords[4].get())
        pass
        
    def set_gtmAccount_threaded(self, event):
        thread = Thread(target=self.set_gtmAccount, args=(event,))
        thread.start()
    
    def set_gtmContainer_threaded(self, event):
        thread = Thread(target=self.set_gtmContainer, args=(event,))
        thread.start()
        
    def set_gtmWorkspace_threaded(self, event):
        thread = Thread(target=self.set_gtmWorkspace, args=(event,))
        thread.start()
    
    def gtmConnect_threaded(self):
        thread = Thread(target=self.gtmConnect)
        thread.start()
    
    def tags_threaded(self):
        thread = Thread(target=self.tags)
        thread.start()
    
    def createTags_threaded(self):
        thread = Thread(target=self.createTags)
        thread.start()
    
    def saveTags_threaded(self):
        pass

    def updateCodeVerify_threaded(self):
        thread = Thread(target = self.updateCodeVerify)
        thread.start()
        
    def set_gtmAccount(self, event):
        """This method implements the actions that Tagbuilder executes when an account is selected from the account downlist.

        Args:
            event (event): Selected a account name from the account downlist in GTM Tab.

        Returns:
            Alert Window: If the process failed TagBuilder show us a window alert.
        """        
        self.gtmContainers, self.gtmWorkspaces = [], []
        account = self.gtmService.getAccount(self.listAccounts.get())
        if account == 404: return self.lanchPopUps('Validation Failed', 'Try to connect to GTM again!', 'Press "Ok" to exit.')
        containers = self.gtmService.getContainers(account['accountId'])
        for container in containers:
            self.gtmContainers.append(container['publicId'])
        workspaces = self.gtmService.getWorkSpaces(containers[0]['accountId'], containers[0]['containerId'])
        for workspace in workspaces:
            self.gtmWorkspaces.append(workspace['name'])
        self.container = containers[0]
        self.workspace = workspaces[0]
        self.listContainers['values'] = self.gtmContainers
        self.listContainers.set(self.gtmContainers[0])
        self.listWorkspaces['values'] = self.gtmWorkspaces
        self.listWorkspaces.set(self.gtmWorkspaces[0])
           
    def set_gtmContainer(self, event):
        """This method implements the actions that Tagbuilder executes when a container is selected from the container downlist.

        Args:
            event (event): Selected a GTM ID from the container downlist in GTM Tab.

        Returns:
            Alert Window: If the process failed TagBuilder show us a window alert.
        """        
        self.gtmWorkspaces = []
        account = self.gtmService.getAccount(self.listAccounts.get())
        if account == 404: return self.lanchPopUps('Validation Failed', 'Try to connect to GTM again!', 'Press "Ok" to exit.')
        container = self.gtmService.getContainer(account['accountId'], self.listContainers.get())
        if container == 404: return self.lanchPopUps('Validation Failed', 'Try to connect to GTM again!', 'Press "Ok" to exit.')
        workspaces = self.gtmService.getWorkSpaces(container['accountId'], container['containerId'])
        for workspace in workspaces:
            self.gtmWorkspaces.append(workspace['name'])
        self.container = container
        self.workspace = workspaces[0]
        self.listWorkspaces['values'] = self.gtmWorkspaces
        self.listWorkspaces.set(self.gtmWorkspaces[0])
        
    def set_gtmWorkspace(self, event):
        """This method implements the actions that Tagbuilder executes when a workspace is selected from the workspace downlist.

        Args:
            event (event): Selected a workspace from the workspace downlist in GTM Tab.

        Returns:
            Alert Window: If the process failed TagBuilder show us a window alert.
        """        
        workspace = self.gtmService.getWorkSpace(self.container['accountId'], self.container['containerId'], self.listWorkspaces.get())
        if workspace == 404: return self.lanchPopUps('Validation Failed', 'Try to connect to GTM again!', 'Press "Ok" to exit.')
        self.workspace = workspace
        print(self.workspace)
    
    def tags(self):
        """This method implements the extration of the pixels from TR Final.
        """
        self.xlsxFile.setSheet('Home')
        self.advertiser.set(self.xlsxFile.readCell('C13') if self.xlsxFile.readCell('C13') != None else '')
        if not hasattr(self, '%sMeasurementID'%PLATFORMS_ADS[3]):
            self.__setattr__('%sMeasurementID'%PLATFORMS_ADS[3], self.xlsxFile.readCell('C24') if self.xlsxFile.readCell('C24') != None else '')
        else:
            setattr(self, '%sMeasurementID'%PLATFORMS_ADS[3], self.xlsxFile.readCell('C24') if self.xlsxFile.readCell('C24') != None else '')
        self.btn_loadTags.configure(state='disable')
        if self.validTRFile('Final'):
            self.addItemTreeViewII(self.getArrayPixels(), 2)
            #self.getArrayPixels(self.getArrayPixels(), 2)
            self.btn_gtmConnect.configure(state='active')
            self.lanchPopUps('Extracted!', 'The Tags had read from TR!', 'Press "Ok" to exit.')
        else:
            self.lanchPopUps('Invalid File', 'You must choice a valid file!', 'Press "Ok" to exit.')
        self.btn_loadTags.configure(state='active')
    
    def gtmConnect(self):       
        """This function implement the GTM Service Conection between TagBuilder and GTM API.
        Furthermore, this function update the content of the list fields of the client account 
        and Container ID, and determine the value of Container Type in the GUI.
        """
        self.gtmAccounts, self.gtmContainers = [], []
        self.btn_gtmConnect.configure(state='disable')
        if not isinstance(self.gtmService, GTM):
            self.gtmService = GTM()  
        else:
            self.gtmService.accountList = self.gtmService.getAccounts()
        for account in self.gtmService.accountList:
            self.gtmAccounts.append(account['name'])
        else:
            self.gtmAccounts.sort()
        self.listAccounts['values'] = self.gtmAccounts 
        #self.listAccounts.set(self.gtmAccounts[0])
        self.listAccounts.set(self.gtmService.accountList[0]['name'])
        containers = self.gtmService.getContainers(self.gtmService.accountList[0]['accountId'])
        for container in containers:
            self.gtmContainers.append(container['publicId'])
        workspaces = self.gtmService.getWorkSpaces(containers[0]['accountId'], containers[0]['containerId'])
        for workspace in workspaces:
            self.gtmWorkspaces.append(workspace['name'])
        self.container = containers[0]
        self.workspace = workspaces[0]
        self.listContainers['values'] = self.gtmContainers
        self.listContainers.set(self.gtmContainers[0])
        self.listWorkspaces['values'] = self.gtmWorkspaces
        self.listWorkspaces.set(self.gtmWorkspaces[0])
        self.btn_gtmConnect.configure(state='active') 
        self.btn_tagging.configure(state='active')    
        
    def createTags(self):
        """This method sets the Tags load from the TR Final file. This process implies the following steps:
            1. Creation or update of the Strategy GroupM Folder.
            2. Creation or update of variables require to implement the tags load from the TR Final file.
            3. Creation or update of triggers requiere to implement the tags load from the TR Final file.
            4. Creation or update of tags load from the TR Final File.

        Returns:
            None: None
        """        
        
        self.gtmVariables = []
        self.gtmTags      = []
        folders           = [-1 for i in range(len(PLATFORMS_ADS))]
        triggersID        = [[] for i in range(len(PLATFORMS_ADS))]
        otherID           = ['' for i in range(len(PLATFORMS_ADS))]
        ga4SettingName    = 'WebStreamGA4'
        ga4Index          = PLATFORMS_ADS.index('ga4')
        progress          = 0
        self.tagProgress.set(progress)
        _gtmID = self.get_gtm_id()
        if _gtmID == None or _gtmID != self.container['publicId']:
            return self.lanchPopUps('GTM ID Error!', "Verify the GTM ID in TagBuilder and TR File!", 'Press "Ok" to exit.')
        self.btn_loadTags.configure(state='disable')
        self.btn_gtmConnect.configure(state='disable')
        self.btn_tagging.configure(state='disable')
        tags, triggers, variables = [], [], []
        #Creation of Folders and Custom Variables
        variables = self.gtmService.getAllVariables(self.container['accountId'], self.container['containerId'], self.workspace['workspaceId'])
        for pixel in self.arrayPixels:
            snippet = ''
            for code in pixel[6:-2]:
                if code != None and code.casefold() not in ['si', 'no', '', 'url', 'event']:
                    snippet += code
            if snippet == '': 
                continue
            else:
                for platform in PLATFORMS_ADS:
                    index = PLATFORMS_ADS.index(platform)
                    #platform = platform.capitalize() if platform != 'programmatic' else ''
                    platform = platform.capitalize()
                    if re.findall(r'%sPV_|%sBtn_|%sScroll\d{1,2}_|%sT\d+ss_'%(platform, platform, platform, platform), pixel[1]):
                        if folders[index] == -1:
                            exist, folders[index] = self.gtmService.existElement(self.workspace['path'], 'Strategy_Nexus%s_'%platform, 'Folder')
                            nameFolder = Naming.createName('Nexus%s'%platform, 'Strategy')
                            if exist:
                                print('El folder de esta plataforma existe')
                                folders[index] = self.gtmService.updateFolder(folders[index]['path'], nameFolder)
                            else:
                                print('El folder de esta plataforma no existe')
                                folders[index] = self.gtmService.createFolder(self.workspace['path'], nameFolder)
                        else:
                            pass
                        pixelVariables = self.fitCustomVariables(pixel[3]).split('/')
                        for pvar in pixelVariables:
                            pvarName = pvar
                            pvar = pvar.casefold()
                            if pvar not in ['u', 'p', 'r']:
                                if (not self.existVariable(variables, pvar) and not self.existVariable(self.gtmVariables, pvar)) or (self.existVariable(variables, pvar) and not self.existVariable(self.gtmVariables, pvar)):
                                    if pvar == 'hash':
                                        self.gtmVariables.append(BasicVariable(pvarName, 'u'))
                                        self.gtmVariables[-1].setProperty('parentFolderId', folders[index]['folderId'])
                                        if not self.existVariable(variables, pvarName): 
                                            self.gtmVariables[-1].setState()
                                        else:
                                            self.gtmVariables[-1].setProperty('variableId', self.getVariableId(variables, pvarName))
                                    else:
                                        if [True for var in pixel[3].casefold().split('/') if re.findall(r'^%s:query'%pvar, var)]:
                                            self.gtmVariables.append(BasicVariable(pvarName, 'u', {'querykey': pixel[5]}))
                                            self.gtmVariables[-1].setProperty('parentFolderId', folders[index]['folderId'])
                                            if not self.existVariable(variables, pvarName): 
                                                self.gtmVariables[-1].setState()
                                            else:
                                                self.gtmVariables[-1].setProperty('variableId', self.getVariableId(variables, pvarName))
                                        elif [True for var in pixel[3].casefold().split('/') if re.findall(r'^%s:datalayer'%pvar, var)]:
                                            pass
                                        elif [True for var in pixel[3].casefold().split('/') if re.findall(r'^%s:javascript'%pvar, var)]:
                                            pass
                                        elif [True for var in pixel[3].casefold().split('/') if re.findall(r'^%s:customjavascript'%pvar, var)]:
                                            pass
                                        else:
                                            pass
                        break
                else:
                    if folders[0] == -1:
                        exist, folders[0] = self.gtmService.existElement(self.workspace['path'], 'Strategy_Nexus_', 'Folder')
                        if exist:
                            folders[0] = self.gtmService.updateFolder(folders[0]['path'])
                        else:
                            folders[0] = self.gtmService.createFolder(self.workspace['path'])
                    else:
                        pass
                    pixelVariables = self.fitCustomVariables(pixel[3]).split('/')
                    for pvar in pixelVariables:
                        pvarName = pvar
                        pvar = pvar.casefold()
                        if pvar not in ['u', 'p', 'r']:
                            if (not self.existVariable(variables, pvar) and not self.existVariable(self.gtmVariables, pvar)) or (self.existVariable(variables, pvar) and not self.existVariable(self.gtmVariables, pvar)):
                                if pvar == 'hash':
                                    self.gtmVariables.append(BasicVariable(pvar, 'u'))
                                    self.gtmVariables[-1].setProperty('parentFolderId', folders[0]['folderId'])
                                    if not self.existVariable(variables, pvar): 
                                        self.gtmVariables[-1].setState()
                                    else:
                                        self.gtmVariables[-1].setProperty('variableId', self.getVariableId(variables, pvarName))
                                else:
                                    if [True for var in pixel[3].casefold().split('/') if re.findall(r'^%s:query'%pvar, var)]:
                                        self.gtmVariables.append(BasicVariable(pvar, 'u', {'querykey': pixel[5]}))
                                        self.gtmVariables[-1].setProperty('parentFolderId', folders[0]['folderId'])
                                        if not self.existVariable(variables, pvar): 
                                            self.gtmVariables[-1].setState()
                                        else:
                                            self.gtmVariables[-1].setProperty('variableId', self.getVariableId(variables, pvarName))
                                    elif [True for var in pixel[3].casefold().split('/') if re.findall(r'^%s:datalayer'%pvar, var)]:
                                        pass
                                    elif [True for var in pixel[3].casefold().split('/') if re.findall(r'^%s:javascript'%pvar, var)]:
                                        pass
                                    elif [True for var in pixel[3].casefold().split('/') if re.findall(r'^%s:customjavascript'%pvar, var)]:
                                        pass
                                    else:
                                        pass
        self.tagProgress.set(5)
        for var in self.gtmVariables:
            if var.create:
                while True:
                    try:
                        self.gtmService.createVariable(self.workspace['accountId'], self.workspace['containerId'], self.workspace['workspaceId'], var.temple)
                    except HttpError:
                        print("GTM: Don't hurry me, please. Go us so fast!!!")
                        time.sleep(60)
                        self.gtmService.createVariable(self.workspace['accountId'], self.workspace['containerId'], self.workspace['workspaceId'], var.temple)
                    break   
            else:
                while True:
                    try:
                        self.gtmService.updateVariable(self.workspace['path']+'/variables/%s'%var.temple['variableId'], var.temple)
                    except HttpError:
                        print("GTM: Don't hurry me, please. Go us so fast!!!")
                        time.sleep(60)
                        self.gtmService.updateVariable(self.workspace['path']+'/variables/%s'%var.temple['variableId'], var.temple)
                    break 
        self.tagProgress.set(10)
        tags = self.gtmService.getAllTags(self.container['accountId'], self.container['containerId'], self.workspace['workspaceId'])
        triggers  = self.gtmService.getAllTriggers(self.container['accountId'], self.container['containerId'], self.workspace['workspaceId'])
        #Creation of GA4 Setting Tag
        if folders[ga4Index] != -1:
            ga4SettingName = Naming.createName('WebStreamGA4', self.advertiser.get())
            self.gtmTags.append(GA4Setting(ga4SettingName, self.__getattribute__('%sMeasurementID'%PLATFORMS_ADS[3])))
            self.gtmTags[-1].setProperty('parentFolderId', folders[ga4Index]['folderId'])
            if not self.existTag(tags, ga4SettingName):
                self.gtmTags[-1].setState()
            else:
                tagId = self.getTagId(tags, ga4SettingName)
                if tagId != '': self.gtmTags[-1].setProperty('tagId', tagId)
        self.tagProgress.set(15)
        self.updateSnipetCodes()
        self.tagProgress.set(20)
        home = urlparse(self.get_homepage()).hostname if self.get_homepage() != None else 'homepage.com'
        for pixel in self.arrayPixels:
            snippet = ''
            for code in pixel[6:-2]:
                if code != None and code.casefold() not in ['si', 'no', '', 'url', 'event']:
                    snippet += code
            if snippet == '': continue
            advertiser, trigger, date = pixel[1].split('_')
            if pixel[0] == 'Home' or pixel[0] == 'Funnel':
                if [True for p in PLATFORMS_ADS if re.findall(r'%sPV$|%sBtn$|%sScroll\d{1,2}$|%sT\d+ss$'%(p.capitalize(),p.capitalize(), p.capitalize(),p.capitalize()),trigger)]:
                    if re.findall(r'Ga4PV$|Ga4Btn$|Ga4Scroll\d{1,2}$|Ga4T\d+ss$',trigger):
                        self.gtmTags.append(GA4Event(pixel[1], ga4SettingName))
                        self.gtmTags[-1].setProperty('parentFolderId', folders[ga4Index]['folderId'])
                        if not self.existTag(tags, pixel[1]):
                            self.gtmTags[-1].setState()
                        else:
                            tagId = self.getTagId(tags, pixel[1])
                            if tagId != '': self.gtmTags[-1].setProperty('tagId', tagId)
                        if re.findall(r'Ga4Scroll\d{1,2}$',trigger):
                            if re.findall(r'^AllPages', trigger):
                                try:
                                    depth = re.findall(r'\d{1,2}', re.findall(r'Scroll\d{1,2}', trigger)[0])[0]
                                except:
                                    depth = self.scrollDeep.get()
                                self.gtmTags[-1].setTrigger(ScrollTrigger(pixel[1], depth))
                                self.gtmTags[-1].trigger.setProperty('parentFolderId', folders[ga4Index]['folderId'])
                                if not self.existTrigger(triggers, pixel[1]): 
                                    self.gtmTags[-1].trigger.setState()
                                else:
                                    triggerId = self.getTriggerId(triggers, pixel[1])
                                    if triggerId != '': 
                                        self.gtmTags[-1].setProperty('firingTriggerId', [triggerId])
                                        self.gtmTags[-1].trigger.setProperty('triggerId', triggerId)
                        elif re.findall(r'Ga4T\d+ss$',trigger):
                            if re.findall(r'^AllPages', trigger):
                                try:
                                    time_ = re.findall(r'\d+', re.findall(r'T\d+ss', trigger)[0])[0]
                                except:
                                    time_ = self.timerLast.get()
                                self.gtmTags[-1].setTrigger(TimerTrigger(pixel[1], time_, home))
                                self.gtmTags[-1].trigger.setProperty('parentFolderId', folders[ga4Index]['folderId'])
                                if not self.existTrigger(triggers, pixel[1]): 
                                    self.gtmTags[-1].trigger.setState()
                                else:
                                    triggerId = self.getTriggerId(triggers, pixel[1])
                                    if triggerId != '': 
                                        self.gtmTags[-1].setProperty('firingTriggerId', [triggerId])
                                        self.gtmTags[-1].trigger.setProperty('triggerId', triggerId)
                        elif re.findall(r'Ga4Btn$',trigger):
                            try:
                                attribute, value = pixel[5].split(':')
                                attribute, value = attribute.upper(), value
                            except:
                                attribute, value = 'TEXT', 'TBD'
                            self.gtmTags[-1].setTrigger(ClickTrigger(pixel[1], attribute, value))
                            self.gtmTags[-1].trigger.setProperty('parentFolderId', folders[ga4Index]['folderId'])
                            if self.gtmSharing: self.gtmTags[-1].trigger.addFilter('filter', 'endsWith', 'Page Hostname', home)
                            if not self.existTrigger(triggers, pixel[1]): 
                                self.gtmTags[-1].trigger.setState()
                            else:
                                triggerId = self.getTriggerId(triggers, pixel[1])
                                if triggerId != '': 
                                    self.gtmTags[-1].setProperty('firingTriggerId', [triggerId])
                                    self.gtmTags[-1].trigger.setProperty('triggerId', triggerId)
                        else:
                            if re.findall(r'^HomeUTM', trigger):
                                pass
                            elif re.findall(r'^Home', trigger):
                                self.gtmTags[-1].setTrigger(PageviewTrigger(pixel[1], pixel[4], pageType='Home'))
                                self.gtmTags[-1].trigger.setProperty('parentFolderId', folders[ga4Index]['folderId'])
                                if not self.existTrigger(triggers, pixel[1]): 
                                    self.gtmTags[-1].trigger.setState()
                                else:
                                    triggerId = self.getTriggerId(triggers, pixel[1])
                                    if triggerId != '': 
                                        self.gtmTags[-1].setProperty('firingTriggerId', [triggerId])
                                        self.gtmTags[-1].trigger.setProperty('triggerId', triggerId)
                            elif re.findall(r'AllPages', trigger):
                                self.gtmTags[-1].setProperty('firingTriggerId', '2147479553')
                            else:
                                self.gtmTags[-1].setTrigger(PageviewTrigger(pixel[1], pixel[4], pageType='Section'))
                                self.gtmTags[-1].trigger.setProperty('parentFolderId', folders[ga4Index]['folderId'])
                                if self.gtmSharing: self.gtmTags[-1].trigger.addFilter('filter', 'endsWith', 'Page Hostname', home)
                                if not self.existTrigger(triggers, pixel[1]): 
                                    self.gtmTags[-1].trigger.setState()
                                else:
                                    triggerId = self.getTriggerId(triggers, pixel[1])
                                    if triggerId != '': 
                                        self.gtmTags[-1].setProperty('firingTriggerId', [triggerId])
                                        self.gtmTags[-1].trigger.setProperty('triggerId', triggerId)
                    elif re.findall(r'AdsPV$|AdsBtn$|AdsScroll\d{1,2}$|AdsT\d+ss$',trigger):
                        pass
                    elif re.findall(r'MetaPV$|MetaBtn$|MetaScroll\d{1,2}$|MetaT\d+ss$',trigger):
                        pass
                    elif re.findall(r'TwitterPV$|TwitterBtn$|TwitterScroll\d{1,2}$|TwitterT\d+ss$',trigger):
                        pass
                    elif re.findall(r'Tik-tokPV$|Tik-tokBtn$|Tik-tokScroll\d{1,2}$|Tik-tokT\d+ss$',trigger):
                        pass
                    else:
                        pass
                else:
                    if re.findall(r'PV$', trigger):
                        if re.findall(r'^HomeUTM', trigger):
                            pass
                        elif re.findall(r'^Home', trigger):
                            self.gtmTags.append(CustomTemple(pixel[1], snippet))
                            self.gtmTags[-1].setProperty('parentFolderId', folders[0]['folderId'])
                            self.gtmTags[-1].setTrigger(PageviewTrigger(pixel[1], pixel[4], pageType='Home'))
                            self.gtmTags[-1].trigger.setProperty('parentFolderId', folders[0]['folderId'])
                            if not self.existTag(tags, pixel[1]):
                                self.gtmTags[-1].setState()
                            else:
                                tagId = self.getTagId(tags, pixel[1])
                                if tagId != '': self.gtmTags[-1].setProperty('tagId', tagId)
                            if not self.existTrigger(triggers, pixel[1]): 
                                self.gtmTags[-1].trigger.setState()
                            else:
                                triggerId = self.getTriggerId(triggers, pixel[1])
                                if triggerId != '': 
                                    self.gtmTags[-1].setProperty('firingTriggerId', [triggerId])
                                    self.gtmTags[-1].trigger.setProperty('triggerId', triggerId)
                        elif re.findall(r'AllPages', trigger):
                            self.gtmTags.append(CustomTemple(pixel[1], snippet))
                            self.gtmTags[-1].setProperty('firingTriggerId', '2147479553')
                            self.gtmTags[-1].setProperty('parentFolderId', folders[0]['folderId'])
                            if not self.existTag(tags, pixel[1]): 
                                self.gtmTags[-1].setState()
                            else:
                                tagId = self.getTagId(tags, pixel[1])
                                if tagId != '': self.gtmTags[-1].setProperty('tagId', tagId)
                        else:
                            self.gtmTags.append(AudienceTag(pixel[1], snippet, pixel[4])) 
                            self.gtmTags[-1].setProperty('parentFolderId', folders[0]['folderId'])
                            self.gtmTags[-1].trigger.setProperty('parentFolderId', folders[0]['folderId'])
                            if self.gtmSharing: self.gtmTags[-1].trigger.addFilter('filter', 'endsWith', 'Page Hostname', home)
                            if not self.existTag(tags, pixel[1]): 
                                self.gtmTags[-1].setState()
                            else:
                                tagId = self.getTagId(tags, pixel[1])
                                if tagId != '': self.gtmTags[-1].setProperty('tagId', tagId)
                            if not self.existTrigger(triggers, pixel[1]): 
                                self.gtmTags[-1].trigger.setState()
                            else:
                                triggerId = self.getTriggerId(triggers, pixel[1])
                                if triggerId != '': 
                                    self.gtmTags[-1].setProperty('firingTriggerId', [triggerId])
                                    self.gtmTags[-1].trigger.setProperty('triggerId', triggerId)
                    elif re.findall(r'Scroll\d{1,2}$', trigger):
                        if re.findall(r'^AllPages', trigger):
                            self.gtmTags.append(CustomTemple(pixel[1], snippet))
                            self.gtmTags[-1].setProperty('parentFolderId', folders[0]['folderId'])
                            try:
                                depth = re.findall(r'\d{1,2}', re.findall(r'Scroll\d{1,2}', trigger)[0])[0]
                            except:
                                depth = self.scrollDeep.get()
                            self.gtmTags[-1].setTrigger(ScrollTrigger(pixel[1], depth))
                            self.gtmTags[-1].trigger.setProperty('parentFolderId', folders[0]['folderId'])
                            if not self.existTag(tags, pixel[1]):
                                self.gtmTags[-1].setState()
                            else:
                                tagId = self.getTagId(tags, pixel[1])
                                if tagId != '': self.gtmTags[-1].setProperty('tagId', tagId)
                            if not self.existTrigger(triggers, pixel[1]): 
                                self.gtmTags[-1].trigger.setState()
                            else:
                                triggerId = self.getTriggerId(triggers, pixel[1])
                                if triggerId != '': 
                                    self.gtmTags[-1].setProperty('firingTriggerId', [triggerId])
                                    self.gtmTags[-1].trigger.setProperty('triggerId', triggerId)
                    elif re.findall(r'T\d+ss$', trigger):
                        if re.findall(r'^AllPages', trigger):
                            self.gtmTags.append(CustomTemple(pixel[1], snippet))
                            self.gtmTags[-1].setProperty('parentFolderId', folders[0]['folderId'])
                            try:
                                time_ = re.findall(r'\d+', re.findall(r'T\d+ss', trigger)[0])[0]
                            except:
                                time_ = self.timerLast.get()
                            self.gtmTags[-1].setTrigger(TimerTrigger(pixel[1], time_, home))
                            self.gtmTags[-1].trigger.setProperty('parentFolderId', folders[0]['folderId'])
                            if not self.existTag(tags, pixel[1]):
                                self.gtmTags[-1].setState()
                            else:
                                tagId = self.getTagId(tags, pixel[1])
                                if tagId != '': self.gtmTags[-1].setProperty('tagId', tagId)
                            if not self.existTrigger(triggers, pixel[1]): 
                                self.gtmTags[-1].trigger.setState()
                            else:
                                triggerId = self.getTriggerId(triggers, pixel[1])
                                if triggerId != '': 
                                    self.gtmTags[-1].setProperty('firingTriggerId', [triggerId])
                                    self.gtmTags[-1].trigger.setProperty('triggerId', triggerId)
                    elif re.findall(r'Btn$', trigger):
                        try:
                            attribute, value = pixel[5].split(':')
                            attribute, value = attribute.upper(), value
                        except:
                            attribute, value = 'TEXT', 'TBD'
                        self.gtmTags.append(ButtonTag(pixel[1], snippet, {'attribute':attribute, 'value':value}))
                        self.gtmTags[-1].setProperty('parentFolderId', folders[0]['folderId']) 
                        self.gtmTags[-1].trigger.setProperty('parentFolderId', folders[0]['folderId'])
                        if self.gtmSharing: self.gtmTags[-1].trigger.addFilter('filter', 'endsWith', 'Page Hostname', home)
                        if not self.existTag(tags, pixel[1]): 
                            self.gtmTags[-1].setState()
                        else:
                            tagId = self.getTagId(tags, pixel[1])
                            if tagId != '': self.gtmTags[-1].setProperty('tagId', tagId)
                        if not self.existTrigger(triggers, pixel[1]): 
                            self.gtmTags[-1].trigger.setState()
                        else:
                            triggerId = self.getTriggerId(triggers, pixel[1])
                            if triggerId != '': 
                                self.gtmTags[-1].setProperty('firingTriggerId', [triggerId])
                                self.gtmTags[-1].trigger.setProperty('triggerId', triggerId)
                    else:
                        continue
            elif 'Otros' in pixel[0]:
                if [True for p in PLATFORMS_ADS if re.findall(r'%sPV$'%p.capitalize(),trigger)]:
                    index = [PLATFORMS_ADS.index(p) for p in PLATFORMS_ADS if re.findall(r'%sPV$'%p.capitalize(), trigger)]
                    index = index[0] if index else 0
                    otherID[index] = self.getTagId(tags, pixel[1]) if self.existTag(tags, pixel[1]) else otherID[0]
                else: 
                    otherID[0] = self.getTagId(tags, pixel[1]) if self.existTag(tags, pixel[1]) else otherID[0]
            else:
                if [True for p in PLATFORMS_ADS if re.findall(r'%sPV$'%p.capitalize(),trigger)]:
                    self.gtmTags.append(GA4Event(pixel[1], ga4SettingName))
                    self.gtmTags[-1].setProperty('parentFolderId', folders[ga4Index]['folderId'])
                    if not self.existTag(tags, pixel[1]):
                        self.gtmTags[-1].setState()
                    else:
                        tagId = self.getTagId(tags, pixel[1])
                        if tagId != '': self.gtmTags[-1].setProperty('tagId', tagId)
                    if re.findall(r'^HomeUTM', trigger):
                        pass
                    elif re.findall(r'^Home', trigger):
                        self.gtmTags[-1].setTrigger(PageviewTrigger(pixel[1], pixel[4], pageType='Home'))
                        self.gtmTags[-1].trigger.setProperty('parentFolderId', folders[ga4Index]['folderId'])
                        if not self.existTrigger(triggers, pixel[1]): 
                            self.gtmTags[-1].trigger.setState()
                        else:
                            triggerId = self.getTriggerId(triggers, pixel[1])
                            if triggerId != '': 
                                self.gtmTags[-1].setProperty('firingTriggerId', [triggerId])
                                self.gtmTags[-1].trigger.setProperty('triggerId', triggerId)
                    elif re.findall(r'AllPages', trigger):
                        self.gtmTags[-1].setProperty('firingTriggerId', '2147479553')
                    else:
                        self.gtmTags[-1].setTrigger(PageviewTrigger(pixel[1], pixel[4], pageType='Section'))
                        self.gtmTags[-1].trigger.setProperty('parentFolderId', folders[ga4Index]['folderId'])
                        if self.gtmSharing: self.gtmTags[-1].trigger.addFilter('filter', 'endsWith', 'Page Hostname', home)
                        if not self.existTrigger(triggers, pixel[1]): 
                            self.gtmTags[-1].trigger.setState()
                        else:
                            triggerId = self.getTriggerId(triggers, pixel[1])
                            if triggerId != '': 
                                self.gtmTags[-1].setProperty('firingTriggerId', [triggerId])
                                self.gtmTags[-1].trigger.setProperty('triggerId', triggerId)
                else:
                    self.gtmTags.append(AudienceTag(pixel[1], snippet, pixel[4])) 
                    self.gtmTags[-1].setProperty('parentFolderId', folders[0]['folderId'])
                    self.gtmTags[-1].trigger.setProperty('parentFolderId', folders[0]['folderId'])
                    if self.gtmSharing: self.gtmTags[-1].trigger.addFilter('filter', 'endsWith', 'Page Hostname', home)
                    if not self.existTag(tags, pixel[1]): 
                        self.gtmTags[-1].setState()
                    else:
                        tagId = self.getTagId(tags, pixel[1])
                        if tagId != '': self.gtmTags[-1].setProperty('tagId', tagId)
                    if not self.existTrigger(triggers, pixel[1]): 
                        self.gtmTags[-1].trigger.setState()
                    else:
                        triggerId = self.getTriggerId(triggers, pixel[1])
                        if triggerId != '': 
                            self.gtmTags[-1].setProperty('firingTriggerId', [triggerId])
                            self.gtmTags[-1].trigger.setProperty('triggerId', triggerId)
        progress = 25
        self.tagProgress.set(progress)
        print('-*'*200)
        print('El numero de Tags a crear es: ', len(self.gtmTags))
        deltaTag = 70/(len(self.gtmTags)) if len(self.gtmTags)>0 else 85
        if deltaTag == 85: self.tagProgress.set(10+deltaTag)
        print('Cada incremento es de: ', deltaTag)
        for tag, index in zip(self.gtmTags,range(len(self.gtmTags))):
            if 'AllPagesPV' in tag.temple['name'] or 'WebStreamGA4' in tag.temple['name'] or 'AllPagesGa4PV' in tag.temple['name']:
                pass
            elif tag.trigger.create:
                while True:
                    try:
                        trg = self.gtmService.createTrigger(self.workspace['accountId'], self.workspace['containerId'], self.workspace['workspaceId'], tag.trigger.temple)
                        self.gtmTags[index].setProperty('firingTriggerId', [trg['triggerId']])
                    except HttpError:
                        print("GTM: Don't hurry me, please. Go us so fast!!!")
                        time.sleep(60)
                        trg = self.gtmService.createTrigger(self.workspace['accountId'], self.workspace['containerId'], self.workspace['workspaceId'], tag.trigger.temple)
                    break
                self.gtmTags[index].setProperty('firingTriggerId', [trg['triggerId']])
                if 'PV_' in tag.temple['name'] and not 'AllPages' in tag.temple['name']:
                    print('Si hay tags tipo PV')
                    advertiser, trigger, date = tag.temple['name'].split('_')
                    if [True for p in PLATFORMS_ADS if re.findall(r'%sPV$'%p.capitalize(),trigger)]:
                        print('entramos a las plataformas')
                        index = [PLATFORMS_ADS.index(p) for p in PLATFORMS_ADS if re.findall(r'%sPV$'%p.capitalize(), trigger)]
                        index = index[0] if index else 0
                        triggersID[index].append(trg['triggerId'])
                    else:
                        print('entramos a programattic')
                        triggersID[0].append(trg['triggerId'])
                print('Trigger Nuevo: ', trg)
            else:
                while True:
                    try:
                        self.gtmService.updateTrigger(self.workspace['path']+'/triggers/%s'%tag.trigger.temple['triggerId'], tag.trigger.temple)
                    except HttpError:
                        print("GTM: Don't hurry me, please. Go us so fast!!!")
                        time.sleep(60)
                        self.gtmService.updateTrigger(self.workspace['path']+'/triggers/%s'%tag.trigger.temple['triggerId'], tag.trigger.temple)
                    break
                if 'PV_' in tag.temple['name'] and not 'AllPages' in tag.temple['name']:
                    print('Si hay tags tipo PV')
                    advertiser, trigger, date = tag.temple['name'].split('_')
                    if [True for p in PLATFORMS_ADS if re.findall(r'%sPV$'%p.capitalize(),trigger)]:
                        index = [PLATFORMS_ADS.index(p) for p in PLATFORMS_ADS if re.findall(r'%sPV$'%p.capitalize(), trigger)]
                        index = index[0] if index else 0
                        triggersID[index].append(tag.trigger.temple['triggerId'])
                    else:
                        triggersID[0].append(tag.trigger.temple['triggerId'])
            if tag.create:
                print('Tag Nuevo: ', tag.temple)
                while True:
                    try:
                        self.gtmService.createTag(self.workspace['accountId'], self.workspace['containerId'], self.workspace['workspaceId'], tag.temple)
                    except HttpError:
                        print("GTM: Don't hurry me, please. Go us so fast!!!")
                        time.sleep(60)
                        self.gtmService.createTag(self.workspace['accountId'], self.workspace['containerId'], self.workspace['workspaceId'], tag.temple)
                    break
            else:
                print('Tag Existente: ', tag.temple)
                while True:
                    try:
                        self.gtmService.updateTag(self.workspace['path']+'/tags/%s'%tag.temple['tagId'], tag.temple)
                    except HttpError:
                        print("GTM: Don't hurry me, please. Go us so fast!!!")
                        time.sleep(60)
                        self.gtmService.updateTag(self.workspace['path']+'/tags/%s'%tag.temple['tagId'], tag.temple)
                    break
            progress += deltaTag
            print('El avance es: ', progress)
            #self.tagProgress.set(10+int(deltaTag*index))
            self.tagProgress.set(progress)
            time.sleep(10)
        print('o-o'*60)
        print('OtherIDs: ', otherID)
        print('|-|'*60)
        print('TriggerIDs: ', triggersID)
        if [True for tID in triggersID if tID]:
            print('Empezamos creación de tag Otros')
            #if len(triggersID[0])>0:
            #index = index[0] if index else 0
            for pixel in self.arrayPixels:
                if pixel[0] == 'Otros':
                    print('Pixel de Otros a analizar: ', pixel[1])
                    snippet = ''
                    for code in pixel[6:-2]:
                        if code != None and code.casefold() not in ['si', 'no', '', 'url', 'event']:
                            snippet += code
                    if snippet == '': continue
                    advertiser, trigger, date = pixel[1].split('_')
                    index = [PLATFORMS_ADS.index(p) for p in PLATFORMS_ADS if re.findall(r'%sPV$'%p.capitalize(), trigger)]
                    index = index[0] if index else 0
                    if index>0:
                        self.gtmTags.append(GA4Event(pixel[1], ga4SettingName))
                    else:
                        self.gtmTags.append(CustomTemple(pixel[1], snippet))
                    #temple = {'name': pixel[1], 'type': 'html', 'parameter': [{'type': 'template', 'key': 'html', 'value': snippet}]}
                    self.gtmTags[-1].setProperty('parentFolderId', folders[index]['folderId'])
                    self.gtmTags[-1].setProperty('firingTriggerId', ['2147479553'])
                    self.gtmTags[-1].setProperty('blockingTriggerId', triggersID[index])
                        
                        #temple['firingTriggerId']   = ['2147479553']
                        #temple['blockingTriggerId'] = triggersID[index]
                        #temple['parentFolderId']    = folders[index]['folderId']
                    if self.existTag(tags, pixel[1]):
                        while True:
                            try:
                                self.gtmService.updateTag(self.workspace['path']+'/tags/%s'%otherID[index], self.gtmTags[-1].temple)
                            except HttpError:
                                print("GTM: Don't hurry me, please. Go us so fast!!!")
                                time.sleep(60)
                                self.gtmService.updateTag(self.workspace['path']+'/tags/%s'%otherID[index], self.gtmTags[-1].temple)
                            break
                    else:
                        while True:
                            try:
                                self.gtmService.createTag(self.workspace['accountId'], self.workspace['containerId'], self.workspace['workspaceId'], self.gtmTags[-1].temple)
                            except HttpError:
                                print("GTM: Don't hurry me, please. Go us so fast!!!")
                                time.sleep(60)
                                self.gtmService.createTag(self.workspace['accountId'], self.workspace['containerId'], self.workspace['workspaceId'], self.gtmTags[-1].temple)
                            break
        self.lanchPopUps('Tagging', 'The Measurement Strategy\n had been implemented!', 'Press "Ok" to exit.')
        self.tagProgress.set(100)    
        self.btn_loadTags.configure(state='active')
        self.btn_gtmConnect.configure(state='active')
        self.btn_tagging.configure(state='active')
        
    def existTag(self, tags, tagName):
        date = self.getDateFromName(tagName)
        for tag in tags:
            if tag['name'] == tagName: 
                return True
            else:
                if tagName.replace(date, '') in tag['name']: return True
        else:
            return False
        
    def existTrigger(self, triggers, triggerName):
        date = self.getDateFromName(triggerName)
        for trigger in triggers:
            if trigger['name'] == triggerName: 
                return True
            else:
                    if triggerName.replace(date, '') in trigger['name']:
                        return True
        else:
            return False
        
    def existVariable(self, variables, variableName):
        print('Variables: ', variables)
        print('Variable Name: ', variableName)
        try:
            for variable in variables:
                if variable['name'] == variableName: 
                    return True
            else:
                return False
        except:
            for variable in variables:
                if variable.temple['name'] == variableName: 
                    return True
            else:
                return False
        
    def getDateFromName(self, name):
        try:
            date = re.findall(r'_Jan\d{4}|_Feb\d{4}|_Mar\d{4}|_Apr\d{4}|_May\d{4}|_\d{4}|_Jun\d{4}|_Jul\d{4}|_Aug\d{4}|_Sep\d{4}|_Oct\d{4}|_Nov\d{4}|_Dec\d{4}', name)[0]
        except:
            date = ''
        return date
              
        
    def getTagId(self, tags, tagName):
        date = self.getDateFromName(tagName)
        for tag in tags:
            if tag['name'] == tagName: 
                return tag['tagId']
            else:
                    if tagName.replace(date, '') in tag['name']:
                        return tag['tagId']
        else:
            return ''
        
    def getTriggerId(self, triggers, triggerName):
        date = self.getDateFromName(triggerName)
        for trigger in triggers:
            if trigger['name'] == triggerName: 
                return trigger['triggerId']
            else:
                    if triggerName.replace(date, '') in trigger['name']:
                        return trigger['triggerId']
        else:
            return ''
        
    def getVariableId(self, pixelVars, varName):
        for pvar in pixelVars:
            if pvar['name'] == varName:
                return pvar['variableId']
        else:
            return ''
          
    def getTypeTrigger(self, nameTrigger):
        advertiser, trigger, date = nameTrigger.split('_')
        if re.findall(r'PV$', trigger):
            return 'PV'
        elif re.findall(r'Scroll\d{1,2}_$', trigger):
            return re.findall(r'Scroll\d{1,2}_$', trigger)[0]
        elif re.findall(r'T\d+ss$', trigger):
            return re.findall(r'T\d+ss$', trigger)[0]
        return ''
        
    def set_search(self):
        self.webDOM.setSearchXML(self.searchXML.get())
        
    def set_programmatic(self, platform):
        optionPlatform = ''
        if platform == 3 and self.__getattribute__('platform%s'%PLATFORMS_ADS[3].capitalize()).get():
            measurementID = ''
            while True:
                measurementID = self.windowRequestData('GA4 Measurement ID', 'Please enter the GA4 ID: ')
                try:
                    validMeasurementID = False if not re.findall(r'^G-\w{10}$', measurementID) else True
                except:
                    validMeasurementID = False
                if measurementID != None and measurementID != '' and validMeasurementID:
                    if not hasattr(self, '%sMeasurementID'%PLATFORMS_ADS[3]):
                        self.__setattr__('%sMeasurementID'%PLATFORMS_ADS[3], measurementID)
                        print(self.__getattribute__('%sMeasurementID'%PLATFORMS_ADS[3]))
                    else:
                        setattr(self, '%sMeasurementID'%PLATFORMS_ADS[3], measurementID)
                        #self.__getattribute__('%sMeasurementID'%PLATFORMS_ADS[3]) = measurementID
                        print(self.__getattribute__('%sMeasurementID'%PLATFORMS_ADS[3]))
                    break
                    #return 0
                elif measurementID == None:
                    self.__getattribute__('platform%s'%PLATFORMS_ADS[3].capitalize()).set(False)
                    return -1       
        for platform_ in PLATFORMS_ADS:
            if self.__getattribute__('platform%s'%platform_.capitalize()).get(): optionPlatform += platform_.capitalize()+'/'
        if optionPlatform == '':
            optionPlatform = 'Programmatic'
            self.__getattribute__('platform%s'%PLATFORMS_ADS[0].capitalize()).set(True)
            self.platformAdsList = [optionPlatform]
            self.platformList = PLATFORMS_BASE
        else:
            optionPlatform = optionPlatform[:-1]
            if self.__getattribute__('platform%s'%PLATFORMS_ADS[0].capitalize()).get() and optionPlatform not in self.platformAdsList:  self.platformAdsList = ['Programmatic', optionPlatform]
            else: self.platformAdsList = [optionPlatform]
            self.platformList = []
            for platform in optionPlatform.split('/'):
                if platform == 'Programmatic':
                    for platformBase in PLATFORMS_BASE:
                        self.platformList.append(platformBase)
                else:
                    self.platformList.append(platform)
        self.listPlatformAds['values'] = self.platformAdsList
        self.platforms['values'] = self.platformList
        self.listPlatformAds.set(optionPlatform)
        self.platforms.set(self.platformList[0])
        return 0
    
    def set_maxCategories(self, event=None):
        self.maxCategory.set(self.maxCategory.get())
        self.webDOM.setMaxCategories(self.maxCategory.get())
        self.deleteItemsTreeView()

    def set_sizeWord(self, event=None):
        self.minSizeWord.set(self.minSizeWord.get())
        self.webDOM.setSizeWord(self.minSizeWord.get())
    
    def set_maxLandings(self, event=None):
        """This method implement the require actions thatTagBuilder neet to do when the MUD parameter is fixed.

        Args:
            event (event, optional): Event with the details of the action. Defaults to None.
        """        
        self.maxLandings.set(self.maxLandings.get())
        self.webDOM.setMaxLandings(self.maxLandings.get())
        
    def set_landingsBy(self, event=None):
        self.webDOM.setLandingsBy(int(self.landingsBy.get()))
        self.deleteItemsTreeView()
        
    def set_fixedPaths(self, event=None):
        if int(self.fixedPaths.get())>0:
            paths = urlparse(self.urlAdvertiser.get()).path.replace('.html','').replace('.php','').split('/')
            self.webDOM.deleteItemList(paths, '')
            if len(paths)>0:
                if int(self.fixedPaths.get())>len(paths):
                    self.fixedPath.set(urlparse(self.urlAdvertiser.get()).path.replace('.html','').replace('.php',''))
                    self.fixedPaths.set(len(paths))
                else:
                    path = ''
                    for i in range(int(self.fixedPaths.get())):
                        path += '/' + paths[i]
                    else:
                        self.fixedPath.set(path)
            else:
                #self.lanchPopUps('Path Error', "The homepage doesn't have paths", 'Press "Ok" to exit.')
                self.fixedPath.set('/')
                self.fixedPaths.set(0)
        else:
            self.fixedPath.set('/')
        self.webDOM.setFixedPaths(self.fixedPath.get())
        self.deleteItemsTreeView()

    def deleteBranch(self, event):
        for item_ in self.dataTable.selection():
            if self.dataTable.parent(item_)=='':
                print(self.dataTable.item(item_))
                print(self.dataTable.focus())
                index = self.webDOM.mainSections.index(self.dataTable.focus())
                print(self.webDOM.arraySections[index-1][:2])
                remove_ = list(self.dataTable.selection())
                remove_.remove(item_)
                self.dataTable.selection_remove(remove_)
                break
        for item_ in self.dataTable.selection():
            if self.dataTable.parent(item_)=='':
                print('You will delete a section!')
                index = self.webDOM.mainSections.index(self.dataTable.focus())
                if index>0:
                    for url in self.webDOM.arraySections[index-1]:
                        url_ = urlparse(url)
                        if url_ in self.webDOM.subDomains: self.webDOM.subDomains.remove(url_)
                    self.webDOM.mainSections.pop(index)
                    self.webDOM.arraySections.pop(index-1)
                    self.dataTable.delete(item_)
            else:
                section = self.dataTable.parent(item_)
                index = self.webDOM.mainSections.index(section)
                values = self.dataTable.item(item_,'values')
                if index>0:
                    url_ = urlparse(values[0])
                    if url_ in self.webDOM.subDomains: self.webDOM.subDomains.remove(url_)
                    self.webDOM.arraySections[index-1].remove(values[0])
                    self.dataTable.delete(item_)
                print('You will delete a item!')
        #self.dataTable.delete(s)
        print("Are you sure that perform this action?")
    
    def find(self):
        if self.validURL(self.urlAdvertiser.get()):
            subDomains = []
            if self.builtBy.get() != 'path': return self.lanchPopUps('Building!', "This Building Sitemap way hasn't implemented yet!", 'Press "Ok" to exit.')
            self.btn_sections.configure(state='disable')
            self.btn_save.configure(state='disable')
            if self.mss.get():
                self.marionette.set(True)
                self.showMarionette()
                self.webDOM.resetDriver(self.urlAdvertiser.get(), True)
                url = self.webDOM.driver.current_url
                while self.mss.get():
                    if url != self.webDOM.driver.current_url and self.webDOM.driver.current_url not in subDomains:
                        subDomains.append(self.webDOM.driver.current_url)
                        url = self.webDOM.driver.current_url    
            self.webDOM.setScheme(self.scheme.get())
            self.webDOM.viewProgress = 1
            self.updateProgress_threaded()
            self.webDOM.setStop(False)
            self.btn_find.configure(state='disable')
            #self.maxCategories.configure(state='disable')
            self.btn_stop.configure(state='active')
            self.deleteItemsTreeView()
            #existContainer, containerID = self.pixelBot.existGTM(self.urlAdvertiser.get())
            existContainer, containerID = self.webDOM.existGTM(self.urlAdvertiser.get())
            self.GTM_ID.set(containerID)
            #agregar argumento para el path fijo a tener en cuenta
            fixedPath = self.fixedPath.get() if int(self.fixedPaths.get())>0 else None
            exists_url, exists_sitemap = self.webDOM.buildSiteMap(self.urlAdvertiser.get(), fixedPath)
            if exists_url:
                for url in subDomains:
                    self.webDOM.addSubDomain(url)
                if exists_sitemap and len(self.webDOM.subDomains)>0:
                    self.lanchPopUps('Landings', 'The process of find landings has finished!', 'Press "Ok" to exit.')
                else:
                    self.webDOM.findAnchors(fixedPath)
                    self.webDOM.getSubDomains()
                    self.webDOM.deeperSubDomains(fixedPath)
                    exist_sitemap = True if len(self.webDOM.subDomains)>0 else False 
                    if exist_sitemap:
                        self.lanchPopUps('Landings', 'The process of find landings has finished!', 'Press "Ok" to exit.')
                    else:
                        self.lanchPopUps('Landings', 'TagBuilder does not find landings!', 'Press "Ok" to exit.')
            else:
                self.lanchPopUps('URL Error!', "The URL given not found or it's incorrect!", 'Press "Ok" to exit.')
            self.btn_find.configure(state='active')
            self.btn_sections.configure(state='active')
            self.webDOM.viewProgress = -1
            #self.maxCategories.configure(state='active')
        else:
            self.lanchPopUps('URL Error!', "The URL given is incorrect!", 'Press "Ok" to exit.')
        
    def stopSearch(self):
        self.btn_stop.configure(state='disable')
        self.webDOM.setStop(True)
        self.viewProgress.set(0)
        self.webDOM.viewProgress = 0
        self.btn_find.configure(state='active')
        self.btn_stop.configure(state='active')
    
    def deep(self):
        self.webDOM.deeperSubDomains()
        
    def draw(self):
        self.btn_find.configure(state='disable')
        self.btn_stop.configure(state='disable')
        self.btn_sections.configure(state='disable')
        self.btn_save.configure(state='disable')
        if self.validAdvertiserName():
            if len(self.webDOM.subDomains)>1:
                self.webDOM.getArraySections()
                self.addItemTreeView(self.webDOM.arraySections)
                self.lanchPopUps('Sectioned', 'The process of categorized has finished!', 'Press "Ok" to exit.')
            else:
                self.webDOM.mainSections = ['', 'Otros']
                self.webDOM.arraySections = [['/']]
                self.addItemTreeView(self.webDOM.arraySections)
                self.lanchPopUps('Not enough!', "There aren't enough landings!", 'Press "Ok" to exit.')
        else:
            self.lanchPopUps('Field Required!', 'The Advertiser Name is not valid!', 'Press "Ok" to exit.')
        self.btn_find.configure(state='active')
        self.btn_stop.configure(state='active')
        self.btn_sections.configure(state='active')
        self.btn_save.configure(state='active')
            
    def createPixels(self):
        try:
            self.btn_create.configure(state='disable')
            if self.directoryTR.get() == '' or not self.advertiserId.get().isdigit() or self.advertiser_.get() == '' or self.advertiser_.get() == 'None':
                self.lanchPopUps('Incomplete Fields', 'Check the  fields:\n- T. Request File.\n- Advertiser.\n- Advertiser ID.', 'Press "Ok" to exit.')
            else:
                if self.platforms.get() == 'Xandr Seg' or self.platforms.get() == 'Xandr Conv':
                    self.pixelProgress.set(0)
                    pixelType = 'RTG' if self.platforms.get() == 'Xandr Seg' else 'CONV'
                    if self.logInPlatform(LOGIN_PAGES[0], self.users[0].get(), self.passwords[0].get()):
                        self.pixelProgress.set(2)
                        if not self.pixelBot.setMarketXandr(self.countries.get()): 
                            self.btn_create.configure(state='active')
                            return self.lanchPopUps('Access', "You don't have access to this market", 'Press "Ok" to exit.') 
                        self.pixelProgress.set(5)
                        if self.pixelBot.existAdvertiserId(self.platforms.get(), self.advertiserId.get()):
                            progress = 7
                            self.pixelProgress.set(progress)
                            self.xandrSeg, self.xandrConv = ([], self.xandrConv) if pixelType=='RTG' else (self.xandrSeg, [])
                            step = (90/len(self.arrayPixels)) if len(self.arrayPixels)>0 else 90
                            for pixel in self.arrayPixels:
                                if pixelType == 'RTG' and (pixel[7]==None or pixel[7]=='' or pixel[7]=='NO'):
                                    self.xandrSeg.append('NO')
                                elif pixelType == 'CONV' and (pixel[8]==None or pixel[8]=='' or pixel[8]=='NO'):
                                    self.xandrConv.append('NO')   
                                else:
                                    if not self.pixelBot.existPixel(self.platforms.get(), self.advertiserId.get(), pixel[1]):
                                        snippet =  self.pixelBot.createPixel(self.advertiserId.get(), pixel[1], platform=0, pixelType=pixelType)
                                        #pixel.append(snippet)
                                        self.xandrSeg.append(snippet) if pixelType=='RTG' else self.xandrConv.append(snippet)
                                    else:
                                        snippet = self.pixelBot.getSnippetCode(self.advertiserId.get(),pixel[1], self.platforms.get())
                                        self.xandrSeg.append(snippet) if pixelType=='RTG' else self.xandrConv.append(snippet)
                                        #self.lanchPopUps('Pixel Exists!', 'The pixel, %s, exists.'%pixel[1], 'Press "Ok" to exit.')
                                progress += step
                                self.pixelProgress.set(progress)
                            self.lanchPopUps('Finished', 'Process of create Pixels have already finished.', 'Press "Ok" to exit.')
                            self.pixelProgress.set(100)
                        else:
                            self.pixelProgress.set(0)
                            self.btn_create.configure(state='active')
                            return self.lanchPopUps('Not founded!', "The advertiser can't founded!", 'Press "Ok" to exit.')
                    else:
                        self.btn_create.configure(state='active')
                        return self.lanchPopUps('Xandr login failed!', 'Check your credentials, please.', 'Press "Ok" to exit.')
                elif self.platforms.get() == 'DV360':
                    self.pixelProgress.set(0)
                    if self.logInPlatform(LOGIN_PAGES[1], self.users[0].get(), self.passwords[1].get()):
                        self.pixelProgress.set(2)
                        if self.pixelBot.existAdvertiserId(self.platforms.get(), self.advertiserId.get()):
                            self.DV360 = []
                            progress = 5
                            self.pixelProgress.set(progress)
                            step = (90/len(self.arrayPixels)) if len(self.arrayPixels)>0 else 90
                            for pixel in self.arrayPixels:
                                if pixel[9] in [None,'','No','NO','no', 'nO']:
                                    self.DV360.append('NO')
                                else:
                                    if not self.pixelBot.existPixel(self.platforms.get(), self.advertiserId.get(), pixel[1]):
                                        fitVariables = self.fitCustomVariables(pixel[3])
                                        #snippet =  self.pixelBot.createPixel(self.advertiserId.get(), pixel[1], platform=1, customVariable=pixel[3])
                                        snippet =  self.pixelBot.createPixel(self.advertiserId.get(), pixel[1], platform=1, customVariable=fitVariables)
                                        snippet = sM.extractCode(r'<img.*/>', snippet)
                                        self.DV360.append(snippet)
                                        #pixel.append(snippet)
                                    else:
                                        snippet = self.pixelBot.getSnippetCode(self.advertiserId.get(),pixel[1], self.platforms.get())
                                        snippet = sM.extractCode(r'<img.*/>', snippet)
                                        self.DV360.append(snippet)
                                        #self.lanchPopUps('Pixel Exists!', 'The pixel, %s, exists.'%pixel[1], 'Press "Ok" to exit.')
                                progress += step
                                self.pixelProgress.set(progress)
                            self.lanchPopUps('Finished', 'Process of create Pixels have already finished.', 'Press "Ok" to exit.')
                            self.pixelProgress.set(100)
                        else:
                            self.pixelProgress.set(0)
                            self.lanchPopUps('Not founded!', "The advertiser can't founded!", 'Press "Ok" to exit.')
                    else:
                        self.lanchPopUps('DV360 login failed!', 'Check your credentials, please.', 'Press "Ok" to exit.')
                elif self.platforms.get() == 'Taboola Seg' or self.platforms.get() == 'Taboola Conv':
                    self.pixelProgress.set(0)
                    pixelType = 'RTG' if self.platforms.get() == 'Taboola Seg' else 'CONV'
                    if self.logInPlatform(LOGIN_PAGES[2], self.users[0].get(), self.passwords[2].get()):
                        self.pixelProgress.set(2)
                        if self.pixelBot.existAdvertiserId(self.platforms.get(), self.advertiserId.get()):
                            self.pixelProgress.set(5)
                            if self.pixelBot.existTaboolaPixel(self.advertiserId.get()):
                                progress = 7
                                self.pixelProgress.set(progress)
                                step = (90/len(self.arrayPixels)) if len(self.arrayPixels)>0 else 90
                                self.taboolaSeg, self.taboolaConv = ([], self.taboolaConv) if pixelType=='RTG' else (self.taboolaSeg, [])
                                for pixel in self.arrayPixels:
                                    pixel[10] = 'NO' if pixel[10] == None else pixel[10]
                                    pixel[11] = 'NO' if pixel[11] == None else pixel[11]
                                    if pixelType == 'RTG' and pixel[10] in ['NO', 'No', 'no', 'nO', '', None]:
                                    #if pixelType == 'RTG' and pixel[9].casefold() not in ['url', 'event']:
                                        self.taboolaSeg.append('NO')
                                    #elif pixelType == 'CONV' and pixel[10].casefold() not in ['url', 'event']:
                                    elif pixelType == 'CONV' and pixel[11] in ['NO', 'No', 'no', 'nO', '', None]:
                                        self.taboolaConv.append('NO')
                                    else:
                                        event   = True if (pixelType == 'RTG' and pixel[10] in ['Event', 'event', 'EVENT']) or (pixelType == 'CONV' and pixel[11] in ['Event', 'event', 'EVENT']) else False
                                        #event   = True if (pixelType == 'RTG' and pixel[9].casefold() == 'event') or (pixelType == 'CONV' and pixel[10].casefold() == 'event') else False
                                        pathURL = pixel[4] if not event else None
                                        #if self.pixelBot.existPixel(self.platforms.get(), self.advertiserId.get(), pixel[1]): self.lanchPopUps('Pixel Exists!', "The pixel %s already existed!"%pixel[1], 'Press "Ok" to exit.')
                                        snippet =  self.pixelBot.createPixel(self.advertiserId.get(), pixel[1], platform=2, pixelType=pixelType, event_=event, pathURL=pathURL)
                                        self.taboolaSeg.append(snippet) if pixelType=='RTG' else self.taboolaConv.append(snippet)
                                    progress += step
                                    self.pixelProgress.set(progress)
                                self.lanchPopUps('Finished', 'Process of create Pixels have already finished.', 'Press "Ok" to exit.')
                                self.pixelProgress.set(100)
                            else:
                                self.lanchPopUps('Universal Pixel!', "The Taboola Universal Pixel hasn't implemented yet!", 'Press "Ok" to exit.')
                                self.pixelProgress.set(0)
                        else:
                            self.lanchPopUps('Not founded!', "The advertiser can't founded!", 'Press "Ok" to exit.')
                            self.pixelProgress.set(0)
                    else:
                        self.lanchPopUps('Taboola login failed!', 'Check your credentials, please.', 'Press "Ok" to exit.')
                    #self.createPixel(self.platforms.get(), 'AllPagesTest', None)
                elif self.platforms.get().casefold() in PLATFORMS_ADS:
                    self.lanchPopUps('Not Implemented!', 'You have been selected a platform in process to be implemented.', 'Press "Ok" to exit.')
                else:
                    self.pixelProgress.set(0)
                    if self.logInPlatform(LOGIN_PAGES[3], self.users[0].get(), self.passwords[3].get()):
                        self.pixelProgress.set(2)
                        minsightId = self.pixelBot.existMinsightsId(self.advertiser_.get(), self.countries.get(), self.agencies.get())
                        if minsightId != -1:
                            progress = 7
                            self.pixelProgress.set(5)
                            step = (90/len(self.arrayPixels)) if len(self.arrayPixels)>0 else 90
                            self.advertiserId.set(minsightId)
                            self.minsights = []
                            self.pixelProgress.set(progress)
                            for pixel in self.arrayPixels:
                                if pixel[6] in [None,'','No','NO','no', 'nO', '']:
                                    self.minsights.append('NO')
                                else:
                                    if not self.pixelBot.existPixel(self.platforms.get(), self.advertiserId.get(), pixel[1]):
                                        #print('El pixel: '+pixel[1]+', no existe y se puede crear!!!')
                                        fitVariables = self.fitCustomVariables(pixel[3])
                                        print("Las variables ajustadas son: ", fitVariables)
                                        print("Las variables ajustadas son: ", fitVariables)
                                        print("Las variables ajustadas son: ", fitVariables)
                                        #snippet =  self.pixelBot.createPixel(self.advertiserId.get(), pixel[1], platform=3, customVariable=pixel[3])
                                        snippet =  self.pixelBot.createPixel(self.advertiserId.get(), pixel[1], platform=3, customVariable=fitVariables)
                                        self.minsights.append(snippet)
                                        #pixel.append(snippet)
                                    else:
                                        snippet = self.pixelBot.getSnippetCode(self.advertiserId.get(),pixel[1], self.platforms.get())
                                        self.minsights.append(snippet)
                                        #self.lanchPopUps('Pixel Exists!', 'The pixel, %s, exists.'%pixel[1], 'Press "Ok" to exit.')
                                progress += step
                                self.pixelProgress.set(progress)
                            self.lanchPopUps('Finished', 'Process of create Pixels have already finished.', 'Press "Ok" to exit.')
                            self.pixelProgress.set(100)
                        else:
                            self.lanchPopUps('Not founded!', "The advertiser can't founded!", 'Press "Ok" to exit.')
                            self.pixelProgress.set(0)
                    else:
                        self.lanchPopUps('Minsights login failed!', 'Check your credentials, please.', 'Press "Ok" to exit.')
            self.btn_create.configure(state='active')
            self.btn_save_pixels.configure(state='active')
        except:
            print(sys.exc_info())
            self.lanchPopUps('Error!', str(sys.exc_info()[1]), 'Press "Ok" to exit.')
            self.btn_create.configure(state='active')
        
    def createPixel(self, platform_, pixelName_, variables):
        if platform_ == 'Xandr Seg':
            if self.advertiserId.get() != '' and self.advertiserId.get().isnumeric():
                snippet = self.pixelBot.createPixel(self.advertiserId.get(), pixelName_)
                #Add validation of snippet code and then to continue with following instructions
                self.xlsxFile.setPATH(self.directoryTR.get())
                self.xlsxFile.setBook()
                self.xlsxFile.setSheet('Home')
                self.xlsxFile.writeCell('J31',snippet)
                self.xlsxFile.saveBook()
                print(snippet)
            else:
                print('revise el Advertiser ID')
        elif platform_ == 'Xandr Conv':
            if self.advertiserId.get() != '' and self.advertiserId.get().isnumeric():
                snippet = self.pixelBot.createPixel(self.advertiserId.get(), pixelName_, pixelType='CONV')
                #Add validation of snippet code and then to continue with following instructions
                self.xlsxFile.setPATH(self.directoryTR.get())
                self.xlsxFile.setBook()
                self.xlsxFile.setSheet('Home')
                self.xlsxFile.writeCell('J31',snippet)
                self.xlsxFile.saveBook()
                print(snippet)
            else:
                print('revise el Advertiser ID')
        elif platform_ == 'DV360':
            if self.advertiserId.get() != '' and self.advertiserId.get().isnumeric():
                snippet = self.pixelBot.createPixel(self.advertiserId.get(), pixelName_, 1)
                #Add validation of snippet code and then to continue with following instructions
                self.xlsxFile.setPATH(self.directoryTR.get())
                self.xlsxFile.setBook()
                self.xlsxFile.setSheet('Home')
                self.xlsxFile.writeCell('J31',snippet)
                self.xlsxFile.saveBook()
                print(snippet)
            else:
                print('revise el Advertiser ID')
        elif platform_ == 'Taboola':
            if self.advertiserId.get() != '' and self.advertiserId.get().isnumeric():
                snippet = self.pixelBot.createPixel(self.advertiserId.get(), pixelName_, 2, pixelType='CONV')
                #Add validation of snippet code and then to continue with following instructions
                self.xlsxFile.setPATH(self.directoryTR.get())
                self.xlsxFile.setBook()
                self.xlsxFile.setSheet('Home')
                self.xlsxFile.writeCell('J31',snippet)
                self.xlsxFile.saveBook()
                print(snippet)
            else:
                print('revise el Advertiser ID')
        elif platform_ == 'Minsights':
            pass
     
    def createPixelsAll(self):
        while not self.existAllCredentials() or self.setWindow.winfo_exists():
            if not self.setWindow.winfo_exists():
                self.settingWindow()  
        for platform, user, password in zip(LOGIN_PAGES, self.users, self.passwords):
            login = False
            self.pixelBot.setDriver(platform)
            self.windowCode = False
            try_ = 0
            while True:
                login = self.pixelBot.doLogin(user.get(), password.get())
                if self.pixelBot.reqCode and (not self.windowCode): 
                    self.updateCodeVerify_threaded()
                    self.windowCode = True
                self.pixelBot.authFail = self.pixelBot.auth_alert()
                if login or self.pixelBot.authFail:
                    if self.pixelBot.authFail:
                        print('Ha habido un problema de authenticación')
                        if try_<2:
                            self.pixelBot.setDriver(platform)
                            try_+=3
                        else:
                            print('Ha habido un problema de authenticación')
                            break
                    else:
                        break
                elif self.pixelBot.approve:
                    print('Aprueba el ingreso por favor')
                elif not login and not self.pixelBot.startLog:
                    break
    
    """
        This method implement de Log-In Xandr platform.
        Return:
            LogIn:  Boolean
    """         
    def logInPlatform(self, loginPage, user, password):
        login = False
        windowCode = False
        try_ = 0
        self.pixelBot.setDriver(loginPage)
        while not login:
            login = self.pixelBot.doLogin(user, password)
            #self.pixelBot.authFail = self.pixelBot.auth_alert()
            if self.pixelBot.approve:
                self.lanchPopUps('Authorize', 'Authoriza the Access from your cellphone!', 'Press "Ok" to exit.')
                self.pixelBot.approve = False
            elif self.pixelBot.reqCode and not windowCode and self.pixelBot.isVerifyPage():
                windowCode = True
                self.updateCodeVerify_threaded()
                #self.updateCodeVerify()
            elif self.pixelBot.auth_alert(time_=2):
                if try_<2:
                    self.pixelBot.setDriver(loginPage)
                    windowCode = False
                    try_+=1
                else:
                    self.lanchPopUps('Auth Failed', 'There was a authentication problem!', 'Press "Ok" to exit.')
                    break
            elif not login and not self.pixelBot.startLog:
                break
        return login
    
    def loginAllPlatforms(self):
        self.logInPlatform(LOGIN_PAGES[0], self.users[0].get(), self.passwords[0].get())
        self.logInPlatform(LOGIN_PAGES[1], self.users[0].get(), self.passwords[1].get())
        self.logInPlatform(LOGIN_PAGES[2], self.users[0].get(), self.passwords[2].get())
        self.logInPlatform(LOGIN_PAGES[3], self.users[0].get(), self.passwords[3].get())

    def updateCodeVerify(self):
        alertWin = tk.Tk()
        alertWin.withdraw()
        self.pixelBot.code = simpledialog.askstring('Verification','What is the code?',parent=alertWin)
        alertWin.destroy()
        
    def windowRequestData(self, title, message):
        alertWin = tk.Tk()
        alertWin.withdraw()
        data = simpledialog.askstring(title, message,parent=alertWin)
        alertWin.destroy()
        return data
    
    def validsSections(self, mainSections, arraySections):
        sections = []

    def pixels(self):
        """This function get the parameters of the pixels to implement from TR file.
            Parameters:
                None:   None.
            Return:
                None: None. 
        """      
        self.btn_pixels.configure(state='disable')
        if self.validTRFile():
            #self.arrayPixels = self.getArrayPixels()
            self.addItemTreeViewII(self.getArrayPixels())
            self.lanchPopUps('Extracted!', 'The pixels had read from TR!', 'Press "Ok" to exit.')
        else:
            self.lanchPopUps('Invalid File', 'You must choice a valid file!', 'Press "Ok" to exit.')
        self.btn_create.configure(state='active')
        self.btn_pixels.configure(state='active')

    def validTRFile(self, prefix=''):
        """This method valids if a file choosen is valid or not.

        Args:
            prefix (str, optional): Aditional text to diference TR file of TR Final File. Defaults to ''.

        Returns:
            Boolean: True or False.
        """        
        try:
            if self.directoryTR.get().split('/')[-1].startswith('TagReq_') and (self.directoryTR.get().split('/')[-1][-12:-9] in MONTHS) and self.directoryTR.get().split('/')[-1][-9:-5].isnumeric():
                return True
            elif self.directoryTRF.get().split('/')[-1].startswith('TagReq'+prefix+'_') and (self.directoryTRF.get().split('/')[-1][-12:-9] in MONTHS) and self.directoryTRF.get().split('/')[-1][-9:-5].isnumeric():
                return True
            else:
                return False
        except:
            return False
    
    def getArrayPixels(self, starColumn=PIXEL_SETTING_COLUMNS[0], endColumn=PIXEL_SETTING_COLUMNS[1]):
        """This function reads the TR file and get the differents pixels that we need to implement.

        Returns:
            Pixels: Array of information about all pixels to implement extracted from the file.
        """
        pixels = []
        for sheetname in self.xlsxFile.book.sheetnames:
            self.xlsxFile.setSheet(sheetname)
            flat, cell, indexes = True, 'E31', [1, 0, 3, 2, 4, 5, 6, 7, 8, 9, 10]
            if self.xlsxFile.readCell(cell) in [None, '']: flat = False
            if sheetname in ['Concept Tagging Request ', 'Hoja1', 'Listas']:
                continue
            if sheetname == 'Home' or sheetname == 'Funnel':
                while flat:
                    dataPixel = []
                    pixels.append([])
                    #pixels[-1].insert(0,'General')
                    pixels[-1].insert(0, sheetname)
                    row = int(re.findall(r'\d+', cell)[0])
                    table = self.xlsxFile.sheet._cells_by_row(starColumn, row, endColumn, row)
                    for r in table:
                        for c in r:
                            dataPixel.append(c.value)
                    for index in indexes:
                        if index == 2 and 'PV_' in dataPixel[1] and not 'Home' in dataPixel[1] and not 'AllPages' in dataPixel[1]:
                            path_ = urlparse(dataPixel[index]).path.split('/')
                            self.webDOM.deleteItemList(path_, '')
                            self.webDOM.deleteSubPaths(path_)
                            try:
                                pixels[-1].append('/'+path_[0])
                            except:
                                pixels[-1].append(None)
                        else:
                            pixels[-1].append(dataPixel[index])
                    pixels[-1].append(cell)
                    cell, value = self.xlsxFile.readNextCell(cell)
                    if value in [None, '']: flat = False
            else:
                while flat:
                    dataPixel = []
                    pixels.append([])
                    pixels[-1].insert(0, sheetname)
                    row = int(re.findall(r'\d+', cell)[0])
                    table = self.xlsxFile.sheet._cells_by_row(starColumn, row, endColumn, row)
                    for r in table:
                        for c in r:
                            dataPixel.append(c.value)
                    for index in indexes:
                        if index == 2:
                            if sheetname == 'Otros':
                                pixels[-1].append('/')
                            else:
                                try:
                                    path_ = urlparse(self.xlsxFile.readCell('F31')).path.split('/')
                                    self.webDOM.deleteItemList(path_, '')
                                    self.webDOM.deleteSubPaths(path_)
                                    pixels[-1].append('/'+path_[0])
                                except:
                                    pixels[-1].append(None)
                        else:
                            pixels[-1].append(dataPixel[index]) 
                    pixels[-1].append(sheetname)
                    pixels[-1].append(cell)
                    cell, value = self.xlsxFile.readNextCell(cell)   
                    if value in [None, '']: flat = False    
        return pixels
    
    def save(self):
        if self.validGTMID():
            try:
                self.btn_save.configure(state='disable')
                self.xlsxFile.setPATH(self.pathTR.get())
                self.xlsxFile.setBook()
                deployGTM = 'No' if 'GTM-XXXXXXX' in self.GTM_ID.get() else 'Si'
                for sheet in ['Tagging Request', 'Funnel', 'Sections']:
                    self.xlsxFile.setSheet(sheet)
                    self.xlsxFile.writeCell('C13', self.advertiser.get(), ['left','center'])
                    self.xlsxFile.writeCell('C23', self.GTM_ID.get(), ['left','center'])
                    self.xlsxFile.writeCell('C21', deployGTM, ['left','center'])
                    if self.__getattribute__('platform%s'%PLATFORMS_ADS[3].capitalize()).get(): self.xlsxFile.writeCell('C24', self.__getattribute__('%sMeasurementID'%PLATFORMS_ADS[3]), ['left','center'])
                if len(self.webDOM.mainSections)>1: 
                    self.createSectionSheets(self.webDOM.mainSections[1:])
                else:
                    self.xlsxFile.setSheet('Tagging Request')
                    self.xlsxFile.sheet = self.xlsxFile.book['Tagging Request']
                    self.xlsxFile.sheet.title = 'Home'
                self.xlsxFile.setSheet('Home')
                cell = 'E31'
                styleFont = {'name':'Calibri', 'size':11, 'bold':True, 'italic':True, 'color':'FF000000'}
                for platform in PLATFORMS_ADS:
                    if self.__getattribute__('platform%s'%platform.capitalize()).get():
                        platform = '' if platform == 'programmatic' else platform
                        cell, row, column = self.xlsxFile.nextFreeCell(cell)
                        if cell != 'E31':
                            self.xlsxFile.sheet.merge_cells('B%d:B%d'%(row,row+1))
                            self.xlsxFile.sheet.merge_cells('B%d:B%d'%(row+2,row+3))
                            self.xlsxFile.writeCell('B'+str(row), 'Awareness', font_=styleFont)
                            self.xlsxFile.writeCell('B'+str(row+2), 'Consideration', font_=styleFont)
                            self.xlsxFile.fillCell('B'+str(row), PLATFORM_COLORS[platform])
                            self.xlsxFile.fillCell('B'+str(row+2), PLATFORM_COLORS[platform])
                            for r in range(4):
                                for c in COLUMNS:
                                    self.xlsxFile.fillCell(c+str(row+r), PLATFORM_COLORS[platform])
                        if platform == PLATFORMS_ADS[3] and self.__getattribute__('platform%s'%PLATFORMS_ADS[3].capitalize()).get(): self.xlsxFile.writeCell('I'+str(row), self.__getattribute__('%sMeasurementID'%PLATFORMS_ADS[3]))
                        self.xlsxFile.writeCell('C'+str(row), 'Home')
                        self.xlsxFile.writeCell('G'+str(row), 'u')
                        self.xlsxFile.writeCell('D'+str(row), 'Page View')
                        self.xlsxFile.writeCell('F'+str(row), self.urlAdvertiser.get())
                        self.xlsxFile.writeCell('E'+str(row), self.xlsxFile.getNameSection(self.advertiser.get(), 'Home'+platform.capitalize()))
                        cell, row, column = self.xlsxFile.nextFreeCell(cell)
                        if platform == PLATFORMS_ADS[3] and self.__getattribute__('platform%s'%PLATFORMS_ADS[3].capitalize()).get(): self.xlsxFile.writeCell('I'+str(row), self.__getattribute__('%sMeasurementID'%PLATFORMS_ADS[3]))
                        self.xlsxFile.writeCell('C'+str(row), 'Section')
                        self.xlsxFile.writeCell('D'+str(row), 'Page View')
                        self.xlsxFile.writeCell('F'+str(row), 'AllPages')
                        self.xlsxFile.writeCell('G'+str(row), 'u/p')
                        self.xlsxFile.writeCell('E'+str(row), self.xlsxFile.getNameSection(self.advertiser.get(), 'AllPages'+platform.capitalize(),'PV'))
                        cell, row, column = self.xlsxFile.nextFreeCell(cell)
                        if platform == PLATFORMS_ADS[3] and self.__getattribute__('platform%s'%PLATFORMS_ADS[3].capitalize()).get(): self.xlsxFile.writeCell('I'+str(row), self.__getattribute__('%sMeasurementID'%PLATFORMS_ADS[3]))
                        self.xlsxFile.writeCell('C'+str(row), 'Section')
                        self.xlsxFile.writeCell('D'+str(row), 'Scroll')
                        self.xlsxFile.writeCell('F'+str(row), 'AllPages')
                        self.xlsxFile.writeCell('G'+str(row), 'u/p')
                        self.xlsxFile.writeCell('E'+str(row), self.xlsxFile.getNameSection(self.advertiser.get(), 'AllPages'+platform.capitalize(),'Scroll%s'%self.scrollDeep.get()))
                        cell, row, column = self.xlsxFile.nextFreeCell(cell)
                        if platform == PLATFORMS_ADS[3] and self.__getattribute__('platform%s'%PLATFORMS_ADS[3].capitalize()).get(): self.xlsxFile.writeCell('I'+str(row), self.__getattribute__('%sMeasurementID'%PLATFORMS_ADS[3]))
                        self.xlsxFile.writeCell('C'+str(row), 'Section')
                        self.xlsxFile.writeCell('D'+str(row), 'Timer')
                        self.xlsxFile.writeCell('F'+str(row), 'AllPages')
                        self.xlsxFile.writeCell('G'+str(row), 'u/p')
                        self.xlsxFile.writeCell('E'+str(row), self.xlsxFile.getNameSection(self.advertiser.get(), 'AllPages'+platform.capitalize(),'T%sss'%self.timerLast.get()))
                cell, row, column = self.xlsxFile.nextFreeCell(cell)
                self.xlsxFile.sheet.merge_cells('B%d:B%d'%(row,row+1))
                self.xlsxFile.writeCell('B'+str(row), 'Microconversion', font_=styleFont)
                self.xlsxFile.fillCell('B'+str(row), PLATFORM_COLORS['microconvertion'])
                for r in range(2):
                    for c in COLUMNS:
                        self.xlsxFile.fillCell(c+str(row+r), PLATFORM_COLORS['microconvertion'])
                if len(self.webDOM.arraySections)>0: self.loadData(self.webDOM.arraySections)
                self.xlsxFile.book.remove(self.xlsxFile.book['Sections'])
                directory = filedialog.askdirectory()
                if len(directory) > 0:
                    self.directoryTR.set(self.xlsxFile.saveBook(directory))
                else:
                    self.directoryTR.set(self.xlsxFile.saveBook())
                    #self.xlsxFile.saveBook()
                self.advertiser_.set(self.advertiser.get())
                self.btn_save.configure(state='active')
                self.lanchPopUps('Save', 'The TagBuilder file has saved!', 'Press "Ok" to exit.')
            except PermissionError:
                self.lanchPopUps('PermissionError!', "The TR file is opened or don't\n have permission to save.", 'Press "Ok" to exit.')
                print(sys.exc_info())
            except:
                print(sys.exc_info())
                self.lanchPopUps('Error!', str(sys.exc_info()[1]), 'Press "Ok" to exit.')
        else:
            self.lanchPopUps('Fields missing!', 'Check the Container ID and Advertiser Name!', 'Press "Ok" to exit.')
    
    def savePixels(self):
        self.btn_save_pixels.configure(state='disable')
        snippet_Arrays = {'Xandr Seg': self.xandrSeg, 'Xandr Conv': self.xandrConv, 'DV360': self.DV360, 'Minsights': self.minsights, 'Taboola Seg': self.taboolaSeg, 'Taboola Conv': self.taboolaConv}
        try:
            flat, cell, pixelsHome = True, 'E31', 1
            self.xlsxFile.setSheet('Home')
            if self.xlsxFile.readCell(cell) in [None, '']: flat, pixelsHome = False, 0
            while flat:
                cell, value = self.xlsxFile.readNextCell(cell)
                flat, pixelsHome = (False, pixelsHome) if value in [None, ''] else (True, pixelsHome+1)
            print('El numero de pixeles en sheet home es: ', pixelsHome)
            flat, cell, pixelsFunnel = True, 'E31', pixelsHome+1
            self.xlsxFile.setSheet('Funnel')
            if self.xlsxFile.readCell(cell) in [None, '']: flat, pixelsFunnel = False, pixelsHome
            print("PixelsFunnel", pixelsFunnel)
            while flat:
                cell, value = self.xlsxFile.readNextCell(cell)
                flat, pixelsFunnel = (False, pixelsFunnel) if value in [None, ''] else (True, pixelsFunnel+1)
            print('El numero de pixeles en sheet Funnel es: ', pixelsFunnel-pixelsHome)
            print('*-*'*60)
            print('El número de pixeles es: ', len(self.arrayPixels))
            print(self.arrayPixels)
            for DSP in snippet_Arrays:
                index, indexSection, cellCol = 0, 4, 30
                #print('Pixel Setting: ',snippet_Arrays[DSP])    
                for snippet in snippet_Arrays[DSP]:
                    print('+-'*60)
                    print(indexSection)
                    print('El código del pixel %d es: '%index, snippet)
                    row = re.findall(r'\d+', self.arrayPixels[index][-1])[0]
                    if index<pixelsHome or index<pixelsFunnel:
                        if index<pixelsHome: 
                            self.xlsxFile.setSheet('Home')
                            index_ = index
                        else: 
                            self.xlsxFile.setSheet('Funnel')
                            index_ = index-pixelsHome     
                        if DSP == 'Xandr Seg':
                            self.xlsxFile.writeCell('J%s'%row, snippet) 
                            #cell = 'J%s'%str(cellCol+index_+1)
                            #self.xlsxFile.writeCell(cell, snippet)
                        elif DSP == 'Xandr Conv': 
                            self.xlsxFile.writeCell('K%s'%row, snippet)
                            #cell = 'K%s'%str(cellCol+index_+1)
                            #self.xlsxFile.writeCell(cell, snippet)
                        elif DSP == 'DV360':
                            self.xlsxFile.writeCell('L%s'%row, snippet) 
                            #cell = 'L%s'%str(cellCol+index_+1)
                            #self.xlsxFile.writeCell(cell, snippet)
                        elif DSP == 'Minsights': 
                            self.xlsxFile.writeCell('I%s'%row, snippet)
                            #cell = 'I%s'%str(cellCol+index_+1)
                            #self.xlsxFile.writeCell(cell, snippet)
                        elif DSP == 'Taboola Seg': 
                            self.xlsxFile.writeCell('M%s'%row, snippet)
                            #cell = 'M%s'%str(cellCol+index_+1)
                            #self.xlsxFile.writeCell(cell, snippet)
                        else: 
                            self.xlsxFile.writeCell('N%s'%row, snippet)
                            #cell = 'N%s'%str(cellCol+index_+1)
                            #self.xlsxFile.writeCell(cell, snippet)
                    else:
                        #self.xlsxFile.setSheet(self.xlsxFile.book.sheetnames[indexSection])
                        self.xlsxFile.setSheet(self.xlsxFile.book.sheetnames[self.xlsxFile.book.sheetnames.index(self.arrayPixels[index][-2])])
                        if DSP == 'Xandr Seg':
                            self.xlsxFile.writeCell('J%s'%row, snippet)
                            #self.xlsxFile.writeCell('J31', snippet)
                        elif DSP == 'Xandr Conv': 
                            self.xlsxFile.writeCell('K%s'%row, snippet)
                            #self.xlsxFile.writeCell('K31', snippet)
                        elif DSP == 'DV360': 
                            self.xlsxFile.writeCell('L%s'%row, snippet)
                            #self.xlsxFile.writeCell('L31', snippet)
                        elif DSP == 'Minsights': 
                            self.xlsxFile.writeCell('I%s'%row, snippet)
                            #self.xlsxFile.writeCell('I31', snippet)
                        elif DSP == 'Taboola Seg':
                            self.xlsxFile.writeCell('M%s'%row, snippet) 
                            #self.xlsxFile.writeCell('M31', snippet)
                        else: 
                            self.xlsxFile.writeCell('N%s'%row, snippet)
                            #self.xlsxFile.writeCell('N31', snippet)
                        indexSection += 1
                    index += 1  
            print('¡Hemos llegado hasta aquí!')
            directory = filedialog.askdirectory()
            print(directory)
            if len(directory) > 0:
                self.xlsxFile.setSheet('Home')
                self.directoryTR.set(self.xlsxFile.saveBook(directory, False))
                self.lanchPopUps('Save', 'The Tagging Request file has saved!', 'Press "Ok" to exit.')
            else:
                self.lanchPopUps('Save Error', 'You need to choose a directory!', 'Press "Ok" to exit.')
        except PermissionError:
            self.lanchPopUps('Permission Error!', "The file is open or you haven't permissions.", 'Press "Ok" to exit.')
        except:
            #self.lanchPopUps('Error!', str(sys.exc_info()[1]), 'Press "Ok" to exit.')
            self.lanchPopUps('Error!', sys.exc_info(), 'Press "Ok" to exit.')
        self.btn_save_pixels.configure(state='active')
      
    def updateProgress_threaded(self):
        thread = Thread(target = self.updateProgress)
        thread.start()

    def updateProgress(self):
        while self.webDOM.viewProgress > 0:
            self.viewProgress.set(self.webDOM.viewProgress)
            time.sleep(1)
        else:
            print('Se ha finalizado este hilo de seguimiento')
            time.sleep(10)
            self.viewProgress.set(0)
    
    def updateSnipetCodes(self):
        for pixel in self.arrayPixels:
            fitVariables = self.fitCustomVariables(pixel[3])
            variables = fitVariables.split('/')
            for variable in variables:
                variable_ = ''
                if variable == 'u': variable_ = 'Page URL'
                elif variable == 'p': variable_ = 'Page Path'
                elif variable == 'r': variable_ = 'Referrer'
                else: variable_ = variable
                varDV = '[%s]'%variable
                varMS = '[REPLACE THIS WITH YOUR MACRO AND PASS IN %s]'%variable
                for code, index in zip(pixel[5:], range(5,len(pixel))):
                    if code != None:
                        code_ = code.replace(varDV, '{{%s}}'%variable_).replace(varMS, '{{%s}}'%variable_) 
                        self.arrayPixels[self.arrayPixels.index(pixel)][index] = code_   
                        
    def fitCustomVariables(self, customVariables):
        typeVariables = sM.subStrings(r':\w+', customVariables)
        try:
            for typeVariable in typeVariables:
                customVariables = customVariables.replace(typeVariable, '')
            return customVariables
        except:
            return customVariables
                    
    def lanchPopUps(self, title_, message_, detail_):
        messagebox.showinfo(
            title   = title_,
            message = message_,
            detail  = detail_
            )

    # Overwrite the setting's method from child class
    def setting(self):
        self.settingWindow()
        
    def advancedSetting(self):
        self.settingWindow(True)
        
    def exitCalcTag(self):
        self.webDOM.tearDown()
        self.pixelBot.tearDown()
        self.root.quit()
        self.root.destroy()
        exit()
              
if __name__ == '__main__':
    pass
    # root = tk.Tk()
    # tk.Toplevel()
    # TagBuilder = tagFrontEnd(root)
    # TagBuilder.mainloop()
