from .base import BaseUiLinker, WidgetControl
from .layouts import LayoutSetup
from pydantic import BaseModel, validator
from typing import Iterable, Union, Optional, List, Dict
from .io import find_ui
from pydevmgr_core import _BaseObject, BaseData



from PyQt5.QtWidgets import QLayout, QBoxLayout, QGridLayout, QVBoxLayout, QWidget
from PyQt5 import QtCore
from PyQt5.uic import loadUi



#    _  _     __  __       _ _   _   _     _       _             
#  _| || |_  |  \/  |_   _| | |_(_) | |   (_)_ __ | | _____ _ __ 
# |_  ..  _| | |\/| | | | | | __| | | |   | | '_ \| |/ / _ \ '__|
# |_      _| | |  | | |_| | | |_| | | |___| | | | |   <  __/ |   
#   |_||_|   |_|  |_|\__,_|_|\__|_| |_____|_|_| |_|_|\_\___|_|   
                                                               


line_setup = LayoutSetup.Config(widget_kind="line", device="*")
ctrl_setup = LayoutSetup.Config(widget_kind="ctrl", device="*")



class ConfigLayout(BaseModel):
    """ One item that define a layout compose from a ui resource file and a setup """
    setup: List[LayoutSetup.Config] = LayoutSetup.Config()
    size: Optional[List] = None
    ui_file: Optional[str] = None

    @validator("ui_file")
    def _validate_ui_file(cls, ui_file):
        """ Check if ui_file exists in resources """
        if ui_file is not None:
            try:
                find_ui(ui_file) 
            except IOError as e:
                raise ValueError(e)
        return ui_file





line_setup =  ConfigLayout(setup = [LayoutSetup.Config(widget_kind="line", device="*")])
ctrl_setup =  ConfigLayout(setup = [LayoutSetup.Config(widget_kind="ctrl", device="*")])


class ConfigMultiView(BaseModel):
    views : Dict[str,ConfigLayout] = {"line":line_setup, "ctrl":ctrl_setup}

 
class ViewUiLinker(BaseUiLinker):
    Config = ConfigLayout
    _device_linkers  = None       
    
    class Widget(QWidget):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            # make a very simple widget with one single layout named ly_devices
            # do not change the layouut_name 
            layout = QVBoxLayout(objectName="ly_devices") # give a default name for the layout 
            self.setLayout(layout)

    @classmethod
    def new_widget(self, config):
        if config.ui_file:
            return loadUi(find_ui(config.ui_file))
        else:
            return self.Widget()

    def _link(self, downloader, obj_list, data):
        for device, linker in self._device_linkers:
            linker.connect( downloader, device )
        


    def connect(self, downloader, obj_list, data = None):
        if data is None:
            data = self.new_data()
        self.setup_ui( obj_list , data)
        self._link(downloader, obj_list, data)
        
        return WidgetControl( self, downloader, obj_list, data )
       
    def disconnect(self):
        super().disconnect()
        if self._device_linkers:
            for _, linker in self._device_linkers:
                linker.disconnect()
    
    def setup_ui(self, obj_list: List[_BaseObject], data: BaseData):
        self.disconnect()
        self.clear()
            
        self._device_linkers = []
        for setup in self.config.setup:
            ls = LayoutSetup(setup)
            self._device_linkers.extend( ls.insert_widgets(obj_list, self.widget) )

    def clear(self):
        if self._device_linkers:
            for d,l in self._device_linkers:
                l.widget.setParent(None)
    
class MultiViewLinker(BaseUiLinker):
    Config = ConfigMultiView
    
    class Data(BaseModel):
        current_view: str = "line"
    
    class Widget(QWidget):
        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)
            self.container_layout = QVBoxLayout()
            self.setLayout(self.container_layout)
    
    _view_linker = None

    def _link(self, downloader, obj_list, data):
        self._view_linker._link(downloader, obj_list, data)

    def connect(self, downloader, obj_list, data = None):
        if data is None:
            data = self.new_data()
        self.setup_ui(obj_list, data)
        #self._view_linker.connect(downloader, obj_list)
        self._link(downloader, obj_list, data)

        return WidgetControl( self, downloader, obj_list, data )

    def disconnect(self):
        super().disconnect()
        if self._view_linker:
            self._view_linker.disconnect()
    
    def clear(self):
        if self._view_linker:
            self._view_linker.clear()
            self._view_linker.widget.setParent(None)
        
    def setup_ui(self, obj_list: List[_BaseObject], data: BaseData):
        self.disconnect()
        self.clear()
        self._view_linker = None

        view = self.config.views[data.current_view]

        vl = ViewUiLinker(config=view)
        self.widget.container_layout.addWidget(vl.widget)
        vl.setup_ui( obj_list,  vl.new_data() ) 
        self._view_linker = vl
