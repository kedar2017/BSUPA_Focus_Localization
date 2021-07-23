import logging
import inspect
import operator

from decorators   import static_variable

def line_trace():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno

def getLogging(instance_type, logging_filename, instance_name):
    """
    Returns a logging instance
    """
    logger = logging.getLogger(instance_type)
    hdlr = logging.FileHandler('./'+logging_filename)
    formatter = logging.Formatter('%(asctime)s %(instance_name)s %(levelname)s%(message)s ')
    hdlr.setFormatter(formatter)
    logger.addHandler(hdlr)
    logger.setLevel(logging.INFO)
    logger = logging.LoggerAdapter(logger, instance_name)
    return logger

def getLoggers(logging_instance, from_value="%s"):
    """
    Takes logging instance and returns 3 functions
    logInfo, logWarn and logErr
    """
    @static_variable(logger=logging_instance, _from=from_value)
    def logInfo(info, _from="%s", ):
        """
        It MUST a static_variable decoractor in supa/common/ to set logger instance
        Prints as well as logs
        """
        print info
        logInfo.logger.info(info)

    @static_variable(logger=logging_instance, _from=from_value)
    def logErr(err, _from="%s", ):
        """
        It MUST a static_variable decoractor in supa/common/ to set logger instance
        Prints as well as logs
        """
        print err
        logErr.logger.error(logErr._from%err)

    @static_variable(logger=logging_instance, _from=from_value)
    def logWarn(warning, _from="", ):
        """
        It MUST a static_variable decoractor in supa/common/ to set logger instance
        Prints as well as logs
        """
        print warning
        logWarn.logger.warn(logWarn._from%warning)

    return logInfo, logWarn, logErr

def basicLog(file_name, to_write):
    """
    Used when the log information needs to be processed
    """
    file_handler = open(file_name, 'a')
    file_handler.write(to_write+"\n")
    file_handler.close()

def logDeltaTime(dT):
    '''
    logs delta time into a logdT file
    '''
    lFile = open("logdT.log",'a')
    lFile.write(dT+"\n")
    lFile.close()

def isTrue(list_truth_values):
    """
    Returns True if all values in list_truth_values are True
    Used by test cases
    """
    if list_truth_values == []:
        return False
    else:
        return reduce(operator.and_, list_truth_values, True)
