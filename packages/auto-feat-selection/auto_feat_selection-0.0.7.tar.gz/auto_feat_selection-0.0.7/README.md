

# Dependencies 
### Make sure you have install the sklearn  
### sklearn version == 1.0.1
### Feature Selection using Bregman divergence & Itakura Saito

## What is Bregman Divergence & Itakura Saito
In statistics, divergence is a function that finds and measures differences using
the distance between two probability distributions.
Bregman divergence is one of many divergences. It can be calculated with the squared Euclidean distance:

###Steps to apply auto_feat_selection

#import
```
from auto_feat_select_rupakbob import auto_feat_selection
```

#grid_feat_search(dataframe,'taget_column_name', max_divergence(default = 0,max = 10)accepted divergence with the target column) 
```
index 0 = BregmanDivergenceSelector, index 1 = ItakuraSaitoSelector
cols_BregmanDivergenceSelector = grid_feat_search(df,'target',5)[0]
cols_ItakuraSaitoSelector = grid_feat_search(df,'target',5)[1]
```

### Evaluate if the selected features improves the model

###Currently supports Logistic Regression base model with goal to evaluate feature performance

#evaluate_grid_feat_search(dataframe,'taget_column_name')
```
auto_feat_selection.evaluate_grid_feat_search(df,cols_BregmanDivergenceSelector,target ='target')
auto_feat_selection.evaluate_grid_feat_search(df,cols_ItakuraSaitoSelector,target ='target')

```
