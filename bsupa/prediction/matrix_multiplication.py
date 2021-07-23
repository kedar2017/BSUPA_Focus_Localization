from numpy import matrix
from numpy import linalg
import math
import numpy
distance = []
rssi = []

def apply_algo(cell, addr_list_algo, pos_list_algo, addr_list, rssi_list, eqn_val):
	def dst(rox):
		'''
		To get the distance based on the RSSI values
		'''
		#-18.49929610222167, -60.524649913705467
		#ans = (60.5246+rox)/(-18.499)
		ans = ((-1)*eqn_val[1] + rox)/(eqn_val[0])
		ans1 = math.pow(10,ans)
		distance.append(ans1)
     
	elem_x = []
	elem_y = []
	mean_x = 0.0
	mean_y = 0.0
	dist_mean = 0.0
	sq_mean_x = 0.0
	sq_mean_y = 0.0
	sq_mean_dist = 0.0
	dX = 0.0
	dY = 20.0
	count = 0
	elem_x = pos_list_algo[0]
	elem_y = pos_list_algo[1]
	print "LENGTH_ALGO", len(addr_list_algo)
	for i in range(len(addr_list_algo)):
		index = addr_list.index(addr_list_algo[i])
		rssi.append(rssi_list[index])
		dst(rssi[count])
		count = count + 1
	for k in range(count):
		mean_x = mean_x + float(elem_x[k]/count) 
		mean_y = mean_y + float(elem_y[k]/count)
		dist_mean = dist_mean + float(distance[k]/count)
	sq_mean_x = mean_x*mean_x
	sq_mean_y = mean_y*mean_y
	sq_mean_dist = dist_mean*dist_mean
	matrix_a = []
	matrix_b = []
	matrix_c = []
	for g in range(count):
	    val = sq_mean_dist-(distance[g]*distance[g])+(elem_x[g]*elem_x[g])-sq_mean_x+(elem_y[g]*elem_y[g])-sq_mean_y
	    matrix_b.append([val])	
	    matrix_c.append([1])
	    matrix_a.append([elem_x[g] - mean_x, elem_y[g] -mean_y])
	print "small_a", matrix_a
	print "small_b", matrix_b
	print "small_c", matrix_c
	print "distance", distance
	print "elem_x", elem_x
	print "elem_y", elem_y
	A_matrix = matrix(matrix_a)
	B_matrix = matrix(matrix_b)
	print A_matrix
	print B_matrix
	A_matrix_Transpose = A_matrix.T

	C_matrix = A_matrix_Transpose * A_matrix
	print "C_matrix", C_matrix
	D_matrix = C_matrix.I

	E_matrix = A_matrix_Transpose * B_matrix
	print "D_matrix", D_matrix
	print "E_matrix", E_matrix
	F_matrix = D_matrix * E_matrix
	print "X earlier", F_matrix.item(0)
	print "Y earlier", F_matrix.item(1)

	X = F_matrix.item(0)/2.0
	Y = F_matrix.item(1)/2.0
	def calc(h):
		measure = (elem_x[h] - X )* (elem_x[h] - X) + (elem_y[h] - Y) * (elem_y[h] - Y) 
		return math.sqrt(measure)
	algo2_A_list = []
	algo2_B_list = []
	while math.sqrt((dX*dX)+(dY*dY)) > 0.009:
	
		for a in range(count):
			fox = calc(a)
			algo2_A_list.append([(X - elem_x[a])/fox,(Y - elem_y[a])/fox])
			algo2_B_list.append([distance[a] - fox])
		algo2_matrix_A = matrix(algo2_A_list)
		algo2_matrix_B = matrix(algo2_B_list)
		algo2_matrix_A_Transpose = algo2_matrix_A.T
		algo2_matrix_C = algo2_matrix_A_Transpose * algo2_matrix_A
		algo2_matrix_D = algo2_matrix_C.I
		algo2_matrix_E = algo2_matrix_A_Transpose * algo2_matrix_B
		algo2_matrix_F = algo2_matrix_D * algo2_matrix_E
		dX = algo2_matrix_F.item(0)
		dY = algo2_matrix_F.item(1)
		X = X + dX
		Y = Y + dY
	print "dX finally",dX
	print "dY finally",dY
	print "X finally",X
	print "Y finally",Y
	return (X,Y)



	
