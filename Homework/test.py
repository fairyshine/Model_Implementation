from sklearn.svm import LinearSVC

X=[[3,3],[3,2],[1,1]]
y=[1,1,-1]
model = LinearSVC(C=1)#C越大，惩罚越大，越不容易出现分类错误的情况
model.fit(X, y)

b = model.intercept_
w = model.coef_
print('b=', b)
print('w=', w)