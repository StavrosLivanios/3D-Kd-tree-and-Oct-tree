# -*- coding: utf-8 -*-
"""
Created on Thu Mar 26 21:22:55 2020

@author: ctzav
"""
from search import search_kn 
from anytree import Node, RenderTree

def delete(nodes, point):
    
      node =search_kn(nodes,point)
      
      if node.siblings :
         direction = node.dir
         parent = node.parent
         if dir == 'left' :
             paidia = list(parent.children)
             del parent.children
             parent.children = paidia 
             parent.children[1].dir = parent.dir 
             parent = parent.children[1]
             parent.children[1] = None 
         else :
             paidia = list(parent.children)
             del parent.children
             parent.children = paidia 
             parent.children[0].dir = parent.dir 
             parent = parent.children[0]
             parent.children[0] = None 
            
      del node
            
      #create files with the tree created
      DotExporter(nodes[0]).to_dotfile("root2.dot")
      DotExporter(nodes[0]).to_picture("root2.png")
        
          
    
    
    