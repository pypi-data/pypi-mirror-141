from marshmallow import Schema, fields, INCLUDE, ValidationError
from apiflask.fields import Integer, String, DateTime
from ac4y_object.ac4y_object import Ac4yObject

class Ac4yProcessResultSchema(Schema):
    code = Integer()
    message = String()
    description = String()

class Ac4yProcessResult(Ac4yObject):

    def getSuccessProcessResult(self):
        processResult=Ac4yProcessResult()
        processResult.code=1
        processResult.message = "success"
        return processResult

    def getErrorProcessResult(self, description):
        processResult=Ac4yProcessResult()
        processResult.code=-1
        processResult.message = "error"
        processResult.description = description
        return processResult

    def itWasSuccessful(self):
        return self.code ==1;

    def itWasFailed(self):
        return self.code ==-1;

    def itWasNothingToDo(self):
        return self.code ==0;