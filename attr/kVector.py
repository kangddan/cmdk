# -*- coding: utf-8 -*-
import maya.cmds as cmds
import maya.api.OpenMaya as om2
import cmdk.attr.attrUtils as attrUtils


class KVector(object):
    
    def __init__(self, x: float = 0, 
                       y: float = 0, 
                       z: float = 0):
                        
        if isinstance(x, self.__class__):
            self._omVector = x._omVector
        elif isinstance(x, om2.MVector):
            self._omVector = x
        else:
            self._omVector = (x, y, z)
    
    def __repr__(self):
        return 'KVector({}, {}, {})'.format(self.x, self.y, self.z)
        
    def __str__(self):
        return '({}, {}, {})'.format(*self)
        
    @property
    def _omVector(self) -> om2.MVector:
        return self.__omVector
        
    @_omVector.setter
    @attrUtils.checkVectorType
    def _omVector(self, value):
        self.__omVector = om2.MVector(*value)
        
    @property
    def _omPoint(self) -> om2.MPoint:
        return om2.MPoint(self._omVector)
        
    @property
    def x(self) -> float:
        return self._omVector.x
        
    @x.setter
    @attrUtils.checkNumberType
    def x(self, value):
        self._omVector.x = value
        
    @property
    def y(self) -> float:
        return self._omVector.y
        
    @y.setter
    @attrUtils.checkNumberType
    def y(self, value):
        self._omVector.y = value
        
    @property
    def z(self) -> float:
        return self._omVector.z
        
    @z.setter
    @attrUtils.checkNumberType
    def z(self, value):
        self._omVector.z = value
        
    # -------------------------------------------
    @property
    def getHashCode(self) -> int:
        '''
        Returns the hash code of the vector used for hash maps and comparisons
        '''
        hashX = int(self.x * 738566456)
        hashY = int(self.y * 193496634)
        hashZ = int(self.z * 834927916)

        return hashX ^ hashY ^ hashZ
    
    @attrUtils.checkClass
    def isEqual(self, other, epsilon=1e-10) -> bool:
        '''
        Tests component-wise if the difference is no bigger than epsilon
        '''
        return self._omVector.isEquivalent(other._omVector, epsilon)
        
    def isZero(self, epsilon=1e-10) -> bool:
        '''
        Checks if each component is zero
        '''
        return all(abs(n) < epsilon for n in self)
            
    def setZero(self) -> 'self':
        '''
        Sets all components to zero
        '''
        self.x, self.y, self.z = 0, 0, 0
        return self
    
    @property    
    def getAverage(self) -> float:
        '''
        Calculates the average value of x, y and z
        '''
        return (self.x + self.y + self.z) / 3.0
        
    @property
    def getSum(self) -> float:
        '''
        Calculates the sum of x, y and z
        '''
        return self.x + self.y + self.z

    @attrUtils.checkClass
    def setMin(self, other) -> 'self':
        '''
        Set the minimum of each component
        '''
        self.x = min(self.x, other.x)
        self.y = min(self.y, other.y)
        self.z = min(self.z, other.z)
        return self
        
    @attrUtils.checkClass
    def setMax(self, other) -> 'self':
        '''
        Set the maximum of each component
        '''
        self.x = max(self.x, other.x)
        self.y = max(self.y, other.y)
        self.z = max(self.z, other.z)
        return self
    
    @attrUtils.checkClass
    def min(self, other) -> 'KVector':
        '''
        Calculates the minimum of each component
        '''
        return KVector(
        x=min(self.x, other.x),
        y=min(self.y, other.y),
        z=min(self.z, other.z))
    
    @attrUtils.checkClass
    def max(self, other) -> 'KVector':
        '''
        Calculates the maximum of each component
        '''
        return KVector(
        x=max(self.x, other.x),
        y=max(self.y, other.y),
        z=max(self.z, other.z))
    
    @property
    def clamp01(self) -> 'KVector':
        '''
        Returns a vector that is clamped to the range [0.0 .. 1.0]
        '''
        clampedX = max(0.0, min(self.x, 1.0))
        clampedY = max(0.0, min(self.y, 1.0))
        clampedZ = max(0.0, min(self.z, 1.0))
        return KVector(clampedX, clampedY, clampedZ)
        
    @property    
    def getLength(self) -> float:
        '''
        Calculates the length of the vector
        '''
        return self._omVector.length()
        
    @property
    def getSquaredLength(self) -> float:
        '''
        Returns the squared length of the vector
        '''
        return pow(self.getLength, 2)
        

    def getNormalized(self) -> 'KVector':
        '''
        Calculates the normalized vector, so that getLength returns 1
        '''
        nv = self._omVector.normal()
        return KVector(nv.x, nv.y, nv.z)
        
    def normalize(self) -> 'self':
        '''
        Normalizes the vector, so that getLength returns 1
        '''
        self._omVector.normalize()
        return self
        
        
    @property
    def getMin(self) -> float:
        '''
        Returns the minimum of x, y and z
        '''
        return min(self.x, self.y, self.z)
    
    @property
    def getMax(self) -> float:
        '''
        Returns the maximum of x, y and z
        '''
        return max(self.x, self.y, self.z)
        
    def getRightRotated(self, rots) -> 'KVector':
        '''
        Returns a vector where the components have been rotated to the right (in the usual (x, y, z)-representation)
        E.g., with a value of 1 for rots, the result will be (z, x, y)
        
        rots = 1; x, y, z = z, x, y
        rots = 2; x, y, z = y, z, x
        rots = 3; x, y, z = x, y, z (no change)
        '''
        coords = [self.x, self.y, self.z]
        rots = rots % 3
        rotatedCoords = coords[-rots:] + coords[:-rots]
        return KVector(*rotatedCoords)
        
    @attrUtils.checkClass    
    def dot(self, other) -> float:
        '''
        Calculates the dot product of the self and other
        '''
        return self._omVector * other._omVector
        
    @property
    def abs(self):
        '''
        Returns the vector with absolute value for each entry
        '''
        return KVector(abs(self.x), abs(self.y), abs(self.z))
        
    @attrUtils.checkClass       
    def getAngle(self, other) -> float:
        '''
        Calculates angle (in radians) between self and other
        '''
        return self._omVector.angle(other._omVector)
        
    @attrUtils.checkClass       
    def cross(self, other) -> 'KVector':
        '''
        Calculates the cross product of the self and other
        '''
        crossProduct = self._omVector ^ other._omVector
        return KVector(crossProduct.x, crossProduct.y, crossProduct.z)
        
    @attrUtils.checkClass  
    def getDistance(self, other) -> float:
        '''
        Retrieve the distance between two vectors
        '''
        return self._omPoint.distanceTo(other._omPoint)
        
    @staticmethod
    def GetDistance(v1, v2) -> float:
        '''
        Retrieve the distance between two vectors
        '''
        return v1._omPoint.distanceTo(v2._omPoint)
    
    # -----------------------------------------------------
    def __iter__(self):
        yield self.x
        yield self.y
        yield self.z
    
    @attrUtils.checkNumberType     
    def __getitem__(self, index) -> float:
        '''
        Retrieves the value of the x, y or z component of the vector
        '''
        return self._omVector[index]
    
    @attrUtils.checkNumberType        
    def __setitem__(self, index, value):
        '''
        Assigns a value to the x, y or z component of the vector
        '''
        self._omVector[index] = value
            
    def __add__(self, other) -> 'KVector':
        '''
        Adds an operand to the vector
        '''
        if isinstance(other, self.__class__):
            addVec = self._omVector + other._omVector
            return KVector(addVec.x, addVec.y, addVec.z)
        elif isinstance(other, (int, float, complex)):
            return KVector(self.x + other, self.y + other, self.z + other)
        else:
            return NotImplemented
            
    def __radd__(self, other) -> 'KVector':
        '''
        Adds the vector to an operand
        '''
        return self.__add__(other)
    
    def __iadd__(self, other):
        if isinstance(other, self.__class__):
            self._omVector += other._omVector
        elif isinstance(other, (int, float)):
            self.x += other
            self.y += other
            self.z += other
        else:
            return NotImplemented
        return self
    
    def __isub__(self, other):
        if isinstance(other, self.__class__):
            self._omVector -= other._omVector
        elif isinstance(other, (int, float)):
            self.x -= other
            self.y -= other
            self.z -= other
        else:
            return NotImplemented
        return self
        
        
    def __sub__(self, other) -> 'KVector':
        '''
        Subtracts an operand from the vector
        '''
        if isinstance(other, self.__class__):
            subVec = self._omVector - other._omVector
            return KVector(subVec.x, subVec.y, subVec.z)
        elif isinstance(other, (int, float, complex)):
            return KVector(self.x - other, self.y - other, self.z - other)
        else:
            return NotImplemented
    
    def __rsub__(self, other) -> 'KVector':
        '''
        Subtracts the vector from an operand
        '''
        if isinstance(other, self.__class__):
            return other.__sub__(self)
        elif isinstance(other, (int, float)):
            return KVector(other - self.x, other - self.y, other - self.z)
        else:
            return NotImplemented
    
    @attrUtils.checkClass        
    def __ne__(self, other) -> bool:
        return self._omVector != other._omVector
        
    @attrUtils.checkClass        
    def __eq__(self, other) -> bool:
        return self._omVector == other._omVector
        
    def __invert__(self) -> 'KVector':
        '''
        Returns the inverse of the vector
        '''
        return KVector(-self.x, -self.y, -self.z)
        
    def __neg__(self) -> 'KVector':
        return self.__invert__()
        
    def __abs__(self) -> 'KVector':
        return self.abs
    
    @attrUtils.checkNumberType
    def __truediv__(self, other):
        return KVector(self.x / other, self.y / other, self.z / other)
        
    @attrUtils.checkNumberType
    def __itruediv__ (self, other):
        self._omVector /= other
        return self

            
    @attrUtils.checkNumberType
    def __floordiv__(self, other):
        return KVector(self.x // other, self.y // other, self.z // other)
    
    @attrUtils.checkNumberType
    def __ifloordiv__(self, other):
        self.x //= other
        self.y //= other
        self.z //= other
        return self
        
    def __mul__(self, other):
        from cmdk.attr.kMatrix import KMatrix
        
        if isinstance(other, (int, float, complex)):
            return KVector(self.x*other, self.z*other, self.y*other)
        elif isinstance(other, self.__class__):
            return self.dot(other)
        elif isinstance(other, KMatrix):
            #matrix * point
            pass
        else:
            return NotImplemented
            
    def __rmul__(self, other):
        from cmdk.attr.kMatrix import KMatrix
        
        if isinstance(other, (int, float, complex)):
            return KVector(self.x*other, self.z*other, self.y*other)
        elif isinstance(other, KMatrix):
            #matrix * point
            pass
        else:
            return NotImplemented
            
    def __imul__(self, other):
        from cmdk.attr.kMatrix import KMatrix
        
        if isinstance(other, (int, float, complex)):
            self._omVector *= other
        elif isinstance(other, self.__class__):
            pass  # dot
        elif isinstance(other, KMatrix):
            pass
        return self
        
    @attrUtils.checkClass
    def __mod__(self, other):
        '''
        Calculates the cross product of the vector and an operand
        '''
        return self.cross(other)
        
    def __xor__(self, other):
        '''
        Calculates an alternative product operation of the vector and a left-side operand

        If other is a vector, calculates the component-wise product of the vectors
        If other is a matrix, the vector is transformed by it, excluding translations
        '''
        if isinstance(other, self.__class__):
            return KVector(self.x*other.x, self.y*other.y, self.z*other.z)
        elif isinstance(other, KMatrix):
            #matrix * vector
            pass
        else:
            return NotImplemented
            
    def __rxor__(self, other):
        return NotImplemented
        
 
    
if __name__ == '__main__':
    v = KVector(3, 2, 6)
    v2 = KVector(5, 8, 3)
    print(v)
    
    v3 = KVector(v2)
    
    vv = om2.MVector(8, 9, 6)
    vv3 = KVector(vv)
    vv3.normalize()
    vv3._omVector





