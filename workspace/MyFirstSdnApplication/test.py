#!/usr/bin/python

# enable debugging
import cgitb
cgitb.enable()

print "Content-Type: text/plain\r\n\r\n"
print

# import os
# import sys
#
# if len(sys.argv) > 1:
#   output = sys.argv[1]
# else:
#   output = "no argument found"
#
# print "Hello World!!!"
# print output
#!/usr/bin/python

"""
MiniEdit: a simple network editor for Mininet

This is a simple demonstration of how one might build a
GUI application using Mininet as the network model.

Bob Lantz, April 2010
Gregory Gee, July 2013

Controller icon from http://semlabs.co.uk/
OpenFlow icon from https://www.opennetworking.org/
"""

MINIEDIT_VERSION = '2.2.0.1'




from optparse import OptionParser
from Tkinter import *
from ttk import Notebook
from tkMessageBox import showinfo, showerror, showwarning
from subprocess import call
import tkFont
import csv
import tkFileDialog
import tkSimpleDialog
import re
import json
from distutils.version import StrictVersion
import os
import sys
from functools import partial

if 'PYTHONPATH' in os.environ:
    sys.path = os.environ[ 'PYTHONPATH' ].split( ':' ) + sys.path

# someday: from ttk import *

from mininet.log import info, error, debug, output, setLogLevel
from mininet.net import Mininet, VERSION
from mininet.util import ipStr, netParse, ipAdd, quietRun
from mininet.util import buildTopo
from mininet.util import custom #, customConstructor
from mininet.term import makeTerm, cleanUpScreens
from mininet.node import Controller, RemoteController, NOX, OVSController
from mininet.node import CPULimitedHost, Host, Node #, HostWithPrivateDirs
from mininet.node import OVSKernelSwitch, OVSSwitch, UserSwitch
from mininet.link import TCLink, Intf, Link
from mininet.cli import CLI
from mininet.moduledeps import moduleDeps, pathCheck
from mininet.topo import SingleSwitchTopo, LinearTopo, SingleSwitchReversedTopo
from mininet.topolib import TreeTopo

print 'MiniEdit running against MiniNet '+VERSION
TOPODEF = 'none'
TOPOS = { 'minimal': lambda: SingleSwitchTopo( k=2 ),
          'linear': LinearTopo,
          'reversed': SingleSwitchReversedTopo,
          'single': SingleSwitchTopo,
          'none': None,
          'tree': TreeTopo }
CONTROLLERDEF = 'ref'
CONTROLLERS = { 'ref': Controller,
                'ovsc': OVSController,
                'nox': NOX,
                'remote': RemoteController,
                'none': lambda name: None }
LINKDEF = 'default'
LINKS = { 'default': Link,
          'tc': TCLink }
HOSTDEF = 'proc'
HOSTS = { 'proc': Host,
          'rt': custom( CPULimitedHost, sched='rt' ),
          'cfs': custom( CPULimitedHost, sched='cfs' ) }



class MiniEdit( Frame ):

    "A simple network editor for Mininet."

    def __init__( self, parent=None, cheight=600, cwidth=1000 ):

        self.defaultIpBase='10.0.0.0/8'

        self.nflowDefaults = {'nflowTarget':'',
                              'nflowTimeout':'600',
                              'nflowAddId':'0'}
        self.sflowDefaults = {'sflowTarget':'',
                              'sflowSampling':'400',
                              'sflowHeader':'128',
                              'sflowPolling':'30'}

        self.appPrefs={
            "ipBase": self.defaultIpBase,
            "startCLI": "0",
            "terminalType": 'xterm',
            "switchType": 'ovs',
            "dpctl": '',
            'sflow':self.sflowDefaults,
            'netflow':self.nflowDefaults,
            'openFlowVersions':{'ovsOf10':'1',
                                'ovsOf11':'0',
                                'ovsOf12':'0',
                                'ovsOf13':'0'}

        }


        Frame.__init__( self, parent )
        self.action = None
        self.appName = 'MiniEdit'
        self.fixedFont = tkFont.Font ( family="DejaVu Sans Mono", size="14" )

        # Style
        self.font = ( 'Geneva', 9 )
        self.smallFont = ( 'Geneva', 7 )
        self.bg = 'white'

        # Title
        self.top = self.winfo_toplevel()
        self.top.title( self.appName )

        # Menu bar
        self.createMenubar()

        # Editing canvas
        self.cheight, self.cwidth = cheight, cwidth
        self.cframe, self.canvas = self.createCanvas()

        # Toolbar
        self.controllers = {}

        # Toolbar
        self.images = miniEditImages()
        self.buttons = {}
        self.active = None
        self.tools = ( 'Select', 'Host', 'Switch', 'LegacySwitch', 'LegacyRouter', 'NetLink', 'Controller' )
        self.customColors = { 'Switch': 'darkGreen', 'Host': 'blue' }
        # self.toolbar = self.createToolbar()

        # Layout
        # self.toolbar.grid( column=0, row=0, sticky='nsew')
        self.cframe.grid( column=1, row=0 )
        self.columnconfigure( 1, weight=1 )
        self.rowconfigure( 0, weight=1 )
        self.pack( expand=True, fill='both' )

        # About box
        self.aboutBox = None

        # Initialize node data
        self.nodeBindings = self.createNodeBindings()
        self.nodePrefixes = { 'LegacyRouter': 'r', 'LegacySwitch': 's', 'Switch': 's', 'Host': 'h' , 'Controller': 'c'}
        self.widgetToItem = {}
        self.itemToWidget = {}

        # Initialize link tool
        self.link = self.linkWidget = None

        # Selection support
        self.selection = None

        # Keyboard bindings
        self.bind( '<Control-q>', lambda event: self.quit() )
        self.bind( '<KeyPress-Delete>', self.deleteSelection )
        self.bind( '<KeyPress-BackSpace>', self.deleteSelection )
        self.focus()

        self.hostPopup = Menu(self.top, tearoff=0)
        self.hostPopup.add_command(label='Host Options', font=self.font)
        self.hostPopup.add_separator()
        self.hostPopup.add_command(label='Properties', font=self.font, command=self.hostDetails )

        self.hostRunPopup = Menu(self.top, tearoff=0)
        self.hostRunPopup.add_command(label='Host Options', font=self.font)
        self.hostRunPopup.add_separator()
        self.hostRunPopup.add_command(label='Terminal', font=self.font, command=self.xterm )

        self.legacyRouterRunPopup = Menu(self.top, tearoff=0)
        self.legacyRouterRunPopup.add_command(label='Router Options', font=self.font)
        self.legacyRouterRunPopup.add_separator()
        self.legacyRouterRunPopup.add_command(label='Terminal', font=self.font, command=self.xterm )

        self.switchPopup = Menu(self.top, tearoff=0)
        self.switchPopup.add_command(label='Switch Options', font=self.font)
        self.switchPopup.add_separator()
        self.switchPopup.add_command(label='Properties', font=self.font, command=self.switchDetails )

        self.switchRunPopup = Menu(self.top, tearoff=0)
        self.switchRunPopup.add_command(label='Switch Options', font=self.font)
        self.switchRunPopup.add_separator()
        self.switchRunPopup.add_command(label='List bridge details', font=self.font, command=self.listBridge )

        self.linkPopup = Menu(self.top, tearoff=0)
        self.linkPopup.add_command(label='Link Options', font=self.font)
        self.linkPopup.add_separator()
        self.linkPopup.add_command(label='Properties', font=self.font, command=self.linkDetails )

        self.linkRunPopup = Menu(self.top, tearoff=0)
        self.linkRunPopup.add_command(label='Link Options', font=self.font)
        self.linkRunPopup.add_separator()
        self.linkRunPopup.add_command(label='Link Up', font=self.font, command=self.linkUp )
        self.linkRunPopup.add_command(label='Link Down', font=self.font, command=self.linkDown )

        self.controllerPopup = Menu(self.top, tearoff=0)
        self.controllerPopup.add_command(label='Controller Options', font=self.font)
        self.controllerPopup.add_separator()
        self.controllerPopup.add_command(label='Properties', font=self.font, command=self.controllerDetails )


        # Event handling initalization
        self.linkx = self.linky = self.linkItem = None
        self.lastSelection = None

        # Model initialization
        self.links = {}
        self.hostOpts = {}
        self.switchOpts = {}
        self.hostCount = 0
        self.switchCount = 0
        self.controllerCount = 0
        self.net = None

        # Close window gracefully
        Wm.wm_protocol( self.top, name='WM_DELETE_WINDOW', func=self.quit )

    def quit( self ):
        "Stop our network, if any, then quit."
        self.stop()
        Frame.quit( self )

    def createMenubar( self ):
        "Create our menu bar."

        font = self.font

        mbar = Menu( self.top, font=font )
        self.top.configure( menu=mbar )


        fileMenu = Menu( mbar, tearoff=False )
        mbar.add_cascade( label="File", font=font, menu=fileMenu )
        fileMenu.add_command( label="New", font=font, command=self.newTopology )
        fileMenu.add_command( label="Open", font=font, command=self.loadTopology )
        fileMenu.add_command( label="Save", font=font, command=self.saveTopology )
        fileMenu.add_command( label="Export Level 2 Script", font=font, command=self.exportScript )
        fileMenu.add_separator()
        fileMenu.add_command( label='Quit', command=self.quit, font=font )

        editMenu = Menu( mbar, tearoff=False )
        mbar.add_cascade( label="Edit", font=font, menu=editMenu )
        editMenu.add_command( label="Cut", font=font,
                              command=lambda: self.deleteSelection( None ) )
        editMenu.add_command( label="Preferences", font=font, command=self.prefDetails)

        runMenu = Menu( mbar, tearoff=False )
        mbar.add_cascade( label="Run", font=font, menu=runMenu )
        runMenu.add_command( label="Run", font=font, command=self.doRun )
        runMenu.add_command( label="Stop", font=font, command=self.doStop )
        fileMenu.add_separator()
        runMenu.add_command( label='Show OVS Summary', font=font, command=self.ovsShow )
        runMenu.add_command( label='Root Terminal', font=font, command=self.rootTerminal )

        # Application menu
        appMenu = Menu( mbar, tearoff=False )
        appMenu = Menu( mbar, tearoff=False )
        mbar.add_cascade( label="Help", font=font, menu=appMenu )
        appMenu.add_command( label='About MiniEdit', command=self.about,
                             font=font)
    # Canvas

    def createCanvas( self ):
        "Create and return our scrolling canvas frame."
        f = Frame( self )

        canvas = Canvas( f, width=self.cwidth, height=self.cheight,
                         bg=self.bg )

        # Scroll bars
        xbar = Scrollbar( f, orient='horizontal', command=canvas.xview )
        ybar = Scrollbar( f, orient='vertical', command=canvas.yview )
        canvas.configure( xscrollcommand=xbar.set, yscrollcommand=ybar.set )

        # Resize box
        resize = Label( f, bg='white' )

        # Layout
        canvas.grid( row=0, column=1, sticky='nsew')
        ybar.grid( row=0, column=2, sticky='ns')
        xbar.grid( row=1, column=1, sticky='ew' )
        resize.grid( row=1, column=2, sticky='nsew' )

        # Resize behavior
        f.rowconfigure( 0, weight=1 )
        f.columnconfigure( 1, weight=1 )
        f.grid( row=0, column=0, sticky='nsew' )
        f.bind( '<Configure>', lambda event: self.updateScrollRegion() )

        # Mouse bindings
        canvas.bind( '<ButtonPress-1>', self.clickCanvas )
        canvas.bind( '<B1-Motion>', self.dragCanvas )
        canvas.bind( '<ButtonRelease-1>', self.releaseCanvas )

        return f, canvas

    def updateScrollRegion( self ):
        "Update canvas scroll region to hold everything."
        bbox = self.canvas.bbox( 'all' )
        if bbox is not None:
            self.canvas.configure( scrollregion=( 0, 0, bbox[ 2 ],
                                   bbox[ 3 ] ) )

    def canvasx( self, x_root ):
        "Convert root x coordinate to canvas coordinate."
        c = self.canvas
        return c.canvasx( x_root ) - c.winfo_rootx()

    def canvasy( self, y_root ):
        "Convert root y coordinate to canvas coordinate."
        c = self.canvas
        return c.canvasy( y_root ) - c.winfo_rooty()

    # Toolbar

    def activate( self, toolName ):
        "Activate a tool and press its button."
        # Adjust button appearance
        if self.active:
            self.buttons[ self.active ].configure( relief='raised' )
        self.buttons[ toolName ].configure( relief='sunken' )
        # Activate dynamic bindings
        self.active = toolName


# #    def createToolTip(self, widget, text):
#         toolTip = ToolTip(widget)
#         def enter(event):
#             toolTip.showtip(text)
#         def leave(event):
#             toolTip.hidetip()
#         widget.bind('<Enter>', enter)
#         widget.bind('<Leave>', leave)

# def createToolbar( self ):
#     "Create and return our toolbar frame."
#
#     toolbar = Frame( self )
#
#     # Tools
#     for tool in self.tools:
#         cmd = ( lambda t=tool: self.activate( t ) )
#         b = Button( toolbar, text=tool, font=self.smallFont, command=cmd)
#         if tool in self.images:
#             b.config( height=35, image=self.images[ tool ] )
#             self.createToolTip(b, str(tool))
#             # b.config( compound='top' )
#         b.pack( fill='x' )
#         self.buttons[ tool ] = b
#     self.activate( self.tools[ 0 ] )
#
#     # Spacer
#     Label( toolbar, text='' ).pack()
#
#     # Commands
#     for cmd, color in [ ( 'Stop', 'darkRed' ), ( 'Run', 'darkGreen' ) ]:
#         doCmd = getattr( self, 'do' + cmd )
#         b = Button( toolbar, text=cmd, font=self.smallFont,
#                     fg=color, command=doCmd )
#         b.pack( fill='x', side='bottom' )
#
#     return toolbar

    def doRun( self ):
        "Run command."
        self.activate( 'Select' )
        for tool in self.tools:
            self.buttons[ tool ].config( state='disabled' )
        self.start()

    def doStop( self ):
        "Stop command."
        self.stop()
        for tool in self.tools:
            self.buttons[ tool ].config( state='normal' )

    def addNode( self, node, nodeNum, x, y, name=None):
        "Add a new node to our canvas."
        if 'Switch' == node:
            self.switchCount += 1
        if 'Host' == node:
            self.hostCount += 1
        if 'Controller' == node:
            self.controllerCount += 1
        if name is None:
            name = self.nodePrefixes[ node ] + nodeNum
        self.addNamedNode(node, name, x, y)

    def addNamedNode( self, node, name, x, y):
        "Add a new node to our canvas."
        c = self.canvas
        icon = self.nodeIcon( node, name )
        item = self.canvas.create_window( x, y, anchor='c', window=icon,
                                          tags=node )
        self.widgetToItem[ icon ] = item
        self.itemToWidget[ item ] = icon
        icon.links = {}

    def convertJsonUnicode(self, input):
        "Some part of Mininet don't like Unicode"
        if isinstance(input, dict):
            return {self.convertJsonUnicode(key): self.convertJsonUnicode(value) for key, value in input.iteritems()}
        elif isinstance(input, list):
            return [self.convertJsonUnicode(element) for element in input]
        elif isinstance(input, unicode):
            return input.encode('utf-8')
        else:
            return input

    def loadTopology( self ):
        "Load command."
        c = self.canvas

        myFormats = [
            ('Mininet Topology','*.mn'),
            ('All Files','*'),
        ]
        f = tkFileDialog.askopenfile(filetypes=myFormats, mode='rb')
        if f == None:
            return
        self.newTopology()
        loadedTopology = self.convertJsonUnicode(json.load(f))

        # Load application preferences
        if 'application' in loadedTopology:
            self.appPrefs = dict(self.appPrefs.items() + loadedTopology['application'].items())
            if "ovsOf10" not in self.appPrefs["openFlowVersions"]:
                self.appPrefs["openFlowVersions"]["ovsOf10"] = '0'
            if "ovsOf11" not in self.appPrefs["openFlowVersions"]:
                self.appPrefs["openFlowVersions"]["ovsOf11"] = '0'
            if "ovsOf12" not in self.appPrefs["openFlowVersions"]:
                self.appPrefs["openFlowVersions"]["ovsOf12"] = '0'
            if "ovsOf13" not in self.appPrefs["openFlowVersions"]:
                self.appPrefs["openFlowVersions"]["ovsOf13"] = '0'
            if "sflow" not in self.appPrefs:
                self.appPrefs["sflow"] = self.sflowDefaults
            if "netflow" not in self.appPrefs:
                self.appPrefs["netflow"] = self.nflowDefaults

        # Load controllers
        if ('controllers' in loadedTopology):
            if (loadedTopology['version'] == '1'):
                # This is old location of controller info
                hostname = 'c0'
                self.controllers = {}
                self.controllers[hostname] = loadedTopology['controllers']['c0']
                self.controllers[hostname]['hostname'] = hostname
                self.addNode('Controller', 0, float(30), float(30), name=hostname)
                icon = self.findWidgetByName(hostname)
                icon.bind('<Button-3>', self.do_controllerPopup )
            else:
                controllers = loadedTopology['controllers']
                for controller in controllers:
                    hostname = controller['opts']['hostname']
                    x = controller['x']
                    y = controller['y']
                    self.addNode('Controller', 0, float(x), float(y), name=hostname)
                    self.controllers[hostname] = controller['opts']
                    icon = self.findWidgetByName(hostname)
                    icon.bind('<Button-3>', self.do_controllerPopup )


        # Load hosts
        hosts = loadedTopology['hosts']
        for host in hosts:
            nodeNum = host['number']
            hostname = 'h'+nodeNum
            if 'hostname' in host['opts']:
                hostname = host['opts']['hostname']
            else:
                host['opts']['hostname'] = hostname
            if 'nodeNum' not in host['opts']:
                host['opts']['nodeNum'] = int(nodeNum)
            x = host['x']
            y = host['y']
            self.addNode('Host', nodeNum, float(x), float(y), name=hostname)

            # Fix JSON converting tuple to list when saving
            if 'privateDirectory' in host['opts']:
                newDirList = []
                for privateDir in host['opts']['privateDirectory']:
                    if isinstance( privateDir, list ):
                        newDirList.append((privateDir[0],privateDir[1]))
                    else:
                        newDirList.append(privateDir)
                host['opts']['privateDirectory'] = newDirList
            self.hostOpts[hostname] = host['opts']
            icon = self.findWidgetByName(hostname)
            icon.bind('<Button-3>', self.do_hostPopup )

        # Load switches
        switches = loadedTopology['switches']
        for switch in switches:
            nodeNum = switch['number']
            hostname = 's'+nodeNum
            if 'controllers' not in switch['opts']:
                switch['opts']['controllers'] = []
            if 'switchType' not in switch['opts']:
                switch['opts']['switchType'] = 'default'
            if 'hostname' in switch['opts']:
                hostname = switch['opts']['hostname']
            else:
                switch['opts']['hostname'] = hostname
            if 'nodeNum' not in switch['opts']:
                switch['opts']['nodeNum'] = int(nodeNum)
            x = switch['x']
            y = switch['y']
            if switch['opts']['switchType'] == "legacyRouter":
                self.addNode('LegacyRouter', nodeNum, float(x), float(y), name=hostname)
                icon = self.findWidgetByName(hostname)
                icon.bind('<Button-3>', self.do_legacyRouterPopup )
            elif switch['opts']['switchType'] == "legacySwitch":
                self.addNode('LegacySwitch', nodeNum, float(x), float(y), name=hostname)
                icon = self.findWidgetByName(hostname)
                icon.bind('<Button-3>', self.do_legacySwitchPopup )
            else:
                self.addNode('Switch', nodeNum, float(x), float(y), name=hostname)
                icon = self.findWidgetByName(hostname)
                icon.bind('<Button-3>', self.do_switchPopup )
            self.switchOpts[hostname] = switch['opts']

            # create links to controllers
            if (int(loadedTopology['version']) > 1):
                controllers = self.switchOpts[hostname]['controllers']
                for controller in controllers:
                    dest = self.findWidgetByName(controller)
                    dx, dy = self.canvas.coords( self.widgetToItem[ dest ] )
                    self.link = self.canvas.create_line(float(x),
                                                        float(y),
                                                        dx,
                                                        dy,
                                                        width=4,
                                                        fill='red',
                                                        dash=(6, 4, 2, 4),
                                                        tag='link' )
                    c.itemconfig(self.link, tags=c.gettags(self.link)+('control',))
                    self.addLink( icon, dest, linktype='control' )
                    self.createControlLinkBindings()
                    self.link = self.linkWidget = None
            else:
                dest = self.findWidgetByName('c0')
                dx, dy = self.canvas.coords( self.widgetToItem[ dest ] )
                self.link = self.canvas.create_line(float(x),
                                                    float(y),
                                                    dx,
                                                    dy,
                                                    width=4,
                                                    fill='red',
                                                    dash=(6, 4, 2, 4),
                                                    tag='link' )
                c.itemconfig(self.link, tags=c.gettags(self.link)+('control',))
                self.addLink( icon, dest, linktype='control' )
                self.createControlLinkBindings()
                self.link = self.linkWidget = None

        # Load links
        links = loadedTopology['links']
        for link in links:
            srcNode = link['src']
            src = self.findWidgetByName(srcNode)
            sx, sy = self.canvas.coords( self.widgetToItem[ src ] )

            destNode = link['dest']
            dest = self.findWidgetByName(destNode)
            dx, dy = self.canvas.coords( self.widgetToItem[ dest]  )

            self.link = self.canvas.create_line( sx, sy, dx, dy, width=4,
                                             fill='blue', tag='link' )
            c.itemconfig(self.link, tags=c.gettags(self.link)+('data',))
            self.addLink( src, dest, linkopts=link['opts'] )
            self.createDataLinkBindings()
            self.link = self.linkWidget = None

        f.close

    def findWidgetByName( self, name ):
        for widget in self.widgetToItem:
            if name ==  widget[ 'text' ]:
                return widget

    def newTopology( self ):
        "New command."
        for widget in self.widgetToItem.keys():
            self.deleteItem( self.widgetToItem[ widget ] )
        self.hostCount = 0
        self.switchCount = 0
        self.controllerCount = 0
        self.links = {}
        self.hostOpts = {}
        self.switchOpts = {}
        self.controllers = {}
        self.appPrefs["ipBase"]= self.defaultIpBase

    def saveTopology( self ):
        "Save command."
        myFormats = [
            ('Mininet Topology','*.mn'),
            ('All Files','*'),
        ]

        savingDictionary = {}
        fileName = tkFileDialog.asksaveasfilename(filetypes=myFormats ,title="Save the topology as...")
        if len(fileName ) > 0:
            # Save Application preferences
            savingDictionary['version'] = '2'

            # Save Switches and Hosts
            hostsToSave = []
            switchesToSave = []
            controllersToSave = []
            for widget in self.widgetToItem:
                name = widget[ 'text' ]
                tags = self.canvas.gettags( self.widgetToItem[ widget ] )
                x1, y1 = self.canvas.coords( self.widgetToItem[ widget ] )
                if 'Switch' in tags or 'LegacySwitch' in tags or 'LegacyRouter' in tags:
                    nodeNum = self.switchOpts[name]['nodeNum']
                    nodeToSave = {'number':str(nodeNum),
                                  'x':str(x1),
                                  'y':str(y1),
                                  'opts':self.switchOpts[name] }
                    switchesToSave.append(nodeToSave)
                elif 'Host' in tags:
                    nodeNum = self.hostOpts[name]['nodeNum']
                    nodeToSave = {'number':str(nodeNum),
                                  'x':str(x1),
                                  'y':str(y1),
                                  'opts':self.hostOpts[name] }
                    hostsToSave.append(nodeToSave)
                elif 'Controller' in tags:
                    nodeToSave = {'x':str(x1),
                                  'y':str(y1),
                                  'opts':self.controllers[name] }
                    controllersToSave.append(nodeToSave)
                else:
                    raise Exception( "Cannot create mystery node: " + name )
            savingDictionary['hosts'] = hostsToSave
            savingDictionary['switches'] = switchesToSave
            savingDictionary['controllers'] = controllersToSave

            # Save Links
            linksToSave = []
            for link in self.links.values():
                src = link['src']
                dst = link['dest']
                linkopts = link['linkOpts']

                srcName, dstName = src[ 'text' ], dst[ 'text' ]
                linkToSave = {'src':srcName,
                              'dest':dstName,
                              'opts':linkopts}
                if link['type'] == 'data':
                    linksToSave.append(linkToSave)
            savingDictionary['links'] = linksToSave

            # Save Application preferences
            savingDictionary['application'] = self.appPrefs

            try:
                f = open(fileName, 'wb')
                f.write(json.dumps(savingDictionary, sort_keys=True, indent=4, separators=(',', ': ')))
            except Exception as er:
                print er
            finally:
                f.close()

    def exportScript( self ):
        "Export command."
        myFormats = [
            ('Mininet Custom Topology','*.py'),
            ('All Files','*'),
        ]

        fileName = tkFileDialog.asksaveasfilename(filetypes=myFormats ,title="Export the topology as...")
        if len(fileName ) > 0:
            #print "Now saving under %s" % fileName
            f = open(fileName, 'wb')

            f.write("#!/usr/bin/python\n")
            f.write("\n")
            f.write("from mininet.net import Mininet\n")
            f.write("from mininet.node import Controller, RemoteController, OVSController\n")
            f.write("from mininet.node import CPULimitedHost, Host, Node\n")
            f.write("from mininet.node import OVSKernelSwitch, UserSwitch\n")
            if StrictVersion(MININET_VERSION) > StrictVersion('2.0'):
                f.write("from mininet.node import IVSSwitch\n")
            f.write("from mininet.cli import CLI\n")
            f.write("from mininet.log import setLogLevel, info\n")
            f.write("from mininet.link import TCLink, Intf\n")
            f.write("from subprocess import call\n")

            inBandCtrl = False
            hasLegacySwitch = False
            for widget in self.widgetToItem:
                name = widget[ 'text' ]
                tags = self.canvas.gettags( self.widgetToItem[ widget ] )

                if 'Controller' in tags:
                    opts = self.controllers[name]
                    controllerType = opts['controllerType']
                    if controllerType == 'inband':
                        inBandCtrl = True

            if inBandCtrl == True:
                f.write("\n")
                f.write("class InbandController( RemoteController ):\n")
                f.write("\n")
                f.write("    def checkListening( self ):\n")
                f.write("        \"Overridden to do nothing.\"\n")
                f.write("        return\n")

            f.write("\n")
            f.write("def myNetwork():\n")
            f.write("\n")
            f.write("    net = Mininet( topo=None,\n")
            if len(self.appPrefs['dpctl']) > 0:
                f.write("                   listenPort="+self.appPrefs['dpctl']+",\n")
            f.write("                   build=False,\n")
            f.write("                   ipBase='"+self.appPrefs['ipBase']+"')\n")
            f.write("\n")
            f.write("    info( '*** Adding controller\\n' )\n")
            for widget in self.widgetToItem:
                name = widget[ 'text' ]
                tags = self.canvas.gettags( self.widgetToItem[ widget ] )

                if 'Controller' in tags:
                    opts = self.controllers[name]
                    controllerType = opts['controllerType']
                    if 'controllerProtocol' in opts:
                        controllerProtocol = opts['controllerProtocol']
                    else:
                        controllerProtocol = 'tcp'
                    controllerIP = opts['remoteIP']
                    controllerPort = opts['remotePort']


                    f.write("    "+name+"=net.addController(name='"+name+"',\n")

                    if controllerType == 'remote':
                        f.write("                      controller=RemoteController,\n")
                        f.write("                      ip='"+controllerIP+"',\n")
                    elif controllerType == 'inband':
                        f.write("                      controller=InbandController,\n")
                        f.write("                      ip='"+controllerIP+"',\n")
                    elif controllerType == 'ovsc':
                        f.write("                      controller=OVSController,\n")
                    else:
                        f.write("                      controller=Controller,\n")

                    f.write("                      protocol='"+controllerProtocol+"',\n")
                    f.write("                      port="+str(controllerPort)+")\n")
                    f.write("\n")

            # Save Switches and Hosts
            f.write("    info( '*** Add switches\\n')\n")
            for widget in self.widgetToItem:
                name = widget[ 'text' ]
                tags = self.canvas.gettags( self.widgetToItem[ widget ] )
                if 'LegacyRouter' in tags:
                    f.write("    "+name+" = net.addHost('"+name+"', cls=Node, ip='0.0.0.0')\n")
                    f.write("    "+name+".cmd('sysctl -w net.ipv4.ip_forward=1')\n")
                if 'LegacySwitch' in tags:
                    f.write("    "+name+" = net.addSwitch('"+name+"', cls=OVSKernelSwitch, failMode='standalone')\n")
                if 'Switch' in tags:
                    opts = self.switchOpts[name]
                    nodeNum = opts['nodeNum']
                    f.write("    "+name+" = net.addSwitch('"+name+"'");
                    if opts['switchType'] == 'default':
                        if self.appPrefs['switchType'] == 'ivs':
                            f.write(", cls=IVSSwitch")
                        elif self.appPrefs['switchType'] == 'user':
                            f.write(", cls=UserSwitch")
                        elif self.appPrefs['switchType'] == 'userns':
                            f.write(", cls=UserSwitch, inNamespace=True")
                        else:
                            f.write(", cls=OVSKernelSwitch")
                    elif opts['switchType'] == 'ivs':
                        f.write(", cls=IVSSwitch")
                    elif opts['switchType'] == 'user':
                        f.write(", cls=UserSwitch")
                    elif opts['switchType'] == 'userns':
                        f.write(", cls=UserSwitch, inNamespace=True")
                    else:
                        f.write(", cls=OVSKernelSwitch")
                    if 'dpctl' in opts:
                        f.write(", listenPort="+opts['dpctl'])
                    if 'dpid' in opts:
                        f.write(", dpid='"+opts['dpid']+"'")
                    f.write(")\n")
                    if ('externalInterfaces' in opts):
                        for extInterface in opts['externalInterfaces']:
                            f.write("    Intf( '"+extInterface+"', node="+name+" )\n")

            f.write("\n")
            f.write("    info( '*** Add hosts\\n')\n")
            for widget in self.widgetToItem:
                name = widget[ 'text' ]
                tags = self.canvas.gettags( self.widgetToItem[ widget ] )
                if 'Host' in tags:
                    opts = self.hostOpts[name]
                    ip = None
                    defaultRoute = None
                    if 'defaultRoute' in opts and len(opts['defaultRoute']) > 0:
                        defaultRoute = "'via "+opts['defaultRoute']+"'"
                    else:
                        defaultRoute = 'None'
                    if 'ip' in opts and len(opts['ip']) > 0:
                        ip = opts['ip']
                    else:
                        nodeNum = self.hostOpts[name]['nodeNum']
                        ipBaseNum, prefixLen = netParse( self.appPrefs['ipBase'] )
                        ip = ipAdd(i=nodeNum, prefixLen=prefixLen, ipBaseNum=ipBaseNum)

                    if 'cores' in opts or 'cpu' in opts:
                        f.write("    "+name+" = net.addHost('"+name+"', cls=CPULimitedHost, ip='"+ip+"', defaultRoute="+defaultRoute+")\n")
                        if 'cores' in opts:
                            f.write("    "+name+".setCPUs(cores='"+opts['cores']+"')\n")
                        if 'cpu' in opts:
                            f.write("    "+name+".setCPUFrac(f="+str(opts['cpu'])+", sched='"+opts['sched']+"')\n")
                    else:
                        f.write("    "+name+" = net.addHost('"+name+"', cls=Host, ip='"+ip+"', defaultRoute="+defaultRoute+")\n")
                    if ('externalInterfaces' in opts):
                        for extInterface in opts['externalInterfaces']:
                            f.write("    Intf( '"+extInterface+"', node="+name+" )\n")
            f.write("\n")

            # Save Links
            f.write("    info( '*** Add links\\n')\n")
            for key,linkDetail in self.links.iteritems():
              tags = self.canvas.gettags(key)
              if 'data' in tags:
                optsExist = False
                src = linkDetail['src']
                dst = linkDetail['dest']
                linkopts = linkDetail['linkOpts']
                srcName, dstName = src[ 'text' ], dst[ 'text' ]
                bw = ''
                delay = ''
                loss = ''
                max_queue_size = ''
                linkOpts = "{"
                if 'bw' in linkopts:
                    bw =  linkopts['bw']
                    linkOpts = linkOpts + "'bw':"+str(bw)
                    optsExist = True
                if 'delay' in linkopts:
                    delay =  linkopts['delay']
                    if optsExist:
                        linkOpts = linkOpts + ","
                    linkOpts = linkOpts + "'delay':'"+linkopts['delay']+"'"
                    optsExist = True
                if 'loss' in linkopts:
                    if optsExist:
                        linkOpts = linkOpts + ","
                    linkOpts = linkOpts + "'loss':"+str(linkopts['loss'])
                    optsExist = True
                if 'max_queue_size' in linkopts:
                    if optsExist:
                        linkOpts = linkOpts + ","
                    linkOpts = linkOpts + "'max_queue_size':"+str(linkopts['max_queue_size'])
                    optsExist = True
                if 'jitter' in linkopts:
                    if optsExist:
                        linkOpts = linkOpts + ","
                    linkOpts = linkOpts + "'jitter':'"+linkopts['jitter']+"'"
                    optsExist = True
                if 'speedup' in linkopts:
                    if optsExist:
                        linkOpts = linkOpts + ","
                    linkOpts = linkOpts + "'speedup':"+str(linkopts['speedup'])
                    optsExist = True

                linkOpts = linkOpts + "}"
                if optsExist:
                    f.write("    "+srcName+dstName+" = "+linkOpts+"\n")
                f.write("    net.addLink("+srcName+", "+dstName)
                if optsExist:
                    f.write(", cls=TCLink , **"+srcName+dstName)
                f.write(")\n")

            f.write("\n")
            f.write("    info( '*** Starting network\\n')\n")
            f.write("    net.build()\n")

            f.write("    info( '*** Starting controllers\\n')\n")
            f.write("    for controller in net.controllers:\n")
            f.write("        controller.start()\n")
            f.write("\n")

            f.write("    info( '*** Starting switches\\n')\n")
            for widget in self.widgetToItem:
                name = widget[ 'text' ]
                tags = self.canvas.gettags( self.widgetToItem[ widget ] )
                if 'Switch' in tags or 'LegacySwitch' in tags:
                    opts = self.switchOpts[name]
                    ctrlList = ",".join(opts['controllers'])
                    f.write("    net.get('"+name+"').start(["+ctrlList+"])\n")

            f.write("\n")

            f.write("    info( '*** Post configure switches and hosts\\n')\n")
            for widget in self.widgetToItem:
                name = widget[ 'text' ]
                tags = self.canvas.gettags( self.widgetToItem[ widget ] )
                if 'Switch' in tags:
                    opts = self.switchOpts[name]
                    if opts['switchType'] == 'default':
                        if self.appPrefs['switchType'] == 'user':
                            if ('switchIP' in opts):
                                if (len(opts['switchIP'])>0):
                                    f.write("    "+name+".cmd('ifconfig "+name+" "+opts['switchIP']+"')\n")
                        elif self.appPrefs['switchType'] == 'userns':
                            if ('switchIP' in opts):
                                if (len(opts['switchIP'])>0):
                                    f.write("    "+name+".cmd('ifconfig lo "+opts['switchIP']+"')\n")
                        elif self.appPrefs['switchType'] == 'ovs':
                            if ('switchIP' in opts):
                                if (len(opts['switchIP'])>0):
                                    f.write("    "+name+".cmd('ifconfig "+name+" "+opts['switchIP']+"')\n")
                    elif opts['switchType'] == 'user':
                        if ('switchIP' in opts):
                            if (len(opts['switchIP'])>0):
                                f.write("    "+name+".cmd('ifconfig "+name+" "+opts['switchIP']+"')\n")
                    elif opts['switchType'] == 'userns':
                        if ('switchIP' in opts):
                            if (len(opts['switchIP'])>0):
                                f.write("    "+name+".cmd('ifconfig lo "+opts['switchIP']+"')\n")
                    elif opts['switchType'] == 'ovs':
                        if ('switchIP' in opts):
                            if (len(opts['switchIP'])>0):
                                f.write("    "+name+".cmd('ifconfig "+name+" "+opts['switchIP']+"')\n")
            for widget in self.widgetToItem:
                name = widget[ 'text' ]
                tags = self.canvas.gettags( self.widgetToItem[ widget ] )
                if 'Host' in tags:
                    opts = self.hostOpts[name]
                    # Attach vlan interfaces
                    if ('vlanInterfaces' in opts):
                        for vlanInterface in opts['vlanInterfaces']:
                            f.write("    "+name+".cmd('vconfig add "+name+"-eth0 "+vlanInterface[1]+"')\n")
                            f.write("    "+name+".cmd('ifconfig "+name+"-eth0."+vlanInterface[1]+" "+vlanInterface[0]+"')\n")
                    # Run User Defined Start Command
                    if ('startCommand' in opts):
                        f.write("    "+name+".cmdPrint('"+opts['startCommand']+"')\n")
                if 'Switch' in tags:
                    opts = self.switchOpts[name]
                    # Run User Defined Start Command
                    if ('startCommand' in opts):
                        f.write("    "+name+".cmdPrint('"+opts['startCommand']+"')\n")

            # Configure NetFlow
            nflowValues = self.appPrefs['netflow']
            if len(nflowValues['nflowTarget']) > 0:
                nflowEnabled = False
                nflowSwitches = ''
                for widget in self.widgetToItem:
                    name = widget[ 'text' ]
                    tags = self.canvas.gettags( self.widgetToItem[ widget ] )

                    if 'Switch' in tags:
                        opts = self.switchOpts[name]
                        if 'netflow' in opts:
                            if opts['netflow'] == '1':
                                nflowSwitches = nflowSwitches+' -- set Bridge '+name+' netflow=@MiniEditNF'
                                nflowEnabled=True
                if nflowEnabled:
                    nflowCmd = 'ovs-vsctl -- --id=@MiniEditNF create NetFlow '+ 'target=\\\"'+nflowValues['nflowTarget']+'\\\" '+ 'active-timeout='+nflowValues['nflowTimeout']
                    if nflowValues['nflowAddId'] == '1':
                        nflowCmd = nflowCmd + ' add_id_to_interface=true'
                    else:
                        nflowCmd = nflowCmd + ' add_id_to_interface=false'
                    f.write("    \n")
                    f.write("    call('"+nflowCmd+nflowSwitches+"', shell=True)\n")

            # Configure sFlow
            sflowValues = self.appPrefs['sflow']
            if len(sflowValues['sflowTarget']) > 0:
                sflowEnabled = False
                sflowSwitches = ''
                for widget in self.widgetToItem:
                    name = widget[ 'text' ]
                    tags = self.canvas.gettags( self.widgetToItem[ widget ] )

                    if 'Switch' in tags:
                        opts = self.switchOpts[name]
                        if 'sflow' in opts:
                            if opts['sflow'] == '1':
                                sflowSwitches = sflowSwitches+' -- set Bridge '+name+' sflow=@MiniEditSF'
                                sflowEnabled=True
                if sflowEnabled:
                    sflowCmd = 'ovs-vsctl -- --id=@MiniEditSF create sFlow '+ 'target=\\\"'+sflowValues['sflowTarget']+'\\\" '+ 'header='+sflowValues['sflowHeader']+' '+ 'sampling='+sflowValues['sflowSampling']+' '+ 'polling='+sflowValues['sflowPolling']
                    f.write("    \n")
                    f.write("    call('"+sflowCmd+sflowSwitches+"', shell=True)\n")

            f.write("\n")
            f.write("    CLI(net)\n")
            for widget in self.widgetToItem:
                name = widget[ 'text' ]
                tags = self.canvas.gettags( self.widgetToItem[ widget ] )
                if 'Host' in tags:
                    opts = self.hostOpts[name]
                    # Run User Defined Stop Command
                    if ('stopCommand' in opts):
                        f.write("    "+name+".cmdPrint('"+opts['stopCommand']+"')\n")
                if 'Switch' in tags:
                    opts = self.switchOpts[name]
                    # Run User Defined Stop Command
                    if ('stopCommand' in opts):
                        f.write("    "+name+".cmdPrint('"+opts['stopCommand']+"')\n")

            f.write("    net.stop()\n")
            f.write("\n")
            f.write("if __name__ == '__main__':\n")
            f.write("    setLogLevel( 'info' )\n")
            f.write("    myNetwork()\n")
            f.write("\n")


            f.close()


    # Generic canvas handler
    #
    # We could have used bindtags, as in nodeIcon, but
    # the dynamic approach used here
    # may actually require less code. In any case, it's an
    # interesting introspection-based alternative to bindtags.

    def canvasHandle( self, eventName, event ):
        "Generic canvas event handler"
        if self.active is None:
            return
        toolName = self.active
        handler = getattr( self, eventName + toolName, None )
        if handler is not None:
            handler( event )

    def clickCanvas( self, event ):
        "Canvas click handler."
        self.canvasHandle( 'click', event )

    def dragCanvas( self, event ):
        "Canvas drag handler."
        self.canvasHandle( 'drag', event )

    def releaseCanvas( self, event ):
        "Canvas mouse up handler."
        self.canvasHandle( 'release', event )

    # Currently the only items we can select directly are
    # links. Nodes are handled by bindings in the node icon.

    def findItem( self, x, y ):
        "Find items at a location in our canvas."
        items = self.canvas.find_overlapping( x, y, x, y )
        if len( items ) == 0:
            return None
        else:
            return items[ 0 ]

    # Canvas bindings for Select, Host, Switch and Link tools

    def clickSelect( self, event ):
        "Select an item."
        self.selectItem( self.findItem( event.x, event.y ) )

    def deleteItem( self, item ):
        "Delete an item."
        # Don't delete while network is running
        if self.buttons[ 'Select' ][ 'state' ] == 'disabled':
            return
        # Delete from model
        if item in self.links:
            self.deleteLink( item )
        if item in self.itemToWidget:
            self.deleteNode( item )
        # Delete from view
        self.canvas.delete( item )

    def deleteSelection( self, _event ):
        "Delete the selected item."
        if self.selection is not None:
            self.deleteItem( self.selection )
        self.selectItem( None )

    def nodeIcon( self, node, name ):
        "Create a new node icon."
        icon = Button( self.canvas, image=self.images[ node ],
                       text=name, compound='top' )
        # Unfortunately bindtags wants a tuple
        bindtags = [ str( self.nodeBindings ) ]
        bindtags += list( icon.bindtags() )
        icon.bindtags( tuple( bindtags ) )
        return icon

    def newNode( self, node, event ):
        "Add a new node to our canvas."
        c = self.canvas
        x, y = c.canvasx( event.x ), c.canvasy( event.y )
        name = self.nodePrefixes[ node ]
        if 'Switch' == node:
            self.switchCount += 1
            name = self.nodePrefixes[ node ] + str( self.switchCount )
            self.switchOpts[name] = {}
            self.switchOpts[name]['nodeNum']=self.switchCount
            self.switchOpts[name]['hostname']=name
            self.switchOpts[name]['switchType']='default'
            self.switchOpts[name]['controllers']=[]
        if 'LegacyRouter' == node:
            self.switchCount += 1
            name = self.nodePrefixes[ node ] + str( self.switchCount )
            self.switchOpts[name] = {}
            self.switchOpts[name]['nodeNum']=self.switchCount
            self.switchOpts[name]['hostname']=name
            self.switchOpts[name]['switchType']='legacyRouter'
        if 'LegacySwitch' == node:
            self.switchCount += 1
            name = self.nodePrefixes[ node ] + str( self.switchCount )
            self.switchOpts[name] = {}
            self.switchOpts[name]['nodeNum']=self.switchCount
            self.switchOpts[name]['hostname']=name
            self.switchOpts[name]['switchType']='legacySwitch'
            self.switchOpts[name]['controllers']=[]
        if 'Host' == node:
            self.hostCount += 1
            name = self.nodePrefixes[ node ] + str( self.hostCount )
            self.hostOpts[name] = {'sched':'host'}
            self.hostOpts[name]['nodeNum']=self.hostCount
            self.hostOpts[name]['hostname']=name
        if 'Controller' == node:
            name = self.nodePrefixes[ node ] + str( self.controllerCount )
            ctrlr = { 'controllerType': 'ref',
                      'hostname': name,
                      'controllerProtocol': 'tcp',
                      'remoteIP': '127.0.0.1',
                      'remotePort': 6633}
            self.controllers[name] = ctrlr
            # We want to start controller count at 0
            self.controllerCount += 1

        icon = self.nodeIcon( node, name )
        item = self.canvas.create_window( x, y, anchor='c', window=icon,
                                          tags=node )
        self.widgetToItem[ icon ] = item
        self.itemToWidget[ item ] = icon
        self.selectItem( item )
        icon.links = {}
        if 'Switch' == node:
            icon.bind('<Button-3>', self.do_switchPopup )
        if 'LegacyRouter' == node:
            icon.bind('<Button-3>', self.do_legacyRouterPopup )
        if 'LegacySwitch' == node:
            icon.bind('<Button-3>', self.do_legacySwitchPopup )
        if 'Host' == node:
            icon.bind('<Button-3>', self.do_hostPopup )
        if 'Controller' == node:
            icon.bind('<Button-3>', self.do_controllerPopup )

    def clickController( self, event ):
        "Add a new Controller to our canvas."
        self.newNode( 'Controller', event )

    def clickHost( self, event ):
        "Add a new host to our canvas."
        self.newNode( 'Host', event )

    def clickLegacyRouter( self, event ):
        "Add a new switch to our canvas."
        self.newNode( 'LegacyRouter', event )

    def clickLegacySwitch( self, event ):
        "Add a new switch to our canvas."
        self.newNode( 'LegacySwitch', event )

    def clickSwitch( self, event ):
        "Add a new switch to our canvas."
        self.newNode( 'Switch', event )

    def dragNetLink( self, event ):
        "Drag a link's endpoint to another node."
        if self.link is None:
            return
        # Since drag starts in widget, we use root coords
        x = self.canvasx( event.x_root )
        y = self.canvasy( event.y_root )
        c = self.canvas
        c.coords( self.link, self.linkx, self.linky, x, y )

    def releaseNetLink( self, _event ):
        "Give up on the current link."
        if self.link is not None:
            self.canvas.delete( self.link )
        self.linkWidget = self.linkItem = self.link = None

    # Generic node handlers

    def createNodeBindings( self ):
        "Create a set of bindings for nodes."
        bindings = {
            '<ButtonPress-1>': self.clickNode,
            '<B1-Motion>': self.dragNode,
            '<ButtonRelease-1>': self.releaseNode,
            '<Enter>': self.enterNode,
            '<Leave>': self.leaveNode
        }
        l = Label()  # lightweight-ish owner for bindings
        for event, binding in bindings.items():
            l.bind( event, binding )
        return l

    def selectItem( self, item ):
        "Select an item and remember old selection."
        self.lastSelection = self.selection
        self.selection = item

    def enterNode( self, event ):
        "Select node on entry."
        self.selectNode( event )

    def leaveNode( self, _event ):
        "Restore old selection on exit."
        self.selectItem( self.lastSelection )

    def clickNode( self, event ):
        "Node click handler."
        if self.active is 'NetLink':
            self.startLink( event )
        else:
            self.selectNode( event )
        return 'break'

    def dragNode( self, event ):
        "Node drag handler."
        if self.active is 'NetLink':
            self.dragNetLink( event )
        else:
            self.dragNodeAround( event )

    def releaseNode( self, event ):
        "Node release handler."
        if self.active is 'NetLink':
            self.finishLink( event )

    # Specific node handlers

    def selectNode( self, event ):
        "Select the node that was clicked on."
        item = self.widgetToItem.get( event.widget, None )
        self.selectItem( item )

    def dragNodeAround( self, event ):
        "Drag a node around on the canvas."
        c = self.canvas
        # Convert global to local coordinates;
        # Necessary since x, y are widget-relative
        x = self.canvasx( event.x_root )
        y = self.canvasy( event.y_root )
        w = event.widget
        # Adjust node position
        item = self.widgetToItem[ w ]
        c.coords( item, x, y )
        # Adjust link positions
        for dest in w.links:
            link = w.links[ dest ]
            item = self.widgetToItem[ dest ]
            x1, y1 = c.coords( item )
            c.coords( link, x, y, x1, y1 )
        self.updateScrollRegion()

    def createControlLinkBindings( self ):
        "Create a set of bindings for nodes."
        # Link bindings
        # Selection still needs a bit of work overall
        # Callbacks ignore event

        def select( _event, link=self.link ):
            "Select item on mouse entry."
            self.selectItem( link )

        def highlight( _event, link=self.link ):
            "Highlight item on mouse entry."
            self.selectItem( link )
            self.canvas.itemconfig( link, fill='green' )

        def unhighlight( _event, link=self.link ):
            "Unhighlight item on mouse exit."
            self.canvas.itemconfig( link, fill='red' )
            #self.selectItem( None )

        self.canvas.tag_bind( self.link, '<Enter>', highlight )
        self.canvas.tag_bind( self.link, '<Leave>', unhighlight )
        self.canvas.tag_bind( self.link, '<ButtonPress-1>', select )

    def createDataLinkBindings( self ):
        "Create a set of bindings for nodes."
        # Link bindings
        # Selection still needs a bit of work overall
        # Callbacks ignore event

        def select( _event, link=self.link ):
            "Select item on mouse entry."
            self.selectItem( link )

        def highlight( _event, link=self.link ):
            "Highlight item on mouse entry."
            self.selectItem( link )
            self.canvas.itemconfig( link, fill='green' )

        def unhighlight( _event, link=self.link ):
            "Unhighlight item on mouse exit."
            self.canvas.itemconfig( link, fill='blue' )
            #self.selectItem( None )

        self.canvas.tag_bind( self.link, '<Enter>', highlight )
        self.canvas.tag_bind( self.link, '<Leave>', unhighlight )
        self.canvas.tag_bind( self.link, '<ButtonPress-1>', select )
        self.canvas.tag_bind( self.link, '<Button-3>', self.do_linkPopup )


    def startLink( self, event ):
        "Start a new link."
        if event.widget not in self.widgetToItem:
            # Didn't click on a node
            return

        w = event.widget
        item = self.widgetToItem[ w ]
        x, y = self.canvas.coords( item )
        self.link = self.canvas.create_line( x, y, x, y, width=4,
                                             fill='blue', tag='link' )
        self.linkx, self.linky = x, y
        self.linkWidget = w
        self.linkItem = item


    def finishLink( self, event ):
        "Finish creating a link"
        if self.link is None:
            return
        source = self.linkWidget
        c = self.canvas
        # Since we dragged from the widget, use root coords
        x, y = self.canvasx( event.x_root ), self.canvasy( event.y_root )
        target = self.findItem( x, y )
        dest = self.itemToWidget.get( target, None )
        if ( source is None or dest is None or source == dest
                or dest in source.links or source in dest.links ):
            self.releaseNetLink( event )
            return
        # For now, don't allow hosts to be directly linked
        stags = self.canvas.gettags( self.widgetToItem[ source ] )
        dtags = self.canvas.gettags( target )
        if (('Host' in stags and 'Host' in dtags) or
           ('Controller' in dtags and 'LegacyRouter' in stags) or
           ('Controller' in stags and 'LegacyRouter' in dtags) or
           ('Controller' in dtags and 'LegacySwitch' in stags) or
           ('Controller' in stags and 'LegacySwitch' in dtags) or
           ('Controller' in dtags and 'Host' in stags) or
           ('Controller' in stags and 'Host' in dtags) or
           ('Controller' in stags and 'Controller' in dtags)):
            self.releaseNetLink( event )
            return

        # Set link type
        linkType='data'
        if 'Controller' in stags or 'Controller' in dtags:
            linkType='control'
            c.itemconfig(self.link, dash=(6, 4, 2, 4), fill='red')
            self.createControlLinkBindings()
        else:
            linkType='data'
            self.createDataLinkBindings()
        c.itemconfig(self.link, tags=c.gettags(self.link)+(linkType,))

        x, y = c.coords( target )
        c.coords( self.link, self.linkx, self.linky, x, y )
        self.addLink( source, dest, linktype=linkType )
        if linkType == 'control':
            controllerName = ''
            switchName = ''
            if 'Controller' in stags:
                controllerName = source[ 'text' ]
                switchName = dest[ 'text' ]
            else:
                controllerName = dest[ 'text' ]
                switchName = source[ 'text' ]

            self.switchOpts[switchName]['controllers'].append(controllerName)

        # We're done
        self.link = self.linkWidget = None

    # Menu handlers

    def about( self ):
        "Display about box."
        about = self.aboutBox
        if about is None:
            bg = 'white'
            about = Toplevel( bg='white' )
            about.title( 'About' )
            info = self.appName + ': a simple network editor for MiniNet'
            version = 'MiniEdit '+MINIEDIT_VERSION
            author = 'Originally by: Bob Lantz <rlantz@cs>, April 2010'
            enhancements = 'Enhancements by: Gregory Gee, Since July 2013'
            www = 'http://gregorygee.wordpress.com/category/miniedit/'
            line1 = Label( about, text=info, font='Helvetica 10 bold', bg=bg )
            line2 = Label( about, text=version, font='Helvetica 9', bg=bg )
            line3 = Label( about, text=author, font='Helvetica 9', bg=bg )
            line4 = Label( about, text=enhancements, font='Helvetica 9', bg=bg )
            line5 = Entry( about, font='Helvetica 9', bg=bg, width=len(www), justify=CENTER )
            line5.insert(0, www)
            line5.configure(state='readonly')
            line1.pack( padx=20, pady=10 )
            line2.pack(pady=10 )
            line3.pack(pady=10 )
            line4.pack(pady=10 )
            line5.pack(pady=10 )
            hide = ( lambda about=about: about.withdraw() )
            self.aboutBox = about
            # Hide on close rather than destroying window
            Wm.wm_protocol( about, name='WM_DELETE_WINDOW', func=hide )
        # Show (existing) window
        about.deiconify()

    def createToolImages( self ):
        "Create toolbar (and icon) images."

    def checkIntf( self, intf ):
        "Make sure intf exists and is not configured."
        if ( ' %s:' % intf ) not in quietRun( 'ip link show' ):
            showerror(title="Error",
                      message='External interface ' +intf + ' does not exist! Skipping.')
            return False
        ips = re.findall( r'\d+\.\d+\.\d+\.\d+', quietRun( 'ifconfig ' + intf ) )
        if ips:
            showerror(title="Error",
                      message= intf + ' has an IP address and is probably in use! Skipping.' )
            return False
        return True

    def hostDetails( self, _ignore=None ):
        if ( self.selection is None or
             self.net is not None or
             self.selection not in self.itemToWidget ):
            return
        widget = self.itemToWidget[ self.selection ]
        name = widget[ 'text' ]
        tags = self.canvas.gettags( self.selection )
        if 'Host' not in tags:
            return

        prefDefaults = self.hostOpts[name]
        hostBox = HostDialog(self, title='Host Details', prefDefaults=prefDefaults)
        self.master.wait_window(hostBox.top)
        if hostBox.result:
            newHostOpts = {'nodeNum':self.hostOpts[name]['nodeNum']}
            newHostOpts['sched'] = hostBox.result['sched']
            if len(hostBox.result['startCommand']) > 0:
                newHostOpts['startCommand'] = hostBox.result['startCommand']
            if len(hostBox.result['stopCommand']) > 0:
                newHostOpts['stopCommand'] = hostBox.result['stopCommand']
            if len(hostBox.result['cpu']) > 0:
                newHostOpts['cpu'] = float(hostBox.result['cpu'])
            if len(hostBox.result['cores']) > 0:
                newHostOpts['cores'] = hostBox.result['cores']
            if len(hostBox.result['hostname']) > 0:
                newHostOpts['hostname'] = hostBox.result['hostname']
                name = hostBox.result['hostname']
                widget[ 'text' ] = name
            if len(hostBox.result['defaultRoute']) > 0:
                newHostOpts['defaultRoute'] = hostBox.result['defaultRoute']
            if len(hostBox.result['ip']) > 0:
                newHostOpts['ip'] = hostBox.result['ip']
            if len(hostBox.result['externalInterfaces']) > 0:
                newHostOpts['externalInterfaces'] = hostBox.result['externalInterfaces']
            if len(hostBox.result['vlanInterfaces']) > 0:
                newHostOpts['vlanInterfaces'] = hostBox.result['vlanInterfaces']
            if len(hostBox.result['privateDirectory']) > 0:
                newHostOpts['privateDirectory'] = hostBox.result['privateDirectory']
            self.hostOpts[name] = newHostOpts
            print 'New host details for ' + name + ' = ' + str(newHostOpts)

    def switchDetails( self, _ignore=None ):
        if ( self.selection is None or
             self.net is not None or
             self.selection not in self.itemToWidget ):
            return
        widget = self.itemToWidget[ self.selection ]
        name = widget[ 'text' ]
        tags = self.canvas.gettags( self.selection )
        if 'Switch' not in tags:
            return

        prefDefaults = self.switchOpts[name]
        switchBox = SwitchDialog(self, title='Switch Details', prefDefaults=prefDefaults)
        self.master.wait_window(switchBox.top)
        if switchBox.result:
            newSwitchOpts = {'nodeNum':self.switchOpts[name]['nodeNum']}
            newSwitchOpts['switchType'] = switchBox.result['switchType']
            newSwitchOpts['controllers'] = self.switchOpts[name]['controllers']
            if len(switchBox.result['startCommand']) > 0:
                newSwitchOpts['startCommand'] = switchBox.result['startCommand']
            if len(switchBox.result['stopCommand']) > 0:
                newSwitchOpts['stopCommand'] = switchBox.result['stopCommand']
            if len(switchBox.result['dpctl']) > 0:
                newSwitchOpts['dpctl'] = switchBox.result['dpctl']
            if len(switchBox.result['dpid']) > 0:
                newSwitchOpts['dpid'] = switchBox.result['dpid']
            if len(switchBox.result['hostname']) > 0:
                newSwitchOpts['hostname'] = switchBox.result['hostname']
                name = switchBox.result['hostname']
                widget[ 'text' ] = name
            if len(switchBox.result['externalInterfaces']) > 0:
                newSwitchOpts['externalInterfaces'] = switchBox.result['externalInterfaces']
            newSwitchOpts['switchIP'] = switchBox.result['switchIP']
            newSwitchOpts['sflow'] = switchBox.result['sflow']
            newSwitchOpts['netflow'] = switchBox.result['netflow']
            self.switchOpts[name] = newSwitchOpts
            print 'New switch details for ' + name + ' = ' + str(newSwitchOpts)

    def linkUp( self ):
        if ( self.selection is None or
             self.net is None):
            return
        link = self.selection
        linkDetail =  self.links[link]
        src = linkDetail['src']
        dst = linkDetail['dest']
        srcName, dstName = src[ 'text' ], dst[ 'text' ]
        self.net.configLinkStatus(srcName, dstName, 'up')
        self.canvas.itemconfig(link, dash=())

    def linkDown( self ):
        if ( self.selection is None or
             self.net is None):
            return
        link = self.selection
        linkDetail =  self.links[link]
        src = linkDetail['src']
        dst = linkDetail['dest']
        srcName, dstName = src[ 'text' ], dst[ 'text' ]
        self.net.configLinkStatus(srcName, dstName, 'down')
        self.canvas.itemconfig(link, dash=(4, 4))

    def linkDetails( self, _ignore=None ):
        if ( self.selection is None or
             self.net is not None):
            return
        link = self.selection

        linkDetail =  self.links[link]
        src = linkDetail['src']
        dest = linkDetail['dest']
        linkopts = linkDetail['linkOpts']
        linkBox = LinkDialog(self, title='Link Details', linkDefaults=linkopts)
        if linkBox.result is not None:
            linkDetail['linkOpts'] = linkBox.result
            print 'New link details = ' + str(linkBox.result)

    def prefDetails( self ):
        prefDefaults = self.appPrefs
        prefBox = PrefsDialog(self, title='Preferences', prefDefaults=prefDefaults)
        print 'New Prefs = ' + str(prefBox.result)
        if prefBox.result:
            self.appPrefs = prefBox.result


    def controllerDetails( self ):
        if ( self.selection is None or
             self.net is not None or
             self.selection not in self.itemToWidget ):
            return
        widget = self.itemToWidget[ self.selection ]
        name = widget[ 'text' ]
        tags = self.canvas.gettags( self.selection )
        oldName = name
        if 'Controller' not in tags:
            return

        ctrlrBox = ControllerDialog(self, title='Controller Details', ctrlrDefaults=self.controllers[name])
        if ctrlrBox.result:
            #print 'Controller is ' + ctrlrBox.result[0]
            if len(ctrlrBox.result['hostname']) > 0:
                name = ctrlrBox.result['hostname']
                widget[ 'text' ] = name
            else:
                ctrlrBox.result['hostname'] = name
            self.controllers[name] = ctrlrBox.result
            print 'New controller details for ' + name + ' = ' + str(self.controllers[name])
            # Find references to controller and change name
            if oldName != name:
                for widget in self.widgetToItem:
                    switchName = widget[ 'text' ]
                    tags = self.canvas.gettags( self.widgetToItem[ widget ] )
                    if 'Switch' in tags:
                        switch = self.switchOpts[switchName]
                        if oldName in switch['controllers']:
                            switch['controllers'].remove(oldName)
                            switch['controllers'].append(name)


    def listBridge( self, _ignore=None ):
        if ( self.selection is None or
             self.net is None or
             self.selection not in self.itemToWidget ):
            return
        name = self.itemToWidget[ self.selection ][ 'text' ]
        tags = self.canvas.gettags( self.selection )

        if name not in self.net.nameToNode:
            return
        if 'Switch' in tags or 'LegacySwitch' in tags:
           call(["xterm -T 'Bridge Details' -sb -sl 2000 -e 'ovs-vsctl list bridge " + name + "; read -p \"Press Enter to close\"' &"], shell=True)

    def ovsShow( self, _ignore=None ):
        call(["xterm -T 'OVS Summary' -sb -sl 2000 -e 'ovs-vsctl show; read -p \"Press Enter to close\"' &"], shell=True)

    def rootTerminal( self, _ignore=None ):
        call(["xterm -T 'Root Terminal' -sb -sl 2000 &"], shell=True)

    # Model interface
    #
    # Ultimately we will either want to use a topo or
    # mininet object here, probably.

    def addLink( self, source, dest, linktype='data', linkopts={} ):
        "Add link to model."
        source.links[ dest ] = self.link
        dest.links[ source ] = self.link
        self.links[ self.link ] = {'type' :linktype,
                                   'src':source,
                                   'dest':dest,
                                   'linkOpts':linkopts}

    def deleteLink( self, link ):
        "Delete link from model."
        pair = self.links.get( link, None )
        if pair is not None:
            source=pair['src']
            dest=pair['dest']
            del source.links[ dest ]
            del dest.links[ source ]
            stags = self.canvas.gettags( self.widgetToItem[ source ] )
            dtags = self.canvas.gettags( self.widgetToItem[ dest ] )
            ltags = self.canvas.gettags( link )

            if 'control' in ltags:
                controllerName = ''
                switchName = ''
                if 'Controller' in stags:
                    controllerName = source[ 'text' ]
                    switchName = dest[ 'text' ]
                else:
                    controllerName = dest[ 'text' ]
                    switchName = source[ 'text' ]

                if controllerName in self.switchOpts[switchName]['controllers']:
                    self.switchOpts[switchName]['controllers'].remove(controllerName)


        if link is not None:
            del self.links[ link ]

    def deleteNode( self, item ):
        "Delete node (and its links) from model."

        widget = self.itemToWidget[ item ]
        tags = self.canvas.gettags(item)
        if 'Controller' in tags:
            # remove from switch controller lists
            for serachwidget in self.widgetToItem:
                name = serachwidget[ 'text' ]
                tags = self.canvas.gettags( self.widgetToItem[ serachwidget ] )
                if 'Switch' in tags:
                    if widget['text'] in self.switchOpts[name]['controllers']:
                        self.switchOpts[name]['controllers'].remove(widget['text'])

        for link in widget.links.values():
            # Delete from view and model
            self.deleteItem( link )
        del self.itemToWidget[ item ]
        del self.widgetToItem[ widget ]

    def buildNodes( self, net):
        # Make nodes
        print "Getting Hosts and Switches."
        for widget in self.widgetToItem:
            name = widget[ 'text' ]
            tags = self.canvas.gettags( self.widgetToItem[ widget ] )
            #print name+' has '+str(tags)

            if 'Switch' in tags:
                opts = self.switchOpts[name]
                #print str(opts)

                # Create the correct switch class
                switchClass = customOvs
                switchParms={}
                if 'dpctl' in opts:
                    switchParms['listenPort']=int(opts['dpctl'])
                if 'dpid' in opts:
                    switchParms['dpid']=opts['dpid']
                if opts['switchType'] == 'default':
                    if self.appPrefs['switchType'] == 'ivs':
                        switchClass = IVSSwitch
                    elif self.appPrefs['switchType'] == 'user':
                        switchClass = CustomUserSwitch
                    elif self.appPrefs['switchType'] == 'userns':
                        switchParms['inNamespace'] = True
                        switchClass = CustomUserSwitch
                    else:
                        switchClass = customOvs
                elif opts['switchType'] == 'user':
                    switchClass = CustomUserSwitch
                elif opts['switchType'] == 'userns':
                    switchClass = CustomUserSwitch
                    switchParms['inNamespace'] = True
                elif opts['switchType'] == 'ivs':
                    switchClass = IVSSwitch
                else:
                    switchClass = customOvs

                if switchClass == customOvs:
                    # Set OpenFlow versions
                    self.openFlowVersions = []
                    if self.appPrefs['openFlowVersions']['ovsOf10'] == '1':
                        self.openFlowVersions.append('OpenFlow10')
                    if self.appPrefs['openFlowVersions']['ovsOf11'] == '1':
                        self.openFlowVersions.append('OpenFlow11')
                    if self.appPrefs['openFlowVersions']['ovsOf12'] == '1':
                        self.openFlowVersions.append('OpenFlow12')
                    if self.appPrefs['openFlowVersions']['ovsOf13'] == '1':
                        self.openFlowVersions.append('OpenFlow13')
                    protoList = ",".join(self.openFlowVersions)
                    switchParms['protocols'] = protoList
                newSwitch = net.addSwitch( name , cls=switchClass, **switchParms)

                # Some post startup config
                if switchClass == CustomUserSwitch:
                    if ('switchIP' in opts):
                        if (len(opts['switchIP']) > 0):
                            newSwitch.setSwitchIP(opts['switchIP'])
                if switchClass == customOvs:
                    if ('switchIP' in opts):
                        if (len(opts['switchIP']) > 0):
                            newSwitch.setSwitchIP(opts['switchIP'])

                # Attach external interfaces
                if ('externalInterfaces' in opts):
                    for extInterface in opts['externalInterfaces']:
                        if self.checkIntf(extInterface):
                           Intf( extInterface, node=newSwitch )

            elif 'LegacySwitch' in tags:
                newSwitch = net.addSwitch( name , cls=LegacySwitch)
            elif 'LegacyRouter' in tags:
                newSwitch = net.addHost( name , cls=LegacyRouter)
            elif 'Host' in tags:
                opts = self.hostOpts[name]
                #print str(opts)
                ip = None
                defaultRoute = None
                if 'defaultRoute' in opts and len(opts['defaultRoute']) > 0:
                    defaultRoute = 'via '+opts['defaultRoute']
                if 'ip' in opts and len(opts['ip']) > 0:
                    ip = opts['ip']
                else:
                    nodeNum = self.hostOpts[name]['nodeNum']
                    ipBaseNum, prefixLen = netParse( self.appPrefs['ipBase'] )
                    ip = ipAdd(i=nodeNum, prefixLen=prefixLen, ipBaseNum=ipBaseNum)

                # Create the correct host class
                if 'cores' in opts or 'cpu' in opts:
                    if ('privateDirectory' in opts):
                        hostCls = partial( CPULimitedHostWithPrivateDirs,
                                           privateDirs=opts['privateDirectory'] )
                    else:
                        hostCls=CPULimitedHost
                else:
                    if ('privateDirectory' in opts):
                        hostCls = partial( HostWithPrivateDirs,
                                           privateDirs=opts['privateDirectory'] )
                    else:
                        hostCls=Host
                newHost = net.addHost( name,
                                       cls=hostCls,
                                       ip=ip,
                                       defaultRoute=defaultRoute
                                      )

                # Set the CPULimitedHost specific options
                if 'cores' in opts:
                    newHost.setCPUs(cores = opts['cores'])
                if 'cpu' in opts:
                    newHost.setCPUFrac(f=opts['cpu'], sched=opts['sched'])

                # Attach external interfaces
                if ('externalInterfaces' in opts):
                    for extInterface in opts['externalInterfaces']:
                        if self.checkIntf(extInterface):
                           Intf( extInterface, node=newHost )
                if ('vlanInterfaces' in opts):
                    if len(opts['vlanInterfaces']) > 0:
                        print 'Checking that OS is VLAN prepared'
                        self.pathCheck('vconfig', moduleName='vlan package')
                        moduleDeps( add='8021q' )
            elif 'Controller' in tags:
                opts = self.controllers[name]

                # Get controller info from panel
                controllerType = opts['controllerType']
                if 'controllerProtocol' in opts:
                    controllerProtocol = opts['controllerProtocol']
                else:
                    controllerProtocol = 'tcp'
                    opts['controllerProtocol'] = 'tcp'
                controllerIP = opts['remoteIP']
                controllerPort = opts['remotePort']

                # Make controller
                print 'Getting controller selection:'+controllerType
                if controllerType == 'remote':
                    net.addController(name=name,
                                      controller=RemoteController,
                                      ip=controllerIP,
                                      protocol=controllerProtocol,
                                      port=controllerPort)
                elif controllerType == 'inband':
                    net.addController(name=name,
                                      controller=InbandController,
                                      ip=controllerIP,
                                      protocol=controllerProtocol,
                                      port=controllerPort)
                elif controllerType == 'ovsc':
                    net.addController(name=name,
                                      controller=OVSController,
                                      protocol=controllerProtocol,
                                      port=controllerPort)
                else:
                    net.addController(name=name,
                                      controller=Controller,
                                      protocol=controllerProtocol,
                                      port=controllerPort)

            else:
                raise Exception( "Cannot create mystery node: " + name )

    def pathCheck( self, *args, **kwargs ):
        "Make sure each program in *args can be found in $PATH."
        moduleName = kwargs.get( 'moduleName', 'it' )
        for arg in args:
            if not quietRun( 'which ' + arg ):
                showerror(title="Error",
                      message= 'Cannot find required executable %s.\n' % arg +
                       'Please make sure that %s is installed ' % moduleName +
                       'and available in your $PATH.' )

    def buildLinks( self, net):
        # Make links
        print "Getting Links."
        for key,link in self.links.iteritems():
            tags = self.canvas.gettags(key)
            if 'data' in tags:
                src=link['src']
                dst=link['dest']
                linkopts=link['linkOpts']
                srcName, dstName = src[ 'text' ], dst[ 'text' ]
                srcNode, dstNode = net.nameToNode[ srcName ], net.nameToNode[ dstName ]
                if linkopts:
                    net.addLink(srcNode, dstNode, cls=TCLink, **linkopts)
                else:
                    #print str(srcNode)
                    #print str(dstNode)
                    net.addLink(srcNode, dstNode)
                self.canvas.itemconfig(key, dash=())


    def build( self ):
        print "Build network based on our topology."

        dpctl = None
        if len(self.appPrefs['dpctl']) > 0:
            dpctl = int(self.appPrefs['dpctl'])
        net = Mininet( topo=None,
                       listenPort=dpctl,
                       build=False,
                       ipBase=self.appPrefs['ipBase'] )

        self.buildNodes(net)
        self.buildLinks(net)

        # Build network (we have to do this separately at the moment )
        net.build()

        return net


    def postStartSetup( self ):

        # Setup host details
        for widget in self.widgetToItem:
            name = widget[ 'text' ]
            tags = self.canvas.gettags( self.widgetToItem[ widget ] )
            if 'Host' in tags:
                newHost = self.net.get(name)
                opts = self.hostOpts[name]
                # Attach vlan interfaces
                if ('vlanInterfaces' in opts):
                    for vlanInterface in opts['vlanInterfaces']:
                        print 'adding vlan interface '+vlanInterface[1]
                        newHost.cmdPrint('ifconfig '+name+'-eth0.'+vlanInterface[1]+' '+vlanInterface[0])
                # Run User Defined Start Command
                if ('startCommand' in opts):
                    newHost.cmdPrint(opts['startCommand'])
            if 'Switch' in tags:
                newNode = self.net.get(name)
                opts = self.switchOpts[name]
                # Run User Defined Start Command
                if ('startCommand' in opts):
                    newNode.cmdPrint(opts['startCommand'])


        # Configure NetFlow
        nflowValues = self.appPrefs['netflow']
        if len(nflowValues['nflowTarget']) > 0:
            nflowEnabled = False
            nflowSwitches = ''
            for widget in self.widgetToItem:
                name = widget[ 'text' ]
                tags = self.canvas.gettags( self.widgetToItem[ widget ] )

                if 'Switch' in tags:
                    opts = self.switchOpts[name]
                    if 'netflow' in opts:
                        if opts['netflow'] == '1':
                            print name+' has Netflow enabled'
                            nflowSwitches = nflowSwitches+' -- set Bridge '+name+' netflow=@MiniEditNF'
                            nflowEnabled=True
            if nflowEnabled:
                nflowCmd = 'ovs-vsctl -- --id=@MiniEditNF create NetFlow '+ 'target=\\\"'+nflowValues['nflowTarget']+'\\\" '+ 'active-timeout='+nflowValues['nflowTimeout']
                if nflowValues['nflowAddId'] == '1':
                    nflowCmd = nflowCmd + ' add_id_to_interface=true'
                else:
                    nflowCmd = nflowCmd + ' add_id_to_interface=false'
                print 'cmd = '+nflowCmd+nflowSwitches
                call(nflowCmd+nflowSwitches, shell=True)

            else:
                print 'No switches with Netflow'
        else:
            print 'No NetFlow targets specified.'

        # Configure sFlow
        sflowValues = self.appPrefs['sflow']
        if len(sflowValues['sflowTarget']) > 0:
            sflowEnabled = False
            sflowSwitches = ''
            for widget in self.widgetToItem:
                name = widget[ 'text' ]
                tags = self.canvas.gettags( self.widgetToItem[ widget ] )

                if 'Switch' in tags:
                    opts = self.switchOpts[name]
                    if 'sflow' in opts:
                        if opts['sflow'] == '1':
                            print name+' has sflow enabled'
                            sflowSwitches = sflowSwitches+' -- set Bridge '+name+' sflow=@MiniEditSF'
                            sflowEnabled=True
            if sflowEnabled:
                sflowCmd = 'ovs-vsctl -- --id=@MiniEditSF create sFlow '+ 'target=\\\"'+sflowValues['sflowTarget']+'\\\" '+ 'header='+sflowValues['sflowHeader']+' '+ 'sampling='+sflowValues['sflowSampling']+' '+ 'polling='+sflowValues['sflowPolling']
                print 'cmd = '+sflowCmd+sflowSwitches
                call(sflowCmd+sflowSwitches, shell=True)

            else:
                print 'No switches with sflow'
        else:
            print 'No sFlow targets specified.'

        ## NOTE: MAKE SURE THIS IS LAST THING CALLED
        # Start the CLI if enabled
        if self.appPrefs['startCLI'] == '1':
            info( "\n\n NOTE: PLEASE REMEMBER TO EXIT THE CLI BEFORE YOU PRESS THE STOP BUTTON. Not exiting will prevent MiniEdit from quitting and will prevent you from starting the network again during this sessoin.\n\n")
            CLI(self.net)

    def start( self ):
        "Start network."
        if self.net is None:
            self.net = self.build()

            # Since I am going to inject per switch controllers.
            # I can't call net.start().  I have to replicate what it
            # does and add the controller options.
            #self.net.start()
            info( '**** Starting %s controllers\n' % len( self.net.controllers ) )
            for controller in self.net.controllers:
                info( str(controller) + ' ')
                controller.start()
            info('\n')
            info( '**** Starting %s switches\n' % len( self.net.switches ) )
            #for switch in self.net.switches:
            #    info( switch.name + ' ')
            #    switch.start( self.net.controllers )
            for widget in self.widgetToItem:
                name = widget[ 'text' ]
                tags = self.canvas.gettags( self.widgetToItem[ widget ] )
                if 'Switch' in tags:
                    opts = self.switchOpts[name]
                    switchControllers = []
                    for ctrl in opts['controllers']:
                        switchControllers.append(self.net.get(ctrl))
                    info( name + ' ')
                    # Figure out what controllers will manage this switch
                    self.net.get(name).start( switchControllers )
                if 'LegacySwitch' in tags:
                    self.net.get(name).start( [] )
                    info( name + ' ')
            info('\n')

            self.postStartSetup()

    def stop( self ):
        "Stop network."
        if self.net is not None:
            # Stop host details
            for widget in self.widgetToItem:
                name = widget[ 'text' ]
                tags = self.canvas.gettags( self.widgetToItem[ widget ] )
                if 'Host' in tags:
                    newHost = self.net.get(name)
                    opts = self.hostOpts[name]
                    # Run User Defined Stop Command
                    if ('stopCommand' in opts):
                        newHost.cmdPrint(opts['stopCommand'])
                if 'Switch' in tags:
                    newNode = self.net.get(name)
                    opts = self.switchOpts[name]
                    # Run User Defined Stop Command
                    if ('stopCommand' in opts):
                        newNode.cmdPrint(opts['stopCommand'])

            self.net.stop()
        cleanUpScreens()
        self.net = None

    def do_linkPopup(self, event):
        # display the popup menu
        if ( self.net is None ):
            try:
                self.linkPopup.tk_popup(event.x_root, event.y_root, 0)
            finally:
                # make sure to release the grab (Tk 8.0a1 only)
                self.linkPopup.grab_release()
        else:
            try:
                self.linkRunPopup.tk_popup(event.x_root, event.y_root, 0)
            finally:
                # make sure to release the grab (Tk 8.0a1 only)
                self.linkRunPopup.grab_release()

    def do_controllerPopup(self, event):
        # display the popup menu
        if ( self.net is None ):
            try:
                self.controllerPopup.tk_popup(event.x_root, event.y_root, 0)
            finally:
                # make sure to release the grab (Tk 8.0a1 only)
                self.controllerPopup.grab_release()

    def do_legacyRouterPopup(self, event):
        # display the popup menu
        if ( self.net is not None ):
            try:
                self.legacyRouterRunPopup.tk_popup(event.x_root, event.y_root, 0)
            finally:
                # make sure to release the grab (Tk 8.0a1 only)
                self.legacyRouterRunPopup.grab_release()

    def do_hostPopup(self, event):
        # display the popup menu
        if ( self.net is None ):
            try:
                self.hostPopup.tk_popup(event.x_root, event.y_root, 0)
            finally:
                # make sure to release the grab (Tk 8.0a1 only)
                self.hostPopup.grab_release()
        else:
            try:
                self.hostRunPopup.tk_popup(event.x_root, event.y_root, 0)
            finally:
                # make sure to release the grab (Tk 8.0a1 only)
                self.hostRunPopup.grab_release()

    def do_legacySwitchPopup(self, event):
        # display the popup menu
        if ( self.net is not None ):
            try:
                self.switchRunPopup.tk_popup(event.x_root, event.y_root, 0)
            finally:
                # make sure to release the grab (Tk 8.0a1 only)
                self.switchRunPopup.grab_release()

    def do_switchPopup(self, event):
        # display the popup menu
        if ( self.net is None ):
            try:
                self.switchPopup.tk_popup(event.x_root, event.y_root, 0)
            finally:
                # make sure to release the grab (Tk 8.0a1 only)
                self.switchPopup.grab_release()
        else:
            try:
                self.switchRunPopup.tk_popup(event.x_root, event.y_root, 0)
            finally:
                # make sure to release the grab (Tk 8.0a1 only)
                self.switchRunPopup.grab_release()

    def xterm( self, _ignore=None ):
        "Make an xterm when a button is pressed."
        if ( self.selection is None or
             self.net is None or
             self.selection not in self.itemToWidget ):
            return
        name = self.itemToWidget[ self.selection ][ 'text' ]
        if name not in self.net.nameToNode:
            return
        term = makeTerm( self.net.nameToNode[ name ], 'Host', term=self.appPrefs['terminalType'] )
        if StrictVersion(MININET_VERSION) > StrictVersion('2.0'):
            self.net.terms += term
        else:
            self.net.terms.append(term)

    def iperf( self, _ignore=None ):
        "Make an xterm when a button is pressed."
        if ( self.selection is None or
             self.net is None or
             self.selection not in self.itemToWidget ):
            return
        name = self.itemToWidget[ self.selection ][ 'text' ]
        if name not in self.net.nameToNode:
            return
        self.net.nameToNode[ name ].cmd( 'iperf -s -p 5001 &' )

    """ BELOW HERE IS THE TOPOLOGY IMPORT CODE """

    def parseArgs( self ):
        """Parse command-line args and return options object.
           returns: opts parse options dict"""

        if '--custom' in sys.argv:
            index = sys.argv.index( '--custom' )
            if len( sys.argv ) > index + 1:
                filename = sys.argv[ index + 1 ]
                self.parseCustomFile( filename )
            else:
                raise Exception( 'Custom file name not found' )

        desc = ( "The %prog utility creates Mininet network from the\n"
                 "command line. It can create parametrized topologies,\n"
                 "invoke the Mininet CLI, and run tests." )

        usage = ( '%prog [options]\n'
                  '(type %prog -h for details)' )

        opts = OptionParser( description=desc, usage=usage )

        addDictOption( opts, TOPOS, TOPODEF, 'topo' )
        addDictOption( opts, LINKS, LINKDEF, 'link' )

        opts.add_option( '--custom', type='string', default=None,
                         help='read custom topo and node params from .py' +
                         'file' )

        self.options, self.args = opts.parse_args()
        # We don't accept extra arguments after the options
        if self.args:
            opts.print_help()
            exit()

    def setCustom( self, name, value ):
        "Set custom parameters for MininetRunner."
        if name in ( 'topos', 'switches', 'hosts', 'controllers' ):
            # Update dictionaries
            param = name.upper()
            globals()[ param ].update( value )
        elif name == 'validate':
            # Add custom validate function
            self.validate = value
        else:
            # Add or modify global variable or class
            globals()[ name ] = value

    def parseCustomFile( self, fileName ):
        "Parse custom file and add params before parsing cmd-line options."
        customs = {}
        if os.path.isfile( fileName ):
            execfile( fileName, customs, customs )
            for name, val in customs.iteritems():
                self.setCustom( name, val )
        else:
            raise Exception( 'could not find custom file: %s' % fileName )

    def importTopo( self ):
        print 'topo='+self.options.topo
        if self.options.topo == 'none':
            return
        self.newTopology()
        topo = buildTopo( TOPOS, self.options.topo )
        link = customConstructor( LINKS, self.options.link )
        importNet = Mininet(topo=topo, build=False, link=link)
        importNet.build()

        c = self.canvas
        rowIncrement = 100
        currentY = 100

        # Add Controllers
        print 'controllers:'+str(len(importNet.controllers))
        for controller in importNet.controllers:
            name = controller.name
            x = self.controllerCount*100+100
            self.addNode('Controller', self.controllerCount,
                 float(x), float(currentY), name=name)
            icon = self.findWidgetByName(name)
            icon.bind('<Button-3>', self.do_controllerPopup )
            ctrlr = { 'controllerType': 'ref',
                      'hostname': name,
                      'controllerProtocol': controller.protocol,
                      'remoteIP': controller.ip,
                      'remotePort': controller.port}
            self.controllers[name] = ctrlr



        currentY = currentY + rowIncrement

        # Add switches
        print 'switches:'+str(len(importNet.switches))
        columnCount = 0
        for switch in importNet.switches:
            name = switch.name
            self.switchOpts[name] = {}
            self.switchOpts[name]['nodeNum']=self.switchCount
            self.switchOpts[name]['hostname']=name
            self.switchOpts[name]['switchType']='default'
            self.switchOpts[name]['controllers']=[]

            x = columnCount*100+100
            self.addNode('Switch', self.switchCount,
                 float(x), float(currentY), name=name)
            icon = self.findWidgetByName(name)
            icon.bind('<Button-3>', self.do_switchPopup )
            # Now link to controllers
            for controller in importNet.controllers:
                self.switchOpts[name]['controllers'].append(controller.name)
                dest = self.findWidgetByName(controller.name)
                dx, dy = c.coords( self.widgetToItem[ dest ] )
                self.link = c.create_line(float(x),
                                          float(currentY),
                                          dx,
                                          dy,
                                          width=4,
                                          fill='red',
                                          dash=(6, 4, 2, 4),
                                          tag='link' )
                c.itemconfig(self.link, tags=c.gettags(self.link)+('control',))
                self.addLink( icon, dest, linktype='control' )
                self.createControlLinkBindings()
                self.link = self.linkWidget = None
            if columnCount == 9:
                columnCount = 0
                currentY = currentY + rowIncrement
            else:
                columnCount =columnCount+1


        currentY = currentY + rowIncrement
        # Add hosts
        print 'hosts:'+str(len(importNet.hosts))
        columnCount = 0
        for host in importNet.hosts:
            name = host.name
            self.hostOpts[name] = {'sched':'host'}
            self.hostOpts[name]['nodeNum']=self.hostCount
            self.hostOpts[name]['hostname']=name
            self.hostOpts[name]['ip']=host.IP()

            x = columnCount*100+100
            self.addNode('Host', self.hostCount,
                 float(x), float(currentY), name=name)
            icon = self.findWidgetByName(name)
            icon.bind('<Button-3>', self.do_hostPopup )
            if columnCount == 9:
                columnCount = 0
                currentY = currentY + rowIncrement
            else:
                columnCount =columnCount+1

        print 'links:'+str(len(topo.links()))
        #[('h1', 's3'), ('h2', 's4'), ('s3', 's4')]
        for link in topo.links():
            print str(link)
            srcNode = link[0]
            src = self.findWidgetByName(srcNode)
            sx, sy = self.canvas.coords( self.widgetToItem[ src ] )

            destNode = link[1]
            dest = self.findWidgetByName(destNode)
            dx, dy = self.canvas.coords( self.widgetToItem[ dest]  )

            params = topo.linkInfo( srcNode, destNode )
            print 'Link Parameters='+str(params)

            self.link = self.canvas.create_line( sx, sy, dx, dy, width=4,
                                             fill='blue', tag='link' )
            c.itemconfig(self.link, tags=c.gettags(self.link)+('data',))
            self.addLink( src, dest, linkopts=params )
            self.createDataLinkBindings()
            self.link = self.linkWidget = None

        importNet.stop()

def miniEditImages():
    "Create and return images for MiniEdit."

    # Image data. Git will be unhappy. However, the alternative
    # is to keep track of separate binary files, which is also
    # unappealing.

    return {
        'Select': BitmapImage(
            file='/usr/include/X11/bitmaps/left_ptr' ),

        'Switch': PhotoImage( data=r"""
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
            """),

        'LegacySwitch': PhotoImage( data=r"""
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
4BE2eIRYeHAEIBwBP0Y4Qn41YWRSCQgAOw==
            """),

        'LegacyRouter': PhotoImage( data=r"""
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
gGPLHwLwcMIo12Qxu0ABAQA7
            """),

        'Controller': PhotoImage( data=r"""
            R0lGODlhMAAwAPcAAAEBAWfNAYWFhcfHx+3t6/f390lJUaWlpfPz8/Hx72lpaZGRke/v77m5uc0B
            AeHh4e/v7WNjY3t7e5eXlyMjI4mJidPT0+3t7f///09PT7Ozs/X19fHx8ZWTk8HBwX9/fwAAAAAA
            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
            AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAACH5BAEAAAAALAAAAAAwADAA
            Bwj/AAEIHEiwoMGDCBMqXMiwocOHECNKnEixosWLGAEIeMCxo8ePHwVkBGABg8mTKFOmtDByAIYN
            MGPCRCCzQIENNzEMGOkBAwIKQIMKpYCgKAIHCDB4GNkAA4OnUJ9++CDhQ1QGFzA0GKkBA4GvYMOK
            BYtBA1cNaNOqXcuWq8q3b81m7Cqzbk2bMMu6/Tl0qFEEAZLKxdj1KlSqVA3rnet1rOOwiwmznUzZ
            LdzLJgdfpIv3pmebN2Pm1GyRbocNp1PLNMDaAM3Im1/alQk4gO28pCt2RdCBt+/eRg8IP1AUdmmf
            f5MrL56bYlcOvaP7Xo6Ag3HdGDho3869u/YE1507t+3AgLz58ujPMwg/sTBUCAzgy49PH0LW5u0x
            XFiwvz////5dcJ9bjxVIAHsSdUXAAgs2yOCDDn6FYEQaFGDgYxNCpEFfHHKIX4IDhCjiiCSS+CGF
            FlCmogYpcnVABTDGKGOMAlRQYwUHnKjhAjX2aOOPN8LImgAL6PiQBhLMqCSNAThQgQRGOqRBBD1W
            aaOVAggnQARRNqRBBxmEKeaYZIrZQZcMKbDiigqM5OabcMYp55x01ilnQAA7
            """),

        'Host': PhotoImage( data=r"""
            R0lGODlhIAAYAPcAMf//////zP//mf//Zv//M///AP/M///MzP/M
            mf/MZv/MM//MAP+Z//+ZzP+Zmf+ZZv+ZM/+ZAP9m//9mzP9mmf9m
            Zv9mM/9mAP8z//8zzP8zmf8zZv8zM/8zAP8A//8AzP8Amf8AZv8A
            M/8AAMz//8z/zMz/mcz/Zsz/M8z/AMzM/8zMzMzMmczMZszMM8zM
            AMyZ/8yZzMyZmcyZZsyZM8yZAMxm/8xmzMxmmcxmZsxmM8xmAMwz
            /8wzzMwzmcwzZswzM8wzAMwA/8wAzMwAmcwAZswAM8wAAJn//5n/
            zJn/mZn/Zpn/M5n/AJnM/5nMzJnMmZnMZpnMM5nMAJmZ/5mZzJmZ
            mZmZZpmZM5mZAJlm/5lmzJlmmZlmZplmM5lmAJkz/5kzzJkzmZkz
            ZpkzM5kzAJkA/5kAzJkAmZkAZpkAM5kAAGb//2b/zGb/mWb/Zmb/
            M2b/AGbM/2bMzGbMmWbMZmbMM2bMAGaZ/2aZzGaZmWaZZmaZM2aZ
            AGZm/2ZmzGZmmWZmZmZmM2ZmAGYz/2YzzGYzmWYzZmYzM2YzAGYA
            /2YAzGYAmWYAZmYAM2YAADP//zP/zDP/mTP/ZjP/MzP/ADPM/zPM
            zDPMmTPMZjPMMzPMADOZ/zOZzDOZmTOZZjOZMzOZADNm/zNmzDNm
            mTNmZjNmMzNmADMz/zMzzDMzmTMzZjMzMzMzADMA/zMAzDMAmTMA
            ZjMAMzMAAAD//wD/zAD/mQD/ZgD/MwD/AADM/wDMzADMmQDMZgDM
            MwDMAACZ/wCZzACZmQCZZgCZMwCZAABm/wBmzABmmQBmZgBmMwBm
            AAAz/wAzzAAzmQAzZgAzMwAzAAAA/wAAzAAAmQAAZgAAM+4AAN0A
            ALsAAKoAAIgAAHcAAFUAAEQAACIAABEAAADuAADdAAC7AACqAACI
            AAB3AABVAABEAAAiAAARAAAA7gAA3QAAuwAAqgAAiAAAdwAAVQAA
            RAAAIgAAEe7u7t3d3bu7u6qqqoiIiHd3d1VVVURERCIiIhEREQAA
            ACH5BAEAAAAALAAAAAAgABgAAAiNAAH8G0iwoMGDCAcKTMiw4UBw
            BPXVm0ixosWLFvVBHFjPoUeC9Tb+6/jRY0iQ/8iVbHiS40CVKxG2
            HEkQZsyCM0mmvGkw50uePUV2tEnOZkyfQA8iTYpTKNOgKJ+C3AhO
            p9SWVaVOfWj1KdauTL9q5UgVbFKsEjGqXVtP40NwcBnCjXtw7tx/
            C8cSBBAQADs=
        """ ),

        'OldSwitch': PhotoImage( data=r"""
            R0lGODlhIAAYAPcAMf//////zP//mf//Zv//M///AP/M///MzP/M
            mf/MZv/MM//MAP+Z//+ZzP+Zmf+ZZv+ZM/+ZAP9m//9mzP9mmf9m
            Zv9mM/9mAP8z//8zzP8zmf8zZv8zM/8zAP8A//8AzP8Amf8AZv8A
            M/8AAMz//8z/zMz/mcz/Zsz/M8z/AMzM/8zMzMzMmczMZszMM8zM
            AMyZ/8yZzMyZmcyZZsyZM8yZAMxm/8xmzMxmmcxmZsxmM8xmAMwz
            /8wzzMwzmcwzZswzM8wzAMwA/8wAzMwAmcwAZswAM8wAAJn//5n/
            zJn/mZn/Zpn/M5n/AJnM/5nMzJnMmZnMZpnMM5nMAJmZ/5mZzJmZ
            mZmZZpmZM5mZAJlm/5lmzJlmmZlmZplmM5lmAJkz/5kzzJkzmZkz
            ZpkzM5kzAJkA/5kAzJkAmZkAZpkAM5kAAGb//2b/zGb/mWb/Zmb/
            M2b/AGbM/2bMzGbMmWbMZmbMM2bMAGaZ/2aZzGaZmWaZZmaZM2aZ
            AGZm/2ZmzGZmmWZmZmZmM2ZmAGYz/2YzzGYzmWYzZmYzM2YzAGYA
            /2YAzGYAmWYAZmYAM2YAADP//zP/zDP/mTP/ZjP/MzP/ADPM/zPM
            zDPMmTPMZjPMMzPMADOZ/zOZzDOZmTOZZjOZMzOZADNm/zNmzDNm
            mTNmZjNmMzNmADMz/zMzzDMzmTMzZjMzMzMzADMA/zMAzDMAmTMA
            ZjMAMzMAAAD//wD/zAD/mQD/ZgD/MwD/AADM/wDMzADMmQDMZgDM
            MwDMAACZ/wCZzACZmQCZZgCZMwCZAABm/wBmzABmmQBmZgBmMwBm
            AAAz/wAzzAAzmQAzZgAzMwAzAAAA/wAAzAAAmQAAZgAAM+4AAN0A
            ALsAAKoAAIgAAHcAAFUAAEQAACIAABEAAADuAADdAAC7AACqAACI
            AAB3AABVAABEAAAiAAARAAAA7gAA3QAAuwAAqgAAiAAAdwAAVQAA
            RAAAIgAAEe7u7t3d3bu7u6qqqoiIiHd3d1VVVURERCIiIhEREQAA
            ACH5BAEAAAAALAAAAAAgABgAAAhwAAEIHEiwoMGDCBMqXMiwocOH
            ECNKnEixosWB3zJq3Mixo0eNAL7xG0mypMmTKPl9Cznyn8uWL/m5
            /AeTpsyYI1eKlBnO5r+eLYHy9Ck0J8ubPmPOrMmUpM6UUKMa/Ui1
            6saLWLNq3cq1q9evYB0GBAA7
        """ ),

        'NetLink': PhotoImage( data=r"""
            R0lGODlhFgAWAPcAMf//////zP//mf//Zv//M///AP/M///MzP/M
            mf/MZv/MM//MAP+Z//+ZzP+Zmf+ZZv+ZM/+ZAP9m//9mzP9mmf9m
            Zv9mM/9mAP8z//8zzP8zmf8zZv8zM/8zAP8A//8AzP8Amf8AZv8A
            M/8AAMz//8z/zMz/mcz/Zsz/M8z/AMzM/8zMzMzMmczMZszMM8zM
            AMyZ/8yZzMyZmcyZZsyZM8yZAMxm/8xmzMxmmcxmZsxmM8xmAMwz
            /8wzzMwzmcwzZswzM8wzAMwA/8wAzMwAmcwAZswAM8wAAJn//5n/
            zJn/mZn/Zpn/M5n/AJnM/5nMzJnMmZnMZpnMM5nMAJmZ/5mZzJmZ
            mZmZZpmZM5mZAJlm/5lmzJlmmZlmZplmM5lmAJkz/5kzzJkzmZkz
            ZpkzM5kzAJkA/5kAzJkAmZkAZpkAM5kAAGb//2b/zGb/mWb/Zmb/
            M2b/AGbM/2bMzGbMmWbMZmbMM2bMAGaZ/2aZzGaZmWaZZmaZM2aZ
            AGZm/2ZmzGZmmWZmZmZmM2ZmAGYz/2YzzGYzmWYzZmYzM2YzAGYA
            /2YAzGYAmWYAZmYAM2YAADP//zP/zDP/mTP/ZjP/MzP/ADPM/zPM
            zDPMmTPMZjPMMzPMADOZ/zOZzDOZmTOZZjOZMzOZADNm/zNmzDNm
            mTNmZjNmMzNmADMz/zMzzDMzmTMzZjMzMzMzADMA/zMAzDMAmTMA
            ZjMAMzMAAAD//wD/zAD/mQD/ZgD/MwD/AADM/wDMzADMmQDMZgDM
            MwDMAACZ/wCZzACZmQCZZgCZMwCZAABm/wBmzABmmQBmZgBmMwBm
            AAAz/wAzzAAzmQAzZgAzMwAzAAAA/wAAzAAAmQAAZgAAM+4AAN0A
            ALsAAKoAAIgAAHcAAFUAAEQAACIAABEAAADuAADdAAC7AACqAACI
            AAB3AABVAABEAAAiAAARAAAA7gAA3QAAuwAAqgAAiAAAdwAAVQAA
            RAAAIgAAEe7u7t3d3bu7u6qqqoiIiHd3d1VVVURERCIiIhEREQAA
            ACH5BAEAAAAALAAAAAAWABYAAAhIAAEIHEiwoEGBrhIeXEgwoUKG
            Cx0+hGhQoiuKBy1irChxY0GNHgeCDAlgZEiTHlFuVImRJUWXEGEy
            lBmxI8mSNknm1Dnx5sCAADs=
        """ )
    }

def addDictOption( opts, choicesDict, default, name, helpStr=None ):
    """Convenience function to add choices dicts to OptionParser.
       opts: OptionParser instance
       choicesDict: dictionary of valid choices, must include default
       default: default choice key
       name: long option name
       help: string"""
    if default not in choicesDict:
        raise Exception( 'Invalid  default %s for choices dict: %s' %
                         ( default, name ) )
    if not helpStr:
        helpStr = ( '|'.join( sorted( choicesDict.keys() ) ) +
                    '[,param=value...]' )
    opts.add_option( '--' + name,
                     type='string',
                     default = default,
                     help = helpStr )


if __name__ == '__main__':
    setLogLevel( 'info' )
    app = MiniEdit()
    ### import topology if specified ###
    app.parseArgs()
    app.importTopo()

app.mainloop()
