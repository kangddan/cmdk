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
            self._omMatrix = self.matrixtoVectors(v1._omMatrix)
        elif isinstance(v1, (om2.MMatrix, list, tuple)):
            self._omMatrix = self.matrixtoVectors(v1)
        else:
            self._omMatrix = ((*v1, 0), (*v2, 0), (*v3, 0), (*off, 1))
    
    def __repr__(self):
        return 'KMatrix(v1: {}; v2: {}; v3: {}; off: {})'.format(
                self.v1, self.v2, self.v3, self.off)
    
    @property
    def _omMatrix(self) -> om2.MMatrix:
        return self.__omMatrix

    @_omMatrix.setter
    def _omMatrix(self, value):
        self.__omMatrix = om2.MMatrix((value[0], value[1], value[2], value[3]))
        
    @staticmethod
    def matrixtoVectors(matrix: om2.MMatrix) -> tuple:
        _matrix = [*matrix]
        v1      = _matrix[0:4]
        v2      = _matrix[4:8]
        v3      = _matrix[8:12]
        off     = _matrix[12:16]
        return v1, v2, v3, off
        
    @property
    def v1(self) -> KVector:
        return KVector(
        self._omMatrix[0], self._omMatrix[1], self._omMatrix[2])
        
    @v1.setter
    def v1(self, vector: KVector):
        self._omMatrix[0], self._omMatrix[1], self._omMatrix[2] = vector
        
    @property
    def v2(self) -> KVector:
        return KVector(
        self._omMatrix[4], self._omMatrix[5], self._omMatrix[6])
        
    @v2.setter
    def v2(self, vector: KVector):
        self._omMatrix[4], self._omMatrix[5], self._omMatrix[6] = vector
        
    @property
    def v3(self) -> KVector:
        return KVector(
        self._omMatrix[8], self._omMatrix[9], self._omMatrix[10])
    
    @v3.setter
    def v3(self, vector: KVector):
        self._omMatrix[8], self._omMatrix[9], self._omMatrix[10] = vector
    
    @property
    def off(self) -> KVector:
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
        
    def mulVectorlR(self, vector: KVector) -> KVector:
        '''
        Multiply the vector by the matrix, this does not include any translation
        '''
        return KVector(vector._omVector * self._omMatrix)
    
    def mulVectorlL(self, vector: KVector) -> KVector:
        '''
        Multiply the vector by the matrix, this does not include any translation
        '''
        return KVector(self._omMatrix * vector._omVector)
    
    def inverse(self):
        '''
        Inverts the matrix
        '''
        return KMatrix(self._omMatrix.inverse())
        
    def __iter__(self):
        return iter(self._omMatrix)
    
    @attrUtils.checkNumberType
    def __getitem__(self, index) -> float:
        return self._omMatrix[index]
    
    @attrUtils.checkNumberType        
    def __setitem__(self, index, value):
        self._omMatrix[index] = value
    
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
        
    def __mul__(self, other):
        if isinstance(other, self.__class__):
            return KMatrix(self._omMatrix * other._omMatrix)
        elif isinstance(other, KVector):
            return self.mul(other)
        elif isinstance(other, (int, float, complex)):
            return KMatrix(self._omMatrix * other)
        else:
            return NotImplemented
            
    def __rmul__(self, other):
        return self.__mul__(other)
        
    def __imul__(self, other):
        if isinstance(other, self.__class__):
            self._omMatrix = self.matrixtoVectors(self._omMatrix * other._omMatrix)
        elif isinstance(other, KVector):
            return self.mul(other)
        elif isinstance(other, (int, float, complex)):
            self._omMatrix = self.matrixtoVectors(self._omMatrix * other)
        else:
            return NotImplemented
        return self
    
    @attrUtils.checkNumberType
    def __truediv__(self, other) -> 'KMatrix':
        return KMatrix(self.v1 / other, self.v2 / other, self.v3 / other, self.off / other)
        
    def __invert__(self) -> 'KMatrix':
        return KMatrix(self.inverse())
        
    def __mod__(self, other) -> KVector:
        if isinstance(other, KVector):
            return self.mulVectorlL(other)
    
    def __rmod__(self, other) -> KVector:
        if isinstance(other, KVector):
            return self.mulVectorlR(other)
        else:
            return NotImplemented
          
    def __imod__(self, other):
        if isinstance(other, KVector):
            return self.mulVectorlR(other)
        else:
            return NotImplemented
        return self
   
    
    @attrUtils.checkClass
    def __eq__(self, other) -> bool:
        return self._omMatrix == other._omMatrix
        
    @attrUtils.checkClass
    def __ne__(self, other) -> bool:
        return self._omMatrix != other._omMatrix
        
            

if __name__ == '__main__':
    
    mm = KMatrix()
    mm[4] = 16
    mm.v2

    # v1 = KVector(3, 2, 6)
    # m1 = KMatrix(KVector(5, 6, 5), KVector(5, 8, 5), KVector(0, 4, 2), KVector(7, 4, 2))
    # m2 = KMatrix(KVector(2, 4, 1), KVector(0, 4, 2), KVector(2, 6, 8), KVector(2, 4, 4))
    # [*m2]
    # m3 = KMatrix(m1)

    
    # m1 == m3
    

    #m1._omMatrix


    

    
    

    