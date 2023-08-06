#!/usr/bin/env python
# coding: utf-8

# Copyright (c) nicolas allezard.
# Distributed under the terms of the Modified BSD License.

"""
TODO: Add module docstring
"""

from ipywidgets import DOMWidget,CallbackDispatcher,Widget,Layout

from traitlets import Unicode, Bool, validate, TraitError,Int,List,Dict,Bytes,Any,Instance,Union

from ._frontend import module_name, module_version
import numpy as np
import base64
import cv2
import copy


from pathlib import Path
from urllib.request import urlopen
from PIL import Image
import io

def tobytes(img):
    """Encode matrix to base64 image string"""
    retval, buffer = cv2.imencode('.png', img)
   
    return bytes(buffer.data)


class Polaroid(DOMWidget):
    """TODO: Add docstring here
    """
    _model_name = Unicode('PolaroidModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode('PolaroidView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)

    
    caption=Unicode('Hello World').tag(sync=True)
    image= Any().tag(sync=True) 
    im_format=Unicode('png').tag(sync=True)
    _mouse_down_callbacks = Instance(CallbackDispatcher, ())
    _client_ready_callbacks = Instance(CallbackDispatcher, ())
    _id=Unicode('polaroid').tag(sync=True)
    width=Int(200).tag(sync=True)
    height=Int(220).tag(sync=True)
    selected=Bool(False).tag(sync=True)

    def __init__(self, *args, **kwargs):
        # print( kwargs)
        
        super(Polaroid, self).__init__(*args, **kwargs)


        if self.layout.min_width is None :
            if 'width' in kwargs :  
                self.layout.min_width=str(kwargs['width']+15)+"px"
            else : 
                self.layout.min_width=str(self.width+15)+"px"

        if self.layout.min_height is None :
            if 'height' in kwargs :  
                self.layout.min_height=str(kwargs['height'])+"px"
            else : 
                self.layout.min_height=str(self.height)+"px"



        self.on_msg(self._handle_frontend_event)

    def on_mouse_down(self, callback, remove=False):
        """Register a callback that will be called on mouse click down."""
        self._mouse_down_callbacks.register_callback(callback, remove=remove)
    
    # Events
    def on_client_ready(self, callback, remove=False):
        """Register a callback that will be called when a new client is ready to receive draw commands.
        When a new client connects to the kernel he will get an empty Canvas (because the canvas is
        almost stateless, the new client does not know what draw commands were previously sent). So
        this function is useful for replaying your drawing whenever a new client connects and is
        ready to receive draw commands.
        """
        self._client_ready_callbacks.register_callback(callback, remove=remove)


    def _handle_frontend_event(self, _, content, buffers):
        
        if content.get("event", "") == "client_ready":
            self._client_ready_callbacks()
        
        if content.get("event", "") == "mousedown":
            self._mouse_down_callbacks(content)    
    
    @validate('width')
    def _valid_width(self, proposal):
        #layout=Layout(min_width=str(proposal['value'])+"px")
       
        return proposal['value']

    @validate('image')
    def _valid_image(self, proposal):
        if isinstance(proposal['value'], str):
            #print(type(proposal['value']),proposal['value'])
            #print("string")
            filename=proposal['value']
            if 'http' in filename:
                data=filename
                self.im_format='url'
                
            else:
                abs_filename=Path(filename).absolute().as_posix()
                #print(abs_filename)
                self.im_format=abs_filename.split(".")[-1]

                data=open(abs_filename,"rb").read()
                #print(type(data))
                #data = base64.b64encode(data).decode()
            return data
        elif str(type(proposal['value']))== "<class 'numpy.ndarray'>" :
            #print(type(proposal['value']),proposal['value'].shape)

            data=tobytes(proposal['value'])
            im_format='png'
            return data
            
        elif isinstance(proposal['value'],Image.Image):
            #print("pil image")
            img_byte_arr = io.BytesIO()
            proposal['value'].save(img_byte_arr, format='PNG')
            im_format='png'
            return img_byte_arr.getvalue()
        else:
            raise TraitError('Invalid type: must be a string, a numpy ndarray or a PIL image, but receive '+str(type(proposal['value'])))
        return None



class Carousel(DOMWidget):
    """TODO: Add docstring here
    """
    _model_name = Unicode('CarouselModel').tag(sync=True)
    _model_module = Unicode(module_name).tag(sync=True)
    _model_module_version = Unicode(module_version).tag(sync=True)
    _view_name = Unicode('CarouselView').tag(sync=True)
    _view_module = Unicode(module_name).tag(sync=True)
    _view_module_version = Unicode(module_version).tag(sync=True)
    _id=Unicode('Carousel').tag(sync=True)

    
  

    image_list=List().tag(sync=True)
    images=List().tag(sync=True)
    images_index=List().tag(sync=True)
    image_captions=List().tag(sync=True)
    im_format=Unicode('png').tag(sync=True)

    selected_id=List().tag(sync=True)
    width=Int().tag(sync=True)
    height=Int().tag(sync=True)

    item_width=Int().tag(sync=True)
    item_height=Int().tag(sync=True)

    _on_click_callbacks = Instance(CallbackDispatcher, ())

    chunk_size=Int(32)
    count=Int(0)


    def __init__(self, *args, **kwargs):
        super(Carousel, self).__init__(*args, **kwargs)
        #print('Carousel')
        self.on_msg(self._handle_frontend_event)
        self.chunk_size=32
        self.chunk_begin=0
        self.chunk_end=0
        self.count=0
        self.send({"touch_item":{"index":10,"new":{} } })
    
   

    def on_click(self, callback, remove=False):
        """Register a callback that will be called on mouse click down."""
        self._on_click_callbacks.register_callback(callback, remove=remove)
     

    def _handle_frontend_event(self, _, content, buffers):
        #print("content",content)

        if content.get("send_data", ""):
            self._send_data(content)
        
        if "selected" in content.get("event", "") :
            self._on_click_callbacks(content)



    def setImageData(self,index,image=None,caption=None,format=None):
        image_data,image_format=self.convertImage(image)
        msg={"index":index,"caption":caption,"format":image_format if not format else format}
        #print("format",image_format)

        if image_format=="url": 
            image_data=bytes(image_data,'utf-8')
        if image is not None:
            self.send({"set_image":msg},{image_data})
        else:
            self.send({"set_image":msg})


    def convertImage(self,image):
        image_data,image_format=None,None
        if isinstance(image, str):
            filename=image
            if 'http' in filename:
                image_data=filename
                image_format='url'
            else:
                abs_filename=Path(filename).absolute().as_posix()
                image_format=abs_filename.split(".")[-1]
                image_data=open(abs_filename,"rb").read()
            
        elif str(type(image))== "<class 'numpy.ndarray'>" :
            image_data=tobytes(image)
            image_format='png'
            
        elif isinstance(image,Image.Image):

            img_byte_arr = io.BytesIO()
            image.save(img_byte_arr, format='PNG')
            image_format='png'
            image_data=img_byte_arr.getvalue()

        return image_data,image_format

    def _send_data(self,content):
        #print("front demand data",content)

        self.count+=1
        returned_list=[]
        
        #print("before",self.chunk_begin,self.chunk_end)

        begin,end,_=content["send_data"]

        if (begin>=self.chunk_begin and begin<self.chunk_end) and  (end>=self.chunk_begin   and end<self.chunk_end):
            #print("send NULL",['-',self.count])
            self.image_list=['-',self.count]
            return 

        self.chunk_begin=begin

        self.chunk_end=self.chunk_begin+self.chunk_size
        
        if self.chunk_end<end : self.chunk_end=end
        
        self.chunk_end = self.chunk_end  if self.chunk_end<=len(self.images) else len(self.images) 
        
        #print("python going to send ",self.chunk_begin,self.chunk_end)

        for i  in range(self.chunk_begin,self.chunk_end):
            image_data,image_format=self.convertImage(self.images[i])
            returned_list+=[[image_data,i]]

            
        if len(returned_list)>0:
            self.image_list=returned_list
        else:
            #print("send NULL",['-',self.count])
            self.image_list=['-',self.count]
    

           
    @validate('images')
    def _valid_images(self, proposal):
        #print('VALID',proposal['value'])
        self.count+=1
        returned_list=[]
       
        self.images_index=list(range( len(proposal.value)) ) 
           

        for i,prop in enumerate(proposal['value']):

            if i>=self.chunk_size: break

            if prop == '-': return ['-',self.count]
            image_data,image_format=self.convertImage(prop)
            returned_list+=[[image_data,i]]
            
        self.image_list=returned_list
        
        return proposal["value"]