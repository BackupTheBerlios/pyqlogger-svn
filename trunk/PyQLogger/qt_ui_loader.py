#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__           = u"Gustavo Sverzut Barbieri"
__author_email__     = u"gsbarbieri@users.sourceforge.net"
__maintainer__       = __author__
__maintainer_email__ = __author_email__
__version__          = "0.2"
__revision__         = '$Rev: $'


"""
This module provides a wrapper to QWidgetFactory, mimicking the C++ behavior.

The problem with Python version is that you can't get your connector
slots assigned by Qt since QWidgetFactory runs in C++ and doesn't know
nothing about Python classes.


This module tries to solve this problem parsing the UI xml file,
looking for <connection> tags and them checking if slots defined there
are available in the given connector, if so it creates a connection
using QObject.connect().


To provide the connector with useful data, it copies every attribute from
the generated QWidget (from QWidgetFactory) that is not in the
connector to it, so you can code it like if it have every methods and
attributes of a QWidget or the methods the QWidgetFactory will return.


Usage:

   class MyForm_Impl:
       def slotAction( self, s ):
           textLabel1 = self.child( 'textLabel1' )
           textLabel1.setText( 'some text: ' + str( s ) )
   

   import qt_ui_loader
   myform_impl = MyForm_Impl()
   myform = qt_ui_loader.create( 'myform.ui', myform_impl )
   

"""

import qt
import qtui
import xml.dom.minidom

def getConnections( ui_file ):
    """Get connections from UI file.

    This function parses the given UI file and get the <connection>
    elements, decode them to tuples and returns a list of existing
    connections.

    The returned list is in the following format:

       [ ( sender1, signal1, receiver1, slot1 ),
         ...
         ( senderN, signalN, receiverN, slotN ) ]
    """
    root = xml.dom.minidom.parse( ui_file )
    connections = root.getElementsByTagName( "connections" )
    c = []
    for e in connections:
        c += e.getElementsByTagName( "connection" )
    connections = c

    c = []
    for e in connections:
        # Get DOM elements
        sender   = e.getElementsByTagName( "sender" )[ 0 ]
        signal   = e.getElementsByTagName( "signal" )[ 0 ]
        receiver = e.getElementsByTagName( "receiver" )[ 0 ]
        slot     = e.getElementsByTagName( "slot" )[ 0 ]
        # Get DATA
        sender   = sender.firstChild.data.encode( "utf-8" )
        signal   = signal.firstChild.data.encode( "utf-8" )
        receiver = receiver.firstChild.data.encode( "utf-8" )
        slot     = slot.firstChild.data.encode( "utf-8" )

        c += [ ( sender, signal, receiver, slot ) ]
    return c
# getConnections()


def mix_objects( o1, o2 ):
    """Put attributes of o2 in o1.

    If an attribute of 'o2' doesn't exists in 'o1', put it there.
    """
    for d in dir( o2 ):
        if not hasattr( o1, d ):
            setattr( o1, d, getattr( o2, d ) )
# mix_objects()


def export_children( gp, object ):
    for child in object.children():
        name = child.name()
        if name and name != "unnamed":
            setattr( gp, name, child )
            export_children(gp, child )
# export_children()


def create( ui_file, connector=None, parent=None, exportchildren=False ):
    """Create a QWidget-based element reading the UI file. Tries to setup connections.

    ui_file        - the user interface filename  (.ui)
    connector      - class instance with implemented slots
    parent         - parent of the base widget
    exportchildren - if children are to be exported as attribute.

    This function is a wrapper to QWidgetFactory. When using dynamic
    UI you must implement the class with the desired connectors, but
    you can NOT do that in Python, since the QWidgetFactory runs in
    C++ and doesn't know about available Python classes.

    Using exportchildren=True, you can access children like this:
        widget.child_name
    otherwise you must use:
        child_name = widget.child( 'child_name' )

    My solution here is to parse the UI file, get the connections and
    check if them are available at the given 'connector', if so, do
    the QObject.connect call.

    Bear in mind that this is a hack, it generally works, but in order
    to have the same data available to your connector, IT COPIES THE
    ATTRIBUTES FROM THE CREATED QWidget TO YOUR CONNECTOR!!! This is
    not always reliable, but 'Works For Me [TM]'.
    """
    connections = getConnections( ui_file )
    widget      = qtui.QWidgetFactory.create( ui_file, None, parent )

    if exportchildren:
        export_children( widget, widget )
    
    # Mix widget and connector
    if connector:
        mix_objects( connector, widget )
        mix_objects( widget, connector )

    for sender, signal, receiver, slot in connections:
        # get sender from widgets:
        sender = widget.child( sender )
        signal = qt.SIGNAL( signal )
        if widget.name() == receiver:
            receiver = widget
        else:
            receiver = widget.child( receiver )
        # strip (...) from slot name, python does not need it
        slot = slot[ : slot.find( "(" ) ]

        # Connector implements this? If so connects
        try:
            s = getattr( connector, slot )
            if callable( s ):
                if sender:
                    qt.QObject.connect( sender, signal, s )
        except AttributeError:
            pass
    # for connections

    return widget
# create()
