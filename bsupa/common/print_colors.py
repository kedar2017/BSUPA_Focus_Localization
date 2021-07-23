'''
    Copyright 2014 Focus Analytics Private Limited. All Rights Reserved.
    FOCUS ANALYTICS PROPRIETARY/CONFIDENTIAL. Use is subject to license terms.

    @version    0.1, 01-May-2015
    @author     Manoj G
    @email      manoj@getfocus.in
'''

class cprint:
    '''
    You know you are now mature in python programming when you start to write
    your own programs to replace/enhance basic functions in python
    This is for color printing which includes enable/disable functionality 
    (to mimick preprocessor #if)

    '''
    def __init__(self, global_enable=True):
        '''
        Global enable bit to enable printing, make it false and all prnt functions stop working
        Very helpful during debugging
        '''
        self.global_enable = global_enable
        self.enable = True

        ENDC = '\033[1;m'
        self.color_lookup = {'gr': '\033[1;30m%s'+ENDC,#Gray
                            'r': '\033[1;31m%s'+ENDC, #Red
                            'g': '\033[1;32m%s'+ENDC, #Green
                            'y': '\033[1;33m%s'+ENDC, #Yellow
                            'b': '\033[1;34m%s'+ENDC, #Blue
                            'm': '\033[1;35m%s'+ENDC, #Magenta
                            'c': '\033[1;36m%s'+ENDC, #Cyan
                            'R': '\033[1;38m%s'+ENDC, #Crimson
                            'w': '\033[1;37m%s'+ENDC, #
                            'hr': '\033[1;41m%s'+ENDC,#Highlight Red
                            'hR': '\033[1;48m%s'+ENDC,#Highlight Crimson
                            'hg': '\033[1;42m%s'+ENDC,#Highlight Green
                            'hc': '\033[1;46m%s'+ENDC,#Highlight Cyan
            }

    def prnt(self, to_print, mode='r' ):
        '''
        Takes string and prints in color
        Default mode is red
        '''
        if self.enable == True and self.global_enable == True:
            if isinstance(to_print, list) or isinstance(to_print, tuple):
                to_print = " \n-->  ".join( str(element) for element in to_print)
            string = str(to_print)
            print self.color_lookup[mode]%(string)

    def set(self):
        '''
        An idempotent function which sets enable bit
        '''
        self.enable = True

    def unset(self):
        '''
        Similar to set function, disables all prnt functions following this
        '''
        self.enable = False

if __name__ == '__main__':
    string  = 'wowowow'
    c = cprint(True)

    c.prnt("Wow this shit works", 'r')

    c.unset()
    c.prnt("This wont be printed", 'y')

    c.set()
    c.prnt("This will be printed","hr")

    c.prnt(("Print multiple objects", ('tuple1','tuple2'), ['list1', 'list2']), 'y')

    # Print everything
    print "------------------------------\nColor Test"
    for i in c.color_lookup.keys():
        print i,' ', c.color_lookup[i]
