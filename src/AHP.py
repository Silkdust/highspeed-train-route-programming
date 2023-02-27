# %%
import numpy as np
import pandas as pd

# %%
class SingleLayerAHP:
    def __init__(self, factor_names, importance_matrix = None):
        self.RI_dict = {1: 0, 2: 0, 3: 0.58, 4: 0.96, 5: 1.12, 6: 1.24, 7: 1.32, 8: 1.41, 9: 1.45, 10: 1.49}
        self.n_factors = len(factor_names)
        self.factors = factor_names
        self.matrix = np.ones(shape = (self.n_factors, self.n_factors))
        self.__get_relative_importance(matrix = importance_matrix)
        self.df = pd.DataFrame(self.matrix, index = self.factors, columns = self.factors)
        display(self.df)
    
    def __get_relative_importance(self, matrix = None):
        if(matrix is None):
            for ind, factor in enumerate(self.factors):
                for j in range(ind + 1, self.n_factors):
                    relative_importance = float(input("Input Factor {}'s Importance Relative to Factor {}".format(factor, self.factors[j])))
                    self.matrix[ind][j] = relative_importance
                    self.matrix[j][ind] = 1 / relative_importance
        else:
            self.matrix = matrix
            for i in range(self.n_factors):
                for j in range(i):
                    self.matrix[i][j] = 1 / self.matrix[j][i]
    
    def AHP(self):
        w, v = np.linalg.eig(self.matrix)
        self.lambda_max = np.max(abs(w))
        ind = list(w).index(max(abs(w)))
        self.CI = (self.lambda_max - self.n_factors) / (self.n_factors - 1)
        self.RI = self.RI_dict[self.n_factors]
        self.CR = self.CI / self.RI
        self.eigvector = v[:, ind] / v[:, ind].sum(axis = 0)

        if(self.CR > 0.1):
            print("Warning: The random consistency index is {}. \nThe judgment matrix does not have satisfactory consistency.".format(self.CR))
        else:
            print("The random consistency index is {}. \nThe judgment matrix has satisfactory consistency.".format(self.CR))
        
        print("The corresponding eigenvector is: ", abs(self.eigvector))

# %%
matrix = [[1,0.75,3,2],
[1,1,3.5,2.5],
[1/3,1/3,1,2],
[2/7,0.5,0.5,1]]
testclass = SingleLayerAHP(factor_names=['Distance', 'Time', 'Blockness', 'PassengerFlow'], importance_matrix = matrix)
testclass.AHP()

# %%
print(testclass.lambda_max)
print(testclass.CI)


