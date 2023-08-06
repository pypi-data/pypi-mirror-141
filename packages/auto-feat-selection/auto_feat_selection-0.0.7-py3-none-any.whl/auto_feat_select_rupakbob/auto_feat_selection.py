# -*- coding: utf-8 -*-
"""


@author: rupak
"""

def grid_feat_search(df,target='target',max_divergence=10):
    from kydavra import BregmanDivergenceSelector,ItakuraSaitoSelector
    #kydavra 0.3.1
    import pandas as pd
    
    
    cols = BregmanDivergenceSelector(max_divergence=max_divergence).select(df,target)
    cols1 =  ItakuraSaitoSelector(max_divergence=max_divergence).select(df,target)
    print("The important Features ",cols)
    
    return cols, cols1 

#index 0 = BregmanDivergenceSelector, index 1 = ItakuraSaitoSelector
#cols_BregmanDivergenceSelector = grid_feat_search(df,'target',5)[0]
#cols_ItakuraSaitoSelector = grid_feat_search(df,'target',5)[1]



    
def evaluate_grid_feat_search(df,feat_list,target ='target'):  
    #evaluation metrics
    from sklearn.metrics import confusion_matrix
    from sklearn.metrics import balanced_accuracy_score
    from sklearn.metrics import roc_auc_score
    from sklearn.metrics import classification_report
    
    def evaluate(y_pred,y_test):
        print("Confusion matrix \n",confusion_matrix(y_test, y_pred))
        print("Balanced Accuracy Score ", balanced_accuracy_score(y_test, y_pred))
        print("Roc AUC Score", roc_auc_score(y_test, y_pred))
        print("Classification Report \n", classification_report(y_test, y_pred))
    
    #With the selector------------------------------------------------------------------
    X  = df.drop(target,axis=1)
    y = df[target]

    #taking only the important features from the BregmanDivergenceSelector
    X = df.drop(feat_list,axis=1)

    #train test split
    from sklearn.model_selection import train_test_split
    X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3, random_state=1)

    #model with the selector
    from sklearn.linear_model import LogisticRegression
    lr_model = LogisticRegression()
    lr_model.fit(X_train,y_train)
    y_pred = lr_model.predict(X_test)
    
    from sklearn.ensemble import RandomForestClassifier
    rf_model = RandomForestClassifier()
    rf_model.fit(X_train,y_train)
    y_pred_1 = rf_model.predict(X_test)
    
    print("Accuracy with Selector using base log model----------------")
    evaluate(y_pred, y_test)
    print("Accuracy with Selector using Random Forest Model...........")
    evaluate(y_pred_1,y_test)
    
    #-----------------------------------------------------------------------------
    #Without the selector
        
    X  = df.drop(target,axis=1)
    y = df[target]
    
    #train test split
    from sklearn.model_selection import train_test_split
    X_train,X_test,y_train,y_test = train_test_split(X,y,test_size=0.3, random_state=1)
    
    #model with the selector
    from sklearn.linear_model import LogisticRegression
    lr_model = LogisticRegression()
    lr_model.fit(X_train,y_train)
    y_pred = lr_model.predict(X_test)
    
    from sklearn.ensemble import RandomForestClassifier
    rf_model = RandomForestClassifier()
    rf_model.fit(X_train,y_train)
    y_pred_1 = rf_model.predict(X_test)
    
    print("Accuracy without Selector using base log model ------------")
    evaluate(y_pred,y_test)    
    print("Accuracy without Selector using base Random Forest model ------------")
    evaluate(y_pred_1,y_test)


#evaluate_grid_feat_search(df,cols_BregmanDivergenceSelector,'target')    
#evaluate_grid_feat_search(df,cols_ItakuraSaitoSelector,'target')    
    