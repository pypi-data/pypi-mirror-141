from dataclasses import dataclass
from unittest.mock import MagicProxy
import numpy as np


@dataclass
class ProcessedData():
    mcp:np.ndarray
    scRightUp:np.ndarray
    scRightBottom:np.ndarray
    scLeftBottom:np.ndarray
    scLeftUp:np.ndarray
    scCenter:np.ndarray
    time:np.ndarray
    
def processDataByMatrix(data:np.ndarray, timeSlice:float):
    mcp = np.zeros(shape=(1024,16))
    scRightUp = np.zeros(shape=(1024))
    scRightBottom = np.zeros(shape=(1024))
    scLeftBottom = np.zeros(shape=(1024))
    scLeftUp = np.zeros(shape=(1024))
    scCenter = np.zeros(shape=(1024))
    time = np.zeros(shape=(1024))
    
    for i in range(0,1024):
        for j in range(0,16):
            mcp[i][j]=data[i][j]
        scRightUp[i]=data[i][24]
        scRightBottom[i]=data[i][25]
        scLeftBottom[i]=data[i][26]
        scLeftUp[i]=data[i][27]
        scCenter[i]=data[i][28]
        time[i] = timeSlice*i
        
    return ProcessedData(mcp,scRightUp,scRightBottom,scLeftBottom,scLeftUp,scCenter,time)