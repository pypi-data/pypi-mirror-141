""" layout definition and tools """
from pydantic import BaseModel, validator  
from typing import List, Optional, Union , Iterable, Tuple 

from pydevmgr_core import BaseDevice, BaseManager

from PyQt5.QtWidgets import QLayout, QBoxLayout, QGridLayout, QWidget
from PyQt5 import QtCore
from PyQt5.uic import loadUi

from .base import get_widget_factory, BaseUiLinker, WidgetFactory
from .io import find_ui 
import glob



class ConfigLayoutSetup(BaseModel):
    layout: str = "ly_devices" 
    device: Union[str, Iterable] = "*"
    dev_type: Union[str, Iterable]  = "*"
    
    exclude_device: Union[str, Iterable] = ""
    exclude_dev_type: Union[str, Iterable]  = ""
    
    widget_kind: str = "ctrl"
    widget_class: Optional[str] = None
    alt_layout: Union[str,Iterable] = []
    column: int = 0
    row: int = 0
    columnSpan: int = 1
    rowSpan: int = 1
    
    stretch: int = 0
    alignment: int = 0 
    
    class Config:
        extra = 'forbid'
    
    @validator("alt_layout")
    def _liste_me(cls, value):
        return [value] if isinstance(value, str) else value


class ConfigLayout(BaseModel):
    """ One item that define a layout compose from a ui resource file and a setup """

    ui_file: str = "simple_devices_frame.ui"
    setup: List[ConfigLayoutSetup] = ConfigLayoutSetup(device="*", layout="ly_devices", widget_kind="ctrl")
    size: Optional[List] = None

    @validator("ui_file")
    def _validate_ui_file(cls, ui_file):
        """ Check if ui_file exists in resources """
        try:
            find_ui(ui_file) 
        except IOError as e:
            raise ValueError(e)
        return ui_file






def _obj_to_match_func(obj):
    if not obj:
        return lambda name: False 
    if isinstance(obj, str):
        return lambda name: glob.fnmatch.fnmatch(name, obj)
    elif hasattr(obj, "__iter__"): 
        return  lambda name: name in obj


def insert_widget(
     device: BaseDevice, 
     layout: QLayout, 
     widget_kind: str, *,
     default_factory: Optional[WidgetFactory] = None,
    
     column: int = 0,
     row: int = 0,
     columnSpan: int = 1,
     rowSpan: int = 1,
     
     stretch: int = 0,
     alignment: int = 0        
    ) -> BaseUiLinker:
    """ Insert one device widget inside a QT Layout object 
    
    Args:
        device (BaseDevice): list of devices 
        layout: (QLayout)
        widget_kind (str):  e.g. "line", "ctrl", "cfg" 
        
    
    Returns:
       linker (BaseUiLinker): A device linker object (not yet connected to device)
       
    """
    factory = get_widget_factory(widget_kind, device.config.type, default=default_factory)       
    linker = factory.build()
    
    widget = linker.widget 
    if isinstance(layout, QBoxLayout): 
        layout.addWidget(widget, stretch, QtCore.Qt.AlignmentFlag(alignment))
    elif isinstance(layout, QGridLayout):
        layout.addWidget(widget, row, column, rowSpan, columnSpan)
    else:
        layout.addWidget(widget)  
    return linker 

def insert_widgets(
      devices: List[BaseDevice], 
      layout: QLayout, 
      widget_kind: str, *, 
      direction: int = 0, # 0 for row 1 for column
      column: int = 0,
      row: int = 0,
      **kwargs
    ) -> List[Tuple[BaseDevice,BaseUiLinker]]:
    """ Insert devices widgets inside a QT Layout object 
    
    Args:
        device (list): list of devices 
        layout: (QLayout)
        widget_kind (str):  e.g. "line", "ctrl", "cfg" 
        
    
    Returns:
       device_linker (list): A list of (device, linker) tuple
       
    """
    
    if direction:
        return [(device,insert_widget(device, layout, widget_kind, column=column+i, row=row, **kwargs)) for i,device in enumerate(devices)]
    else:
        return [(device,insert_widget(device, layout, widget_kind, row=row+i, column=column, **kwargs)) for i,device in enumerate(devices)]
        
        





class LayoutSetup:
    """ Use to define the creation of a widget inside a QLayout 
    
    All argument are optional except ``layout`` 
    
    Args:
       - layout (str): layout name found in the ui 
       - device (str,list):  add widget  of matching name device can be a glob to match (e.g. motor[1-4])
                        This can be also a list of strict names 
       - dev_type (str,list): add widget matching the given device type ('Any' will match all devices) (e.g. Motor)
                        This can be also a list of strict type
       - exclude_device (str,list): work as `device` but for exclusion 
       - exclude_dev_type (str,list): work as `dev_type` but for exclusion 
       - widget_kind (str):  The widget kind  "line", "ctrl", "cfg"
       - widget_class (str): Can be use if a device has no widget defined one can use the widget of an other type 
       - alt_layout (str,Iterable): If layout is not found try with the alternative ones 
       
       - column (int):  default, 0. Used only if the layout is a QGridLayout 
       - row (int): default, 0. Used only if the layout is a QGridLayout 
       - columnSpan (int): default, 1. Used only if the layout is a QGridLayout 
       - rowSpan (int):  default, 1. Used only if the layout is a QGridLayout 
       
       - stretch (int):  default, 0. Used only if the layout is a QBoxLayout
       - alignment (int): default, 0. Used only if the layout is a QBoxLayout see PyQt5 doc           
    """
    Config = ConfigLayoutSetup
             
    def __init__(self, config=None, **kwargs):
        if config is None:
            self.config = self.Config(**kwargs)
        else:
            self.config = config
        
    def filter_devices(self, devices: Iterable[BaseDevice]) -> List[BaseDevice]:
        """ Collect devices from the manager according to matching rules 
        
        The mathcing rules are defined by the properties :
        
        - device: Union[str, Iterable] = "*"
        - dev_type: Union[str, Iterable]  = "*"        
        - exclude_device: Union[str, Iterable] = ""
        - exclude_dev_type: Union[str, Iterable]  = ""
        
        Returns:
           devices: list of matching devices
        """
        
        c = self.config
        output_devices = []
        match_device = _obj_to_match_func(c.device)
        match_type   = _obj_to_match_func(c.dev_type)
        
        exclude_match_device = _obj_to_match_func(c.exclude_device)
        exclude_match_type   = _obj_to_match_func(c.exclude_dev_type)
        for device in devices:        
            if exclude_match_device(device.name): continue
            if exclude_match_type(device.config.type): continue
            if match_device(device.name) and match_type(device.config.type):
                output_devices.append(device)  
        return output_devices
    
    def find_layout(self, ui: QWidget) -> QLayout:
        """ find a layout from a parent ui according to config 
        
        Look for a layout named as .layout properties. If not found look inside 
        the .alt_layout list property. 
        """
        layout = ui.findChild(QLayout, self.config.layout)
        if layout is None:
            for ly_name in self.config.alt_layout:
                layout = ui.findChild(QLayout, ly_name)
                if layout: break
            else:
                raise ValueError(f"Cannot find layout with the name {self.name!r} or any alternatives")
        return layout
    
    

    def insert_widgets(self, 
          devices: Iterable[BaseDevice], 
          ui: QWidget
        ) -> list:
        
        devices = self.filter_devices(devices)
        layout = self.find_layout(ui)
        c = self.config     

        kws = c.dict(
                include = set([ "column","row", "columnSpan","rowSpan","stretch","alignment" ])
                )
                

        return insert_widgets(devices, layout, c.widget_kind, **kws)
       
class Layout:
    """ Class to handle one layout definition and insert widget in the proper ui """
    Config = ConfigLayout    
     
    def __init__(self, config=None, **kwargs):
        if config is None:
            self.config = self.Config(**kwargs)
        else:
            self.config = config
    
    def load_ui(self):
        return loadUi(find_ui(self.config.ui_file))


    def insert_widgets(self, 
            devices: Iterable[BaseDevice], 
            ui: Optional[QWidget] = None
        ) -> list:
        """ Insert widget inside the given ui according to rules defined in .config 

        Args:
            devices (List[BaseDevice]): List of devices to filter and insert according to rules
            ui (optional, QWidget): An ui widget. If not given the one defined in config.ui_file is loaded  (and
            returned)

        Outputs:
            ui:  the ui widget
            (device, linker):  a pair of device and BaseUiLinker class (both are not connected)
        """
        if ui is None:
            ui = self.load_ui()
        
        device_linker = []
        for setup in self.config.setup:
            ls = LayoutSetup(setup)
            device_linker.extend( ls.insert_widgets(devices, ui) )
        return ui, device_linker
   



class DevicesLinker(BaseUiLinker):
    pass

