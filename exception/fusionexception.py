"""
Exceptions.
"""

class InputError(Exception):
    def __init__(self, message, code=400):
        self.message = "InputError: " +  message
        self.code = code

    def __str__(self):
        return self.message + " error code: %s." % self.code


class ClassException(Exception):
    def __init__(self, message, code):
        self.message = "ClassException: " +  message
        self.code = code

    def __str__(self):
        return self.message + " error code: %s." % self.code