# -*- coding: utf-8 -*-
"""
Created on Wed Aug  7 10:21:30 2019

@author: Li Yaojun
Email: liyaojun2008@126.com

Better late than never.
"""

import numpy as np
import geopandas as gpd
from shapely.geometry import Polygon


# create polygons 
def create_vector_polygon(x_size, y_size, r_crs, uy=None, ly=None, lx=None, rx=None):
    
    """create a vector polygon with certain boundary
    
    Parameters
    ----------
    uy : int: the upper boundary
    ly : int: the lower boundary
    lx : int: the left boundary
    rx : int: the right boundary
    x_size : int: the width of each grid
    y_size : int: the hight of each grid
    crs : objection
    
    return
    ------
    grid_gdf : a geopandas.GeoDataFrame
    """
    
    # test parameters
    if uy == None:
        uy = 90
    if ly == None:
        ly = -90
    if lx == None:
        lx = -180
    if rx == None:
        rx = 180

    
    xs = np.arange(lx, rx+x_size, x_size)
    ys = np.arange(ly, uy+y_size, y_size)
    geom_list = []
    for i in range(1, len(xs)):
        x0, x1 = xs[i-1], xs[i]
        for j in range(1, len(ys)):
            y0, y1 = ys[j-1], ys[j]
            coord = ((x0, y0), (x1, y0), (x1, y1), (x0, y1), (x0, y0))
            geom = Polygon(coord)
            geom_list.append(geom)

    grid_gdf = gpd.GeoDataFrame(data =  geom_list,
                            columns = ['geometry'],
                            index = range(len(geom_list)),
                            crs = r_crs.crs)
    return grid_gdf

