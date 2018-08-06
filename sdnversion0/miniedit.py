#!/usr/bin/python

# enable debugging
import cgitb
cgitb.enable()

from optparse import OptionParser
# from Tkinter import *
from Tkinter import ( Frame, Label, LabelFrame, Entry, OptionMenu, Checkbutton,
                      Menu, Toplevel, Button, BitmapImage, PhotoImage, Canvas,
                      Scrollbar, Wm, TclError, StringVar, IntVar,
                      E, W, EW, NW, Y, VERTICAL, SOLID, CENTER,
                      RIGHT, LEFT, BOTH, TRUE, FALSE )
from ttk import Notebook
from tkMessageBox import showerror
from subprocess import call
import tkFont
import tkFileDialog
import tkSimpleDialog
import re
import json
from distutils.version import StrictVersion
import os
import sys
from functools import partial


#print "Content-Type: text/plain\r\n\r\n"
#print

#print "Hello World!"

MINIEDIT_VERSION = '2.2.0.1'
if 'PYTHONPATH' in os.environ:
    sys.path = os.environ[ 'PYTHONPATH' ].split( ':' ) + sys.path

# someday: from ttk import *

from mininet.log import info, debug, warn, setLogLevel
from mininet.net import Mininet, VERSION
from mininet.util import netParse, ipAdd, quietRun
from mininet.util import buildTopo
from mininet.util import custom, customClass
from mininet.term import makeTerm, cleanUpScreens
from mininet.node import Controller, RemoteController, NOX, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSSwitch, UserSwitch
from mininet.link import TCLink, Intf, Link
from mininet.cli import CLI
from mininet.moduledeps import moduleDeps
from mininet.topo import SingleSwitchTopo, LinearTopo, SingleSwitchReversedTopo
from mininet.topolib import TreeTopo

#info( 'MiniEdit running against Mininet '+VERSION, '\n' )
print 'MiniEdit running against Mininet '+VERSION
MININET_VERSION = re.sub(r'[^\d\.]', '', VERSION)
if StrictVersion(MININET_VERSION) > StrictVersion('2.0'):
    from mininet.node import IVSSwitch


class InbandController( RemoteController ):
    "RemoteController that ignores checkListening"
    def checkListening( self ):
        "Overridden to do nothing."
        return

class CustomUserSwitch(UserSwitch):
    "Customized UserSwitch"
    def __init__( self, name, dpopts='--no-slicing', **kwargs ):
        UserSwitch.__init__( self, name, **kwargs )
        self.switchIP = None

    def getSwitchIP(self):
        "Return management IP address"
        return self.switchIP

    def setSwitchIP(self, ip):
        "Set management IP address"
        self.switchIP = ip

    def start( self, controllers ):
        "Start and set management IP address"
        # Call superclass constructor
        UserSwitch.start( self, controllers )
        # Set Switch IP address
        if self.switchIP is not None:
            if not self.inNamespace:
                self.cmd( 'ifconfig', self, self.switchIP )
            else:
                self.cmd( 'ifconfig lo', self.switchIP )

class LegacyRouter( Node ):
    "Simple IP router"
    def __init__( self, name, inNamespace=True, **params ):
        Node.__init__( self, name, inNamespace, **params )

    def config( self, **_params ):
        if self.intfs:
            self.setParam( _params, 'setIP', ip='0.0.0.0' )
        r = Node.config( self, **_params )
        self.cmd('sysctl -w net.ipv4.ip_forward=1')
        return r

class LegacySwitch(OVSSwitch):
    "OVS switch in standalone/bridge mode"
    def __init__( self, name, **params ):
        OVSSwitch.__init__( self, name, failMode='standalone', **params )
        self.switchIP = None

class customOvs(OVSSwitch):
    "Customized OVS switch"

    def __init__( self, name, failMode='secure', datapath='kernel', **params ):
        OVSSwitch.__init__( self, name, failMode=failMode, datapath=datapath,**params )
        self.switchIP = None

    def getSwitchIP(self):
        "Return management IP address"
        return self.switchIP

    def setSwitchIP(self, ip):
        "Set management IP address"
        self.switchIP = ip

    def start( self, controllers ):
        "Start and set management IP address"
        # Call superclass constructor
        OVSSwitch.start( self, controllers )
        # Set Switch IP address
        if self.switchIP is not None:
            self.cmd( 'ifconfig', self, self.switchIP )

class PrefsDialog(tkSimpleDialog.Dialog):
    "Preferences dialog"

    def __init__(self, parent, title, prefDefaults):

        self.prefValues = prefDefaults

        tkSimpleDialog.Dialog.__init__(self, parent, title)

    def body(self, master):
        "Create dialog body"
        self.rootFrame = master
        self.leftfieldFrame = Frame(self.rootFrame, padx=5, pady=5)
        self.leftfieldFrame.grid(row=0, column=0, sticky='nswe', columnspan=2)
        self.rightfieldFrame = Frame(self.rootFrame, padx=5, pady=5)
        self.rightfieldFrame.grid(row=0, column=2, sticky='nswe', columnspan=2)

        # Field for Base IP
        Label(self.leftfieldFrame, text="IP Base:").grid(row=0, sticky=E)
        self.ipEntry = Entry(self.leftfieldFrame)
        self.ipEntry.grid(row=0, column=1)
        ipBase =  self.prefValues['ipBase']
        self.ipEntry.insert(0, ipBase)

        # Selection of terminal type
        Label(self.leftfieldFrame, text="Default Terminal:").grid(row=1, sticky=E)
        self.terminalVar = StringVar(self.leftfieldFrame)
        self.terminalOption = OptionMenu(self.leftfieldFrame, self.terminalVar, "xterm", "gterm")
        self.terminalOption.grid(row=1, column=1, sticky=W)
        terminalType = self.prefValues['terminalType']
        self.terminalVar.set(terminalType)

        # Field for CLI
        Label(self.leftfieldFrame, text="Start CLI:").grid(row=2, sticky=E)
        self.cliStart = IntVar()
        self.cliButton = Checkbutton(self.leftfieldFrame, variable=self.cliStart)
        self.cliButton.grid(row=2, column=1, sticky=W)
        if self.prefValues['startCLI'] == '0':
            self.cliButton.deselect()
        else:
            self.cliButton.select()

        # Selection of switch type
        Label(self.leftfieldFrame, text="Default Switch:").grid(row=3, sticky=E)
        self.switchType = StringVar(self.leftfieldFrame)
        self.switchTypeMenu = OptionMenu(self.leftfieldFrame, self.switchType, "Open vSwitch Kernel Mode", "Indigo Virtual Switch", "Userspace Switch", "Userspace Switch inNamespace")
        self.switchTypeMenu.grid(row=3, column=1, sticky=W)
        switchTypePref = self.prefValues['switchType']
        if switchTypePref == 'ivs':
            self.switchType.set("Indigo Virtual Switch")
        elif switchTypePref == 'userns':
            self.switchType.set("Userspace Switch inNamespace")
        elif switchTypePref == 'user':
            self.switchType.set("Userspace Switch")
        else:
            self.switchType.set("Open vSwitch Kernel Mode")


        # Fields for OVS OpenFlow version
        ovsFrame= LabelFrame(self.leftfieldFrame, text='Open vSwitch', padx=5, pady=5)
        ovsFrame.grid(row=4, column=0, columnspan=2, sticky=EW)
        Label(ovsFrame, text="OpenFlow 1.0:").grid(row=0, sticky=E)
        Label(ovsFrame, text="OpenFlow 1.1:").grid(row=1, sticky=E)
        Label(ovsFrame, text="OpenFlow 1.2:").grid(row=2, sticky=E)
        Label(ovsFrame, text="OpenFlow 1.3:").grid(row=3, sticky=E)

        self.ovsOf10 = IntVar()
        self.covsOf10 = Checkbutton(ovsFrame, variable=self.ovsOf10)
        self.covsOf10.grid(row=0, column=1, sticky=W)
        if self.prefValues['openFlowVersions']['ovsOf10'] == '0':
            self.covsOf10.deselect()
        else:
            self.covsOf10.select()

        self.ovsOf11 = IntVar()
        self.covsOf11 = Checkbutton(ovsFrame, variable=self.ovsOf11)
        self.covsOf11.grid(row=1, column=1, sticky=W)
        if self.prefValues['openFlowVersions']['ovsOf11'] == '0':
            self.covsOf11.deselect()
        else:
            self.covsOf11.select()

        self.ovsOf12 = IntVar()
        self.covsOf12 = Checkbutton(ovsFrame, variable=self.ovsOf12)
        self.covsOf12.grid(row=2, column=1, sticky=W)
        if self.prefValues['openFlowVersions']['ovsOf12'] == '0':
            self.covsOf12.deselect()
        else:
            self.covsOf12.select()

        self.ovsOf13 = IntVar()
        self.covsOf13 = Checkbutton(ovsFrame, variable=self.ovsOf13)
        self.covsOf13.grid(row=3, column=1, sticky=W)
        if self.prefValues['openFlowVersions']['ovsOf13'] == '0':
            self.covsOf13.deselect()
        else:
            self.covsOf13.select()

        # Field for DPCTL listen port
        Label(self.leftfieldFrame, text="dpctl port:").grid(row=5, sticky=E)
        self.dpctlEntry = Entry(self.leftfieldFrame)
        self.dpctlEntry.grid(row=5, column=1)
        if 'dpctl' in self.prefValues:
            self.dpctlEntry.insert(0, self.prefValues['dpctl'])

        # sFlow
        sflowValues = self.prefValues['sflow']
        self.sflowFrame= LabelFrame(self.rightfieldFrame, text='sFlow Profile for Open vSwitch', padx=5, pady=5)
        self.sflowFrame.grid(row=0, column=0, columnspan=2, sticky=EW)

        Label(self.sflowFrame, text="Target:").grid(row=0, sticky=E)
        self.sflowTarget = Entry(self.sflowFrame)
        self.sflowTarget.grid(row=0, column=1)
        self.sflowTarget.insert(0, sflowValues['sflowTarget'])

        Label(self.sflowFrame, text="Sampling:").grid(row=1, sticky=E)
        self.sflowSampling = Entry(self.sflowFrame)
        self.sflowSampling.grid(row=1, column=1)
        self.sflowSampling.insert(0, sflowValues['sflowSampling'])

        Label(self.sflowFrame, text="Header:").grid(row=2, sticky=E)
        self.sflowHeader = Entry(self.sflowFrame)
        self.sflowHeader.grid(row=2, column=1)
        self.sflowHeader.insert(0, sflowValues['sflowHeader'])

        Label(self.sflowFrame, text="Polling:").grid(row=3, sticky=E)
        self.sflowPolling = Entry(self.sflowFrame)
        self.sflowPolling.grid(row=3, column=1)
        self.sflowPolling.insert(0, sflowValues['sflowPolling'])

        # NetFlow
        nflowValues = self.prefValues['netflow']
        self.nFrame= LabelFrame(self.rightfieldFrame, text='NetFlow Profile for Open vSwitch', padx=5, pady=5)
        self.nFrame.grid(row=1, column=0, columnspan=2, sticky=EW)

        Label(self.nFrame, text="Target:").grid(row=0, sticky=E)
        self.nflowTarget = Entry(self.nFrame)
        self.nflowTarget.grid(row=0, column=1)
        self.nflowTarget.insert(0, nflowValues['nflowTarget'])

        Label(self.nFrame, text="Active Timeout:").grid(row=1, sticky=E)
        self.nflowTimeout = Entry(self.nFrame)
        self.nflowTimeout.grid(row=1, column=1)
        self.nflowTimeout.insert(0, nflowValues['nflowTimeout'])

        Label(self.nFrame, text="Add ID to Interface:").grid(row=2, sticky=E)
        self.nflowAddId = IntVar()
        self.nflowAddIdButton = Checkbutton(self.nFrame, variable=self.nflowAddId)
        self.nflowAddIdButton.grid(row=2, column=1, sticky=W)
        if nflowValues['nflowAddId'] == '0':
            self.nflowAddIdButton.deselect()
        else:
            self.nflowAddIdButton.select()

        # initial focus
        return self.ipEntry

    def apply(self):
        ipBase = self.ipEntry.get()
        terminalType = self.terminalVar.get()
        startCLI = str(self.cliStart.get())
        sw = self.switchType.get()
        dpctl = self.dpctlEntry.get()

        ovsOf10 = str(self.ovsOf10.get())
        ovsOf11 = str(self.ovsOf11.get())
        ovsOf12 = str(self.ovsOf12.get())
        ovsOf13 = str(self.ovsOf13.get())

        sflowValues = {'sflowTarget':self.sflowTarget.get(),
                       'sflowSampling':self.sflowSampling.get(),
                       'sflowHeader':self.sflowHeader.get(),
                       'sflowPolling':self.sflowPolling.get()}
        nflowvalues = {'nflowTarget':self.nflowTarget.get(),
                       'nflowTimeout':self.nflowTimeout.get(),
                       'nflowAddId':str(self.nflowAddId.get())}
        self.result = {'ipBase':ipBase,
                       'terminalType':terminalType,
                       'dpctl':dpctl,
                       'sflow':sflowValues,
                       'netflow':nflowvalues,
                       'startCLI':startCLI}
        if sw == 'Indigo Virtual Switch':
            self.result['switchType'] = 'ivs'
            if StrictVersion(MININET_VERSION) < StrictVersion('2.1'):
                self.ovsOk = False
                showerror(title="Error",
                          message='MiniNet version 2.1+ required. You have '+VERSION+'.')
        elif sw == 'Userspace Switch':
            self.result['switchType'] = 'user'
        elif sw == 'Userspace Switch inNamespace':
            self.result['switchType'] = 'userns'
        else:
            self.result['switchType'] = 'ovs'

        self.ovsOk = True
        if ovsOf11 == "1":
            ovsVer = self.getOvsVersion()
            if StrictVersion(ovsVer) < StrictVersion('2.0'):
                self.ovsOk = False
                showerror(title="Error",
                          message='Open vSwitch version 2.0+ required. You have '+ovsVer+'.')
        if ovsOf12 == "1" or ovsOf13 == "1":
            ovsVer = self.getOvsVersion()
            if StrictVersion(ovsVer) < StrictVersion('1.10'):
                self.ovsOk = False
                showerror(title="Error",
                          message='Open vSwitch version 1.10+ required. You have '+ovsVer+'.')

        if self.ovsOk:
            self.result['openFlowVersions']={'ovsOf10':ovsOf10,
                                             'ovsOf11':ovsOf11,
                                             'ovsOf12':ovsOf12,
                                             'ovsOf13':ovsOf13}
        else:
            self.result = None

    @staticmethod
    def getOvsVersion():
        "Return OVS version"
        outp = quietRun("ovs-vsctl --version")
        r = r'ovs-vsctl \(Open vSwitch\) (.*)'
        m = re.search(r, outp)
        if m is None:
            warn( 'Version check failed' )
            return None
        else:
            info( 'Open vSwitch version is '+m.group(1), '\n' )
            return m.group(1)


