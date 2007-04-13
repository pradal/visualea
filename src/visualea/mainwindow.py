# -*- python -*-
#
#       OpenAlea.Visualea: OpenAlea graphical user interface
#
#       Copyright or (C) or Copr. 2006 INRIA - CIRAD - INRA  
#
#       File author(s): Samuel Dufour-Kowalski <samuel.dufour@sophia.inria.fr>
#                       Christophe Pradal <christophe.prada@cirad.fr>
#
#       Distributed under the CeCILL v2 License.
#       See accompanying file LICENSE.txt or copy at
#           http://www.cecill.info/licences/Licence_CeCILL_V2-en.html
# 
#       OpenAlea WebSite : http://openalea.gforge.inria.fr
#

__doc__="""
QT4 Main window 
"""

__license__= "CeCILL v2"
__revision__=" $Id$ "


from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import SIGNAL

import ui_mainwindow
from pycutext import PyCutExt

from openalea.core import cli
from code import InteractiveInterpreter as Interpreter

from node_treeview import NodeFactoryTreeView, PkgModel, CategoryModel
from node_treeview import DataPoolListView, DataPoolModel
from node_treeview import SearchListView, SearchModel

import metainfo

from openalea.core.compositenode import CompositeNodeFactory
from openalea.core.observer import AbstractListener

from dialogs import NewGraph, NewPackage



class MainWindow(QtGui.QMainWindow,
                 ui_mainwindow.Ui_MainWindow,
                 AbstractListener) :

    def __init__(self, pkgman, session, parent=None):
        """
        @param pkgman : the package manager
        @param session : user session
        @param parent : parent window
        """

        QtGui.QMainWindow.__init__(self, parent)
        AbstractListener.__init__(self)
        ui_mainwindow.Ui_MainWindow.__init__(self)
        self.setupUi(self)

        self.pkgmanager = pkgman

        # Set observer
        self.initialise(session)

        # Array to map tab index with node widget
        self.index_nodewidget = []

        self.tabWorkspace.removeTab(0)

        # python interpreter
        interpreter = Interpreter()
        cli.init_interpreter(interpreter, session)
        self.interpreterWidget = PyCutExt(interpreter, cli.get_welcome_msg(), parent=self.splitter)

        # package tree view
        self.pkg_model = PkgModel(pkgman)
        self.packageTreeView = NodeFactoryTreeView(self, self.packageview)
        self.packageTreeView.setModel(self.pkg_model)
        self.vboxlayout.addWidget(self.packageTreeView)

        # category tree view
        self.cat_model = CategoryModel(pkgman)
        self.categoryTreeView = NodeFactoryTreeView(self, self.categoryview)
        self.categoryTreeView.setModel(self.cat_model)
        self.vboxlayout1.addWidget(self.categoryTreeView)

        # search list view
        self.search_model = SearchModel()
        self.searchListView = SearchListView(self, self.searchview)
        self.searchListView.setModel(self.search_model)
        self.vboxlayout2.addWidget(self.searchListView)


        # data pool list view
        self.datapool_model = DataPoolModel(session.datapool)
        self.datapoolListView = DataPoolListView(self, session.datapool, self.datapoolview)
        self.datapoolListView.setModel(self.datapool_model)
        self.vboxlayout3.addWidget(self.datapoolListView)


        # menu callbacks
        self.connect(self.action_About, SIGNAL("activated()"), self.about)
        self.connect(self.actionOpenAlea_Web, SIGNAL("activated()"), self.web)
        self.connect(self.action_Help, SIGNAL("activated()"), self.help)
        self.connect(self.action_Quit, SIGNAL("activated()"), self.quit)
        self.connect(self.action_Close_current_workspace, SIGNAL("activated()"),
                     self.close_workspace)
        self.connect(self.action_Auto_Search, SIGNAL("activated()"), self.find_wralea)
        self.connect(self.action_Add_File, SIGNAL("activated()"), self.add_wralea)
        self.connect(self.action_Run, SIGNAL("activated()"), self.run)
        self.connect(self.tabWorkspace, SIGNAL("contextMenuEvent(QContextMenuEvent)"),
                     self.contextMenuEvent)
        self.connect(self.action_Execute_script, SIGNAL("activated()"),
                     self.exec_python_script)
        self.connect(self.actionFind_Node, SIGNAL("activated()"),
                     self.find_node)

        self.connect(self.action_New_Session, SIGNAL("activated()"), self.new_session)
        self.connect(self.action_Open_Session, SIGNAL("activated()"), self.open_session)
        self.connect(self.action_Save_Session, SIGNAL("activated()"), self.save_session)
        self.connect(self.actionSave_as, SIGNAL("activated()"), self.save_as)

        self.connect(self.action_Export_to_Factory, SIGNAL("activated()"), self.export_to_factory)
        self.connect(self.actionExport_to_Application, SIGNAL("activated()"),
                     self.export_to_application)
        self.connect(self.actionShow_Pool, SIGNAL("activated()"), self.show_pool)
        self.connect(self.actionClear_Data_Pool, SIGNAL("activated()"), self.clear_data_pool)
        self.connect(self.search_lineEdit, SIGNAL("editingFinished()"), self.search_node)
        self.connect(self.action_New_Network, SIGNAL("activated()"), self.new_graph)
        self.connect(self.actionNew_Python_Node, SIGNAL("activated()"), self.new_python_node)
        self.connect(self.actionNew_Package, SIGNAL("activated()"), self.new_package)

        # final init
        self.session = session
        workspace_factory = self.session.user_pkg['Workspace']
        self.session.add_workspace(workspace_factory)
        self.open_widget_tab(workspace_factory)


    def about(self):
        """ Display About Dialog """
        
        mess = QtGui.QMessageBox.about(self, "About Visualea",
                                       "Version %s\n\n"%(metainfo.version) +
                                       "VisuAlea is part of the OpenAlea framework.\n"+
                                       u"Copyright \xa9  2006 INRIA - CIRAD - INRA\n"+
                                       "This Software is distributed under the GPL License.\n\n"+
                                       
                                       "Visit http://openalea.gforge.inria.fr\n\n"
                                       )

    def help(self):
        """ Display help """
        self.web()

    def web(self):
        """ Open OpenAlea website """
        QtGui.QDesktopServices.openUrl(QtCore.QUrl(metainfo.url))


    def quit(self):
        """ Quit Application """

        self.close()


    def notify(self, sender, event):
        """ Notification from observed """

        if(type(sender) == type(self.session)):
            self.update_tabwidget()
            #self.reinit_treeview()

        

    def closeEvent(self, event):
        """ Close All subwindows """
        
        for i in range(self.tabWorkspace.count()):
            w = self.tabWorkspace.widget(i)
            w.close()
        event.accept()


    def reinit_treeview(self):
        """ Reinitialise package and category views """

        self.cat_model.reset()
        self.pkg_model.reset()
        

    def close_workspace(self):
        """ Close current workspace """

        cindex = self.tabWorkspace.currentIndex()

        # Try to save factory if widget is a graph
        try:
            graph = self.index_nodewidget[cindex].node
            modified = graph.graph_modified
            if(modified):
                # Generate factory if user want
                ret = QtGui.QMessageBox.question(self, "Close Workspace",
                                                 "Graph has been modified.\n"+
                                                 "Do you want to report changes to factory ?\n",
                                                 QtGui.QMessageBox.Yes, QtGui.QMessageBox.No,)
            
                if(ret == QtGui.QMessageBox.Yes):
                    self.export_to_factory(graph)
        except:
            pass
           

        # Update session
        try:
            factory = self.index_nodewidget[cindex].factory
            self.session.close_workspace(factory)
            self.close_tab_workspace(cindex)
        except:
            pass
        

    def close_tab_workspace(self, cindex):
        """ Close workspace indexed by cindex cindex is Node"""
        
        w = self.tabWorkspace.widget(cindex)
        self.tabWorkspace.removeTab( cindex )
        w.close()
        w.emit(QtCore.SIGNAL("close()"))
        
        #self.index_nodewidget[cindex].release_listeners()
        del(self.index_nodewidget[cindex])
      

    def update_tabwidget(self):
        """ open tab widget """

        # open tab widgets
        for i in range(len(self.session.workspaces)):
            factory = self.session.workspaces[i]

            try:
                widget = self.index_nodewidget[i]
                if(factory != widget.factory):
                    self.close_tab_workspace(i)
            except: pass
            
            self.open_widget_tab(factory, pos = i)

        removelist = range( len(self.session.workspaces),
                        len(self.index_nodewidget))
        removelist.reverse()
        
        for i in removelist:
            self.close_tab_workspace(i)


    def open_widget_tab(self, factory, caption=None, pos = -1):
        """
        Open a widget in a tab giving the factory and an instance
        caption is append to the tab title
        """
        
        # Test if the node is already opened
        for i in range(len(self.index_nodewidget)):
            widget = self.index_nodewidget[i]
            f = widget.factory
            if(factory is f):
                self.tabWorkspace.setCurrentIndex(i)
                return

        container = QtGui.QWidget(self)
        container.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        widget = factory.edit_widget(parent=container)
        widget.wcaption = caption
        widget.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        vboxlayout = QtGui.QVBoxLayout(container)
        vboxlayout.addWidget(widget)

        if(not caption) : caption = factory.get_id()
        
        index = self.tabWorkspace.insertTab(pos, container, caption)
        self.tabWorkspace.setCurrentIndex(index)
        self.index_nodewidget.append(widget)

        return index
        

    def add_wralea(self):

        filename = QtGui.QFileDialog.getOpenFileName(self, "Add Wralea")
        self.pkgmanager.add_wralea(str(filename))
        self.reinit_treeview()

    
    def find_wralea(self):

        self.pkgmanager
        self.pkgmanager.find_and_register_packages()
        self.reinit_treeview()

    
    def run(self):
        """ Run the active workspace """

        cindex = self.tabWorkspace.currentIndex()
        self.index_nodewidget[cindex].node.eval()
        

    def export_to_factory(self, graph):
        """ Export current workspace composite node to its factory """

        if(not graph):
            cindex = self.tabWorkspace.currentIndex()
            graph = self.index_nodewidget[cindex].node
            
        graph.to_factory(graph.factory)
        graph.factory.package.write()


    def export_to_application(self):
        """ Export current workspace composite node to an Application """

        mess = QtGui.QMessageBox.warning(self, "Error",
                                         "This functionality is not yet implemented")


    def contextMenuEvent(self, event):
        """ Context menu event : Display the menu"""

        pos = self.tabWorkspace.mapFromGlobal(event.globalPos())
        
        tabBar = self.tabWorkspace.tabBar()
        count = tabBar.count()

        index = -1
        for i in range(count):
            if(tabBar.tabRect(i).contains(pos)):
                index = i
                break

        # if no bar was hit, return
        if (index<0) :  return 

        # set hitted bar to front
        self.tabWorkspace.setCurrentIndex(index)
        
        menu = QtGui.QMenu(self)

        action = menu.addAction("Close")
        self.connect(action, SIGNAL("activated()"), self.close_workspace)

        action = menu.addAction("Run")
        self.connect(action, SIGNAL("activated()"), self.run)

        action = menu.addAction("Apply changes")
        self.connect(action, SIGNAL("activated()"), self.export_to_factory)

        menu.move(event.globalPos())
        menu.show()


    def new_graph(self):
        """ Create a new graph """

        pkgs = self.pkgmanager.get_user_packages()
        
        dialog = NewGraph("New Dataflow", pkgs, self.pkgmanager.category.keys(), self)
        ret = dialog.exec_()

        if(ret>0):
            (name, nin, nout, pkg, cat, desc) = dialog.get_data()
            
            newfactory = CompositeNodeFactory(self.pkgmanager, name=name,
                                         description= desc,
                                         category = cat,
                                         )
            
            newfactory.set_nb_input(nin)
            newfactory.set_nb_output(nout)
            
            pkg.add_factory(newfactory)
            pkg.write()
            self.pkgmanager.add_package(pkg)

            self.reinit_treeview()

            self.session.add_workspace(newfactory)
            self.open_widget_tab(newfactory)


    def new_python_node(self):
        """ Create a new node """

        # Get default package
        pkgs = self.pkgmanager.get_user_packages()

        dialog = NewGraph("New Python Node", pkgs, self.pkgmanager.category.keys(), self)
        ret = dialog.exec_()

        if(ret>0):
            (name, nin, nout, pkg, cat, desc) = dialog.get_data()

            pkg.create_user_factory(name=name,
                                    description=desc,
                                    category=cat,
                                    nbin=nin,
                                    nbout=nout,
                                    )
            
            self.pkgmanager.add_package(pkg)
            self.reinit_treeview()


    def new_package(self):
        """ Create a new user package """

        dialog = NewPackage(self.pkgmanager.keys(), parent = self)
        ret = dialog.exec_()

        if(ret>0):
            (name, metainfo, path) = dialog.get_data()

            self.pkgmanager.create_user_package(name, metainfo, path)
            self.reinit_treeview()
        

    def exec_python_script(self):
        """ Choose a python source and execute it """
            
        filename = QtGui.QFileDialog.getOpenFileName(
            self, "Python Script", "Python script (*.py)")

        filename = str(filename)
        if(not filename) : return

        import code
        file = open(filename, 'r')
        
        sources = ''
        compiled = None
        
        for line in file:
            sources += line
            compiled = code.compile_command(sources, filename)

            if(compiled):
                self.interpreterWidget.get_interpreter().runcode(compiled)
                sources = ''


    def new_session(self):

        self.session.clear()
        self.session.add_workspace(self.session.user_pkg['Workspace'].instantiate())

        
    def open_session(self):

        filename = QtGui.QFileDialog.getOpenFileName(
            self, "OpenAlea Session", QtCore.QDir.homePath(), "XML file (*.xml)")

        filename = str(filename)
        if(not filename) : return

        self.session.load(filename)


    def export_graph(self):
        """ Export all open graph to there factory"""

        ret = QtGui.QMessageBox.question(self, "Export",
                                         "Graphs have been modified.\n"+
                                         "Do you want to report changes to Package Manager ?\n",
                                         QtGui.QMessageBox.Yes, QtGui.QMessageBox.No,)

        if(ret == QtGui.QMessageBox.No): return

        for widget in self.index_nodewidget:

            graph = widget.node
            try:
                self.export_to_factory(graph)
            except:
                pass


    def save_session(self):

        if(not self.session.session_filename):
            self.save_as()
        else :
            self.export_graph()
            self.session.save(self.session.session_filename)

        
    def save_as(self):

        self.export_graph()
        filename = QtGui.QFileDialog.getSaveFileName(
            self, "OpenAlea Session",  QtCore.QDir.homePath(), "XML file (*.xml)")

        filename = str(filename)
        if(not filename) : return

        self.session.save(filename)
        

    def show_pool(self):
        """ Show the data pool """

        i = self.tabPackager.indexOf(self.datapoolview)
        self.tabPackager.setCurrentIndex(i)
        

    def clear_data_pool(self):
        """ Clear the data pool """

        self.session.datapool.clear()


    def search_node(self):
        """ Activated when search line edit is validated """

        results = self.pkgmanager.search_node(str(self.search_lineEdit.text()))
        self.search_model.set_results(results)
        

    def find_node(self):
        """ Find node Command """

        i = self.tabPackager.indexOf(self.searchview)
        self.tabPackager.setCurrentIndex(i)
        self.search_lineEdit.setFocus()
       


        

