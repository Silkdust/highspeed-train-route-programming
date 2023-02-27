import gurobipy as gp
from gurobipy import GRB
import numpy as np
import xlrd
import argparse

class Route:
    def __init__(self, name, o, d, dist, t, e_idx, p_idx):
        self.name = name
        self.o = o
        self.d = d
        self.dist = dist
        self.t = t
        self.eidx = e_idx
        self.pidx = p_idx
    def getAttribute(self):
        return self.dist, self.t, self.eidx, self.pidx

'''
def f_r(R_list, i, j):
    for rt in R_list:
        print(rt.o,rt.d)
        if rt.oid==i:
            if rt.did==j:
                return(rt)
'''

class RailwayOptimizer:
    def __init__(self, filepath = "./Project_.xls", opencity = "北京", destination = "桂林"):
        '''
        初始化最优函数类
        Args:
            filepath: 数据路径，默认为./Project_.xls
            opencity: 起点城市，默认为北京
            destination: 终点城市，默认为桂林
        '''
        self.file_path = filepath
        # Open and Destination Attributes
        self.opencity = opencity
        self.destination = destination
        # Cities Attributes
        self.cities = None
        self.cities_num = None
        # Routes Information Attributes
        self.num_routes = None
        self.routes = None
        self.dists = None
        self.Ts = None
        self.eidxs = None
        self.pidxs = None
        # Transline Attributes
        self.gama_list = None
        self.h_list = None
        # Initiate all attributes above
        self.__init_data()
    
    def __init_data(self):
        # open file
        my_file = xlrd.open_workbook(self.file_path)
        table_cities = my_file.sheets()[0]
        table_routes = my_file.sheets()[1]
        table_transline = my_file.sheets()[2]

        # import routes data
        self.num_routes = table_routes.nrows-1
        self.r_dict = {}
        for i in range(self.num_routes):
            d_list = table_routes.row_values(i + 1)
            rt = Route(*d_list)
            self.r_dict[(rt.o, rt.d)] = rt.getAttribute()
        
        # import cities data
        self.cities = table_cities.col_values(1)[1:] 
        #self.cities_num = table_cities.nrows-1

        # import trans-line-limits data
        self.h_list = []
        self.gama_list = []

        rest_num = table_transline.nrows-1
        for i in range(rest_num):
            d_list = table_transline.row_values(i+1)
            if d_list[-1] == 1:
                self.gama_list.append(tuple(d_list[1:4]))
            elif d_list[-2] == 1:
                self.h_list.append(tuple(d_list[1:4]))

        self.gama_list = gp.tuplelist(self.gama_list)
        self.h_list = gp.tuplelist(self.h_list)

        # prepare tupledict
        self.routes, self.dists, self.Ts, self.eidxs, self.pidxs = gp.multidict(self.r_dict)
    
    def solve(self, obj_coef = (0.32, 0.4, 0.15, -0.13), print_solution = True):
        '''
        求解问题
        Args:
            obj_coef: 目标函数的加权参数，默认为(0.32, 0.4, 0.15, -0,13)
            print_solution: 是否打印结果, 默认为True
        
        Returns:
            最优路线里程、运行时间、区段影响指数、区间客流指数
        '''
        # Model
        self.m = gp.Model("BestRoute")

        # Create Decision Variables
        self.if_rt = self.m.addVars(self.routes, vtype = GRB.BINARY, name = 'routes')
        self.if_x = self.m.addVars(self.h_list, vtype = GRB.BINARY, name = 'translines')

        # Obj Func
        lambda1, lambda2, lambda3, lambda4 = obj_coef

        z_1 = self.if_rt.prod(self.dists)
        z_2 = self.if_rt.prod(self.Ts) + 2 * (self.if_rt.sum() - 2) + 18 * self.if_x.sum() 
        z_3 = self.if_rt.prod(self.eidxs)
        z_4 = self.if_rt.prod(self.pidxs)

        X1 = 100 * (z_1 - 85) / (4656 - 85)
        X2 = 100 * (z_2 - 29) / (1561 - 29)
        X3 = z_3 / 530.21 * 100
        X4 = z_4 / 161.15 * 100

        self.m.setObjective(lambda1*X1 + lambda2*X2 + lambda3*X3 + lambda4*X4, GRB.MINIMIZE)

        # Constraints
        # C1:webstream basic
        cities_nood = [i for i in self.cities if i != self.opencity and i != self.destination]
        self.m.addConstrs(self.if_rt.sum('*', i) == self.if_rt.sum(i, '*') for i in cities_nood)
        self.m.addConstr(self.if_rt.sum(self.opencity, '*') == 1)
        self.m.addConstr(self.if_rt.sum('*', self.destination) == 1)
        self.m.addConstr(self.if_rt.sum('*', self.opencity) == 0)
        self.m.addConstr(self.if_rt.sum(self.destination, '*') == 0)

        # C2:no loop
        self.m.addConstrs(self.if_rt[i, j] + self.if_rt[j, i] <= 1 for i, j in self.routes)
        self.m.addConstrs(self.if_rt.sum('*', i) <= 1 for i in cities_nood)
        self.m.addConstrs(self.if_rt.sum(i, '*') <= 1 for i in cities_nood)

        # C3:trans-line

        #    i:cannot trans-line
        self.m.addConstrs(self.if_rt[j, i] + self.if_rt[i, k] <= 1 for i, j, k in self.gama_list)

        #    ii:change direction
        self.m.addConstrs(self.if_rt[j, i] + self.if_rt[i, k] <= 1 + self.if_x[i, j, k] for i, j, k in self.h_list)

        #    iii: no more than once
        self.m.addConstr(self.if_x.sum() <= 1)
                
        # Solve
        self.m.optimize()
        if(print_solution):
            self.printSolution()
    
    def printSolution(self):
        if self.m.status == GRB.OPTIMAL:
            print('\nMinValue: %g' % self.m.objVal)
            
            print('\nStrategy:')
            ot = []
            for var in self.m.getVars():
                ot.append(var.X)
            
            ot = ot[:self.num_routes]
            rt = []
            for i in range(self.num_routes):
                if ot[i] > 0 :
                    rt.append(self.routes[i])
            nrt = len(rt)
            to = self.opencity
            for i in range(nrt):
                for rr in rt:
                    if rr[0] == to:
                        print(rr)
                        to = rr[1]
                        if to == self.destination:
                            break
            
            opt_dist = np.dot(ot[:self.num_routes], self.dists.values())
            opt_time = np.dot(ot[:self.num_routes], self.Ts.values()) + 2 * (sum(ot[:self.num_routes]) - 1) + 18 * sum(ot[self.num_routes:])
            opt_path_influence = np.dot(ot[:self.num_routes], self.eidxs.values())
            opt_interval_passenger_flow = np.dot(ot[:self.num_routes], self.pidxs.values())
            print('Distance of Optimal Path (km): %g' % opt_dist)
            print('Time cost of Optimal Path (min): %g' % opt_time)
            print('Total path influence of Optimal Path: %g' % opt_path_influence)
            print('Total interval passenger flow index of Optimal Path: %g' % opt_interval_passenger_flow)
            return opt_dist, opt_time, opt_path_influence, opt_interval_passenger_flow

        else:
            print('No solution')
            #return 0, 0, 0, 0
            return np.nan, np.nan, np.nan, np.nan


parser = argparse.ArgumentParser()
parser.add_argument('--opencity', '-o', type=str, default='北京', help="start from here")
parser.add_argument('--destination', '-d', type=str, default='桂林', help="end here")
parser.add_argument('--filepath', '-f', default='./Project_.xls', help='file path')
args = parser.parse_args()

opt = RailwayOptimizer(opencity = args.opencity, destination = args.destination, filepath = args.filepath)
opt.solve()