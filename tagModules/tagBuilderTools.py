from datetime import date as dt
from os import path
import re

MONTHS  = [
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
    'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
    ]

class Naming:
    def __init__(self):
        pass
    
    @classmethod
    def getDateCls(cls):
        month = ''
        for i in range(1,13):
            if dt.today().month == i:
                month = MONTHS[i-1]
        return str(dt.today().day), month, str(dt.today().year)
        
    @classmethod
    def createName(cls, root_, prefix_='', suffix_='', day_=False):
        day, month, year = cls.getDateCls()
        if prefix_ != '': prefix_ = prefix_+'_'
        if suffix_ != '': suffix_ = '_'+suffix_
        root_ = root_+'_'
        if day_ == False:
            return prefix_+root_+month+year+suffix_
        else:
            return prefix_+root_+day+month+year+suffix_
    
    def getDate(self):
        month = ''
        for i in range(1,13):
            if dt.today().month == i:
                month = MONTHS[i-1]
        return str(dt.today().day), month, str(dt.today().year)
    
    def createFileName(self, root_, prefix_='', suffix_='', day_=False):
        day, month, year = self.getDate()
        if prefix_ != '': prefix_ = prefix_+'_'
        if suffix_ != '': suffix_ = '_'+suffix_
        root_ = root_+'_'
        if day_ == False:
            return prefix_+root_+month+year+suffix_
        else:
            return prefix_+root_+day+month+year+suffix_
    
class MathTag:
    def __init__(self):
        pass
    
class stringMethods:
    def __init__(self):
        pass
    
    @classmethod
    def subStrings(cls, regexPattern, string):
        try:
            return re.findall(regexPattern, string)
        except:
            return []
        
    @classmethod
    def extractCode(cls, regexPattern, string):
        try:
            return re.findall(regexPattern, string)[0]
        except:
            return string
        
if __name__ == '__main__':
    sObj = stringMethods()