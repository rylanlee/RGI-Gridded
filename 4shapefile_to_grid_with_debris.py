#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec  5 18:20:54 2019

@author: liyaojun
"""

import geopandas as gpd
import pandas as pd
import numpy as np
import os
import multiprocessing as mp
import time
from functools import partial
from copy import copy

t1 = time.time()


def grid_glacier_area(gla, grid):
    t = time.time()
    grid_ = copy(grid)
    grid_gla = gpd.overlay(gla, grid, how='intersection')
    grid_gla_proj = grid_gla.to_crs('+proj=moll +lon_0=0')
    debris = np.sum(grid_gla_proj['geometry'].area/1e6)
    grid_['debris'] = debris
    print(t)
    return grid_


if __name__=='__main__':
    glo_grid = gpd.read_file('/media/iceman/Seagate Expansion Drive/rgi gridded/global grid shapefile/0.5_degree_grid.shp').to_crs({'init': 'epsg:4326'})
    path = '/media/iceman/Data/Glacier dataset/debris_cover'
    rgi_folder = os.listdir(path)
    gla_path = [os.path.join(path, i) for i in rgi_folder if '.shp' in i]
    gla_path.sort()
    for i in gla_path:
        gla = gpd.read_file(i).to_crs({'init': 'epsg:4326'})    
        gla_grids = gpd.sjoin(glo_grid, gla).drop_duplicates('FID')
        gla_grids = gla_grids.loc[:,['FID','geometry']]
        area_func = partial(grid_glacier_area, gla)
        cores = mp.cpu_count()-2
        pool = mp.Pool(cores)
        grids = [gla_grids.loc[[i]] for i in gla_grids.index]
        res = pool.map(area_func, grids)
        grid_area = pd.concat(res)
        outpath = '/media/iceman/Data/rgi_grid_debris/'+i[48:]
        grid_area.to_file(outpath)

t2=time.time()

print("totally cost",t2-t1)