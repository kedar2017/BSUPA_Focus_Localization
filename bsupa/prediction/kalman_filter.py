
import numpy
import statistics
from numpy import matrix
from numpy import linalg
import math

def kalman(initial_value, train_pos, train_dict, live_dict):
    ############################## Now apply algo
    num_dev   = len(live_dict)
    P_pos_cov = 0.2 * genMatrix(num_dev)
    P_rssi_cov= 81  * genMatrix(num_dev)
    P_last    = 0.2 * genMatrix(3)
    p_x_x_k   = 0.0 * genMatrix(num_dev)
    p_x_y_k   = 0.0 * genMatrix(num_dev)
    p_y_y_k   = 0.0 * genMatrix(num_dev)
    x_last    = matrix([[initial_value[0]],[initial_value[1]],[0.0]])
    RSSI_var  = 0.0 * genMatrix(num_dev)
    RSSI_pres = RSSI_var[0].T
    Pos_var   = 0.0 * genMatrix(num_dev)
    Pos_val_pres= Pos_var[0].T
    val_beta  = []
    beta      = []
    scan  = len(train_pos)
    num_iter = 0



    while num_iter < 20:
        num_iter = num_iter + 1
        x_temp   = x_last
        P_temp   = P_last
        RSSI_train_list = []
        for a in range(scan):
            val_beta.append(normpdf(matrix([[train_pos[a][0]],[train_pos[a][1]],[0.0]]),x_temp,P_temp))

        for b in range(scan):
            beta.append(val_beta[b]/sum(val_beta))

        for c in range(scan):
            for addr in train_dict[c].keys():
                RSSI_train_list.append([train_dict[c][addr]])
            RSSI_train_mat = matrix(RSSI_train_list)
            RSSI_pres = RSSI_pres + beta[c] * RSSI_train_mat
            Pos_val_pres= Pos_val_pres + beta[c] * matrix([[train_pos[c][0]],[train_pos[c][1]],[0.0]])
            RSSI_train_list = []

        for d in range(scan):
            for addr in train_dict[d].keys():
                RSSI_train_list.append([train_dict[d][addr]])
            RSSI_train_mat = matrix(RSSI_train_list)
            p_x_x_k = p_x_x_k + beta[d]*(P_pos_cov + ((matrix([[train_pos[d][0]],[train_pos[d][1]],[0.0]])) - Pos_val_pres) * ((matrix([[train_pos[d][0]],[train_pos[d][1]],[0.0]]) - Pos_val_pres).T))
            p_x_y_k = p_x_y_k + beta[d]*((matrix([[train_pos[d][0]],[train_pos[d][1]],[0.0]])) - Pos_val_pres) * ((RSSI_train_mat - RSSI_pres).T)
            p_y_y_k = p_y_y_k + beta[d]*((RSSI_train_mat - RSSI_pres) * (RSSI_train_mat - RSSI_pres).T)
            RSSI_train_list = []

        P_last = p_x_x_k - (p_x_y_k * (p_y_y_k).I * (p_x_y_k).T)
        for addr in train_dict[0].keys():
            RSSI_live_list.append([live_dict[addr]])
        RSSI_live = matrix(RSSI_live_list)

        x_last = x_temp + p_x_y_k * (p_y_y_k).I * (RSSI_live - RSSI_pres)
        RSSI_pres= RSSI_var[0].T
        Pos_val_pres= Pos_var[0].T
        p_x_x_k   = 0.0 * genMatrix(num_dev)
        p_x_y_k   = 0.0 * genMatrix(num_dev)
        p_y_y_k   = 0.0 * genMatrix(num_dev)

    print "Finally", x_last

def genMatrix(num):
    ident = matrix(numpy.identity(num))
    return ident

def normpdf(pos, x, P):
    up = -0.5 * ((pos - x).T) * P.I * (pos - x)
    ans= math.exp(up)
    z  = 6.28 * P
    denom = linalg.det(z)
    denom = math.sqrt(denom)
    return ans/denom

