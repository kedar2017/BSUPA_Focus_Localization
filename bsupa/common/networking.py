import time

def recvEnd(the_socket, End):
    """
    Seeks the data till it encounters End (end_of_data) bytes
    Helps remove the choppy tcp packets and return the entire packet
    """
    total_data=[];data=''
    while True:
            data=the_socket.recv(4096)
            if End in data:
                total_data.append(data[:data.find(End)])
                break
            total_data.append(data)
            if len(total_data)>1:
                #check if end_of_data was split
                last_pair=total_data[-2]+total_data[-1]
                if End in last_pair:
                    total_data[-2]=last_pair[:last_pair.find(End)]
                    total_data.pop()
                    break
    return ''.join(total_data)

### Functions for pipes ####
"""
For synchronization between mapper and supa
Logic:
    when n(mapping_packet) > 5 => mapper writes epoch value to pipe
    supa processes read pipe value everytime and compare with last_update epoch
        if the value is > 0    => supa reloads honeycomb objects
"""

def shouldReload(pipe_name, last_reload):
    """
    Used by supa
    pipe_name obtained from mapper_configurations
    last_reload is the last time the reload had occured
    """
    pipe_value = float(open(pipe_name).read())
    if pipe_value - last_reload > 0:
        return (True, pipe_value)
    else:
        return (False, pipe_value)

def writeTime(pt, pipe_name):
    """
    Small function which writes epoch time value to pipe
    """
    pipe_file = pt.open(pipe_name, 'w')
    pipe_file.write(str(time.time()))
    pipe_file.close()
