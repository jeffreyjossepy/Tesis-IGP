from ExtractData import * 

"""
File : AlternatePLot.py
-----------------------
This file construct a series of plots arranged in a matrix format, whose size is specified by the length of p2(rows) and p3(columns) respectively, p1 determines the different curves in each plot. It first search and arrange the data sets matching the parameter values specified by p1,p2,p3 and the basaline params in a list of lists of lists of dictionarys.Then it creates each plot in a iterative manner, this code assumes that the Matrix of plots has at least dimension 4.
"""


import matplotlib.pyplot as plt
import matplotlib as mpl

def PlotInt(Directory,params,Types,p1,p2,p3,TypeDict,sizePlot,plotParamsDict,Colors,LineStyles,yLabel,xLabel):
    fig,axes = makeFigure(p2,p3,sizePlot)
    Datasets = GetDataSets(Directory,params,Types,p1,p2,p3,TypeDict)
    plotData(Datasets,axes,plotParamsDict,Colors,LineStyles)
    editplot(axes,yLabel,xLabel)

def editplot(axes,yLabel,xLabel):
    editaxis(axes)
    makeLines(axes,2,3)
    addLabels(axes,yLabel,xLabel)

def makeLines(axes,nrows,ncols):
    for i in range(nrows):
        for j in range(ncols):
            plotlines(axes[i,j])

def plotlines(ax):
    ax.plot([-13,7],[0,0], 'k--')
    ax.plot([0,0],[-13,7],'k--')
    ax.plot([-13,7],[13,-7],'k--')
    
    
def editaxis(axes):
    axes[0][0].set_xlim([-13,7])
    axes[0][0].set_ylim([-13,7])

def addLabels(axes,yLabel,xLabel):
    axes[0][0].set_ylabel(yLabel)
    axes[1][0].set_ylabel(yLabel)
    axes[1][1].set_xlabel(xLabel)


def makeFigure(p2,p3,sizePlot):
    p2Name = p2.keys()[0]
    p = p3.values()[0][0]
    return plt.subplots(nrows=len(p3.values()[0]),ncols=len(p2[p2Name][p]),sharex =True,sharey=True,figsize = sizePlot)


def plotData(Datasets,axes,plotParamsDict,Colors,LineStyles):
    for i in range(len(Datasets)):
        for j in range(len(Datasets[i])):
            InnerPlot(Datasets[i][j],axes[i,j],plotParamsDict,Colors,LineStyles)


def InnerPlot(Datasets,canvas,plotParamsDict,Colors,LineStyles):
    for k in range(len(Datasets)):
        for Type in Types:
            UpdateplotParams(plotParamsDict,Type,Colors[k],LineStyles[k])
            Datasets[k][Type].plot(canvas,*plotParamsDict[Type])
        

def UpdateplotParams(plotParamsDict,Type,col,lin):
    Z = plotParamsDict[Type]
    Color = Z[0]
    Line = Z[1]
    Tag = Z[2][0]
    Color[Tag] = col
    Line[Tag] = lin

    
def LoadInv(dataset):
    P = InputInvData(dataset)
    return P.Read(',')

TypeDict = {'Zones':  LoadInv,'Inv': LoadInv}   
ColorCoder = {'Z(IC5)':'b'}
LineCoder = {'Z(IC5)':'--'}

Colors = [ 'b' ,'g','y','r']
LineStyles = ['-','-','-','-']

plotParamsDict= {'Zones':[ColorCoder,LineCoder,['MutualInv']]}
sizePlot = (10,8)
yLabel = r'$\log_{10}(k_{RC})$'
xLabel = r'$\log_{10}(k_{CP})$'


def GeneratePlots(DirData,DirPlots,params,Types,p1,p2,p3,TypeDict,TypeCurves,sizePlot,plotParamsDict,Colors,LineStyles,yLabel,xLabel,LabelMap,FStra,bs):
    for Curves in TypeCurves:
        print Curves
        GenerateCurves(DirData,DirPlots,params,Types,p1,p2,p3,TypeDict,Curves,sizePlot,plotParamsDict,Colors,LineStyles,yLabel,xLabel,LabelMap,FStra,bs)
    


def GenerateCurves(Dir,DirPlots,params,Types,p1,p2,p3,TypeDict,Curves,sizePlot,plotParamsDict,Colors,LineStyles,yLabel,xLabel,LabelMap,FStra,bs):
    plotParamsDict[Types[0]][2] = [Curves]
    for Strategy in FStra:
        params['fmPR']= [Strategy]
        for b in bs:
            params['b'] = [b]
            Label = generateLabel(DirPlots,LabelMap,Curves,Strategy,b)
            PlotInt(Dir,params,Types,p1,p2,p3,TypeDict,sizePlot,plotParamsDict,Colors,LineStyles,yLabel,xLabel)
            plt.savefig(Label+".pdf")
            plt.close()



def generateLabel(Dir,LabelMap,Curves,Val1,Val2):
    Direction = Dir
    Lab1 = LabelMap[Val1]
    if Val2 == r'2e\+00':
        Lab2 = '2e0'
    else:
        Lab2 = Val2
    return Direction+Curves+Lab1+Lab2

LabelMap = {'Grazing':'GrGrAc','Active':'AcAcAc','Sit':'AcSitSit'}
TypeCurves = ['Z(IC5)','Z(IC4)','MutualInv']
FStra = ['Grazing','Active','Sit']
bs = ['2e-02','2e-01',r'2e\+00']   

DirPlots = 'C:/Users/Carlos/Documents/Tesis-IGP/Data/Plots/'

if __name__=="__main__":
    #GeneratePlots(Dir,DirPlots,params,Types,p1,p2,p3,TypeDict,TypeCurves,sizePlot,plotParamsDict,Colors,LineStyles,yLabel,xLabel,LabelMap,FStra,bs)
    PlotInt(Dir,params,Types,p1,p2,p3,TypeDict,sizePlot,plotParamsDict,Colors,LineStyles,yLabel,xLabel)
    plt.savefig('MutualInvb2e-2.pdf')




