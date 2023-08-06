'''
Helper functions for create_ascii.

'''

from typing import Union

def map(val:float, from_range: Union[list,tuple], to_range: Union[list,tuple] ) -> float:
    '''
    Returns the mapping of a real number from the first to the second range.

    Parameters:
        val         : The value to be mapped
        from_range  : List or tuple containing min and max values of range 
        to_range    : List or tuple containing min and max values of range

    Example:
        map(1,[0,2],[0,10])  #returns 5.0

    Reference:
        https://rosettacode.org/wiki/Map_range#Python
    '''

    def validate(variable):
        '''
         - Inner function to determine if variable is a tuple/list of size 2 and it's contents are numbers
        '''
        if(type(variable) in [list,tuple]):
            if len(variable) != 2:
                raise Exception("Expected list or tuple of size 2.")
            else:
                if not all(isinstance(x, (int,float)) for x in variable) or not isinstance(val,(int,float)):
                     raise Exception("Unexpected non-numeric value in input data.")
        else:
            raise Exception("Expected list or tuple of size 2. Received {} instead.".format(type(variable)))

    validate(from_range)
    validate(to_range)

    (x1,x2),(y1,y2) = from_range , to_range
    return y1 + (val-x1)*(y2-y1)/(x2-x1)  