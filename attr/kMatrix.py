# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.api.OpenMaya as om2
import cmdk.attr.attrUtils as attrUtils
from cmdk.attr.kVector import KVector

class KMatrix(object):

    def __init__(self, v1: KVector = KVector(1, 0, 0), 
                       v2: KVector = KVector(0, 1, 0), 
                       v3: KVector = KVector(0, 0, 1), 
                      off: KVector = KVector(0, 0, 0)):
        if isinstance(v1, self.__class__):
            #self._omMatrix = (v1.v1, v1.v2, v1.v3, v1.off)
            self._omMatrix = self.matrixtoVectors(v1._omMatrix)
        elif isinstance(v1, om2.MMatrix):
            self._omMatrix = self.matrixtoVectors(v1)
        else:
            # self._omMatrix = (v1, v2, v3, off)
            self._omMatrix = ((*v1, 0), (*v2, 0), (*v3, 0), (*off, 1))
    
    def __repr__(self):
        return 'KMatrix(v1: {}; v2: {}; v3: {}; off: {})'.format(
                self.v1, self.v2, self.v3, self.off)
    
    @property
    def _omMatrix(self):
        return self.__omMatrix

    @_omMatrix.setter
    def _omMatrix(self, value):
        self.__omMatrix = om2.MMatrix((value[0], 
                                       value[1], 
                                       value[2], 
                                       value[3]))
        # self.__omMatrix = om2.MMatrix(((*value[0], 0), 
        #                                (*value[1], 0), 
        #                                (*value[2], 0), 
        #                                (*value[3], 1)))
        
    @staticmethod
    def matrixtoVectors(matrix: om2.MMatrix):
        v1  = (matrix[0],  matrix[1],  matrix[2], matrix[3])
        v2  = (matrix[4],  matrix[5],  matrix[6], matrix[7])
        v3  = (matrix[8],  matrix[9],  matrix[10], matrix[11])
        off = (matrix[12], matrix[13], matrix[14], matrix[15])
        return v1, v2, v3, off
        
    @property
    def v1(self):
        return KVector(
        self._omMatrix[0], self._omMatrix[1], self._omMatrix[2])
        
    @v1.setter
    def v1(self, vector: KVector):
        self._omMatrix[0], self._omMatrix[1], self._omMatrix[2] = vector
        
    @property
    def v2(self):
        return KVector(
        self._omMatrix[4], self._omMatrix[5], self._omMatrix[6])
        
    @v2.setter
    def v2(self, vector: KVector):
        self._omMatrix[4], self._omMatrix[5], self._omMatrix[6] = vector
        
    @property
    def v3(self):
        return KVector(
        self._omMatrix[8], self._omMatrix[9], self._omMatrix[10])
    
    @v3.setter
    def v3(self, vector: KVector):
        self._omMatrix[8], self._omMatrix[9], self._omMatrix[10] = vector
    
    @property
    def off(self):
        return KVector(
        self._omMatrix[12], self._omMatrix[13], self._omMatrix[14])
    
    @off.setter
    def off(self, vector: KVector):
        self._omMatrix[12], self._omMatrix[13], self._omMatrix[14] = vector
    
    def normalize(self) -> 'self':
        self.v1  = self.v1.getNormalized()
        self.v2  = self.v2.getNormalized()
        self.v3  = self.v3.getNormalized()
        self.off = self.off.getNormalized()
        
    def getNormalized(self) -> 'KMatrix':
        return KMatrix(self.v1.getNormalized(),
                       self.v2.getNormalized(),
                       self.v3.getNormalized(),
                       self.off.getNormalized())
    
    def scale(self):
        pass
        
    @property                   
    def getScale(self) -> KVector:
        return KVector(self.v1.getLength, self.v2.getLength, self.v3.getLength)
        
    def getTensorMatrix(self) -> 'KMatrix':
        '''
        Returns the matrix tensor
        '''
        return KMatrix(self.v1, self.v2, self.v3, self.off.setZero())
        
    def mul(self, vector: KVector) -> KVector:
        '''
        Multiply the vector by the matrix, this includes any translation in the matrix
        '''
        return KVector(om2.MVector(vector._omPoint * self._omMatrix))
        
    def mulV(self, vector: KVector) -> KVector:
        '''
        Multiply the vector by the matrix, this does not include any translation
        '''
        return KVector(vector._omVector * self._omMatrix)
    
    @attrUtils.checkClass    
    def __add__(self, other) -> 'KMatrix':
        addM = self._omMatrix + other._omMatrix
        return KMatrix(addM)
        
    @attrUtils.checkClass 
    def __radd__(self, other) -> 'KMatrix':
        return self.__add__(other)
        
    @attrUtils.checkClass    
    def __iadd__(self, other) -> 'KMatrix':
        self._omMatrix = self.matrixtoVectors(self._omMatrix + other._omMatrix)
        return self
        
    @attrUtils.checkClass     
    def __sub__(self, other) -> 'KMatrix':
        subM = self._omMatrix - other._omMatrix
        return KMatrix(subM)
    
    @attrUtils.checkClass 
    def __rsub__(self, other) -> 'KMatrix':
        return self.__sub__(other)
    
    @attrUtils.checkClass 
    def __isub__(self, other) -> 'KMatrix':
        self._omMatrix = self.matrixtoVectors(self._omMatrix - other._omMatrix)
        return self

if __name__ == '__main__':
    
    m = KMatrix(KVector(5, 6, 5), KVector(5, 8, 5), KVector(0, 4, 2), KVector(7, 12, 15))
    m._omMatrix
    
    m2 = KMatrix(KVector(5, 6, 5), KVector(5, 8, 5), KVector(0, 4, 2), KVector(7, 12, 15))
    m2 += m
    m2 -= m
    m2._omMatrix

    m3 = KMatrix(m2)
    m3._omMatrix
    m1 = KMatrix()
    #v = KVector(3, 2, 6)
    #m = KMatrix(KVector(5, 6, 5), KVector(5, 8, 5), KVector(0, 4, 2), KVector(7, 12, 15))
    #m.mul(v)
    
    #m.mulV(v)

    

    
    

    