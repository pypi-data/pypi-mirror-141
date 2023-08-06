Machine Learning algorithm optimizer for sklearn and evaluation Metrics for Regression Model.
AutoOptimizer provides tools to automatically optimize machine learning model for a dataset with very little user intervention.

It refers to techniques that allow semi-sophisticated machine learning practitioners and non-experts 
to discover a good predictive model pipeline for their machine learning algorithm task quickly,
with very little intervention other than providing a dataset.


#Prerequisites:

jupyterlab(contains all sub packages except mlxtend) or: {sklearn,matplotlib,mlxtend,numpy}	


#Usage:


Scikit learn supervised and unsupervised learning models using python.


{DBSCAN, KMeans, MeanShift,  LogisticRegression, KNeighborsClassifier, SupportVectorClassifier, DecisionTree}


#Running for example:


from autooptimizer.dbscan import dbscan


from autooptimizer.kmeans import kmeans


from autooptimizer.meanshift import meanshift


from autooptimizer.logreg import logreg


from autooptimizer.knn import knn


from autooptimizer.svc import svc


from autooptimizer.decisiontree import decisiontree


dbscan(x)


kmeans(x)


meanshift(x)


logreg(x,y)


knn(x,y)


svc(x,y)


decisiontree(x,y)


'x' should be your independent variable or feature's values and 'y' is target variable or dependent variable.
The output of the program is the maximum possible accuracy with the appropriate parameters to use in model.

#Metrics

{root_mean_squared_error, root_mean_squared_log_error, root_mean_squared_precentage_error,
symmetric_mean_absolute_precentage_error, mean_bias_error, relative_squared_error, root_relative_squared_error
relative_absolute_error, median_absolute_percentage_error, mean_absolute_percentage_error}


from autooptimizer.metrics import root_mean_squared_error


root_mean_squared_error(true, predicted)


#Contact and Contributing:
Please share your good ideas with us. 
Simply letting us know how we can improve the programm to serve you better.
Thanks for contributing with the programm.

>>>https://github.com/mrb987/autooptimizer
>>>info@genesiscube.ir