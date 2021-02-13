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
    area = np.sum(grid_gla_proj['geometry'].area/1e6)
    grid_['area'] = area
    print(t)
    return grid_


if __name__=='__main__':
    glo_grid = gpd.read_file('global_grid.shp')
    path = 'glacier_file'
    rgi_folder = os.listdir(path)
    gla_path = [os.path.join(path, i) for i in rgi_folder if '.shp' in i]
    for i in gla_path:
        gla = gpd.read_file(i)    
        gla_grids = gpd.sjoin(glo_grid, gla).drop_duplicates('FID')
        gla_grids = gla_grids.loc[:,['FID','geometry']]
        area_func = partial(grid_glacier_area, gla)
        cores = mp.cpu_count()
        pool = mp.Pool(cores)
        grids = [gla_grids.loc[[i]] for i in gla_grids.index]
        res = pool.map(area_func, grids)
        grid_area = pd.concat(res)
        outpath = 'result_file'+i[64:]
        grid_area.to_file(outpath)

t2=time.time()

print("totally cost",t2-t1)