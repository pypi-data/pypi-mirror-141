import numpy as np


class LinearRegression():


    def fit(self,X,y):
    
        rows_x, columns_x = X.shape 
        X=np.c_[np.ones(rows_x),X] 
    
        X_t=np.transpose(X)

        arr_inverse=np.linalg.inv(np.dot(X_t,X))
        theta=np.linalg.multi_dot([arr_inverse,X_t,y])

        self.intercept=theta[0]
        self.weights=np.delete(theta,0)  

    
    def predict(self,X):
        list=[]
        y_hat=np.array(list)
        
    
        y_hat=np.add(np.dot(X,self.weights),self.intercept)
        return y_hat

