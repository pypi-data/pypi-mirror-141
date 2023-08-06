from ExplainAI.flx_data.input import input_dataset
d=input_dataset(flag=0)
# print(d)

from ExplainAI.data_processing.split_data import split_data
xtr,ytr,xte,yte=split_data(d,target="SWC").split_xy() #"SWC_F_MDS_1"
# print(xtr)
#
#
#
from ExplainAI.model.make_model import make_model
m,res,y_predict=make_model(modeltype='RandomForest',
                             x_train=xtr,
                             y_train=ytr,
                             x_test=xte,
                             y_test=yte)
print(res)
from ExplainAI.utils import get_x,get_features

x=get_x(d,target="SWC")
f=get_features(x)



from ExplainAI.explainers.shap_func.shap_func import shap_explainations_feature_value_d
s=shap_explainations_feature_value_d(m,x,f,color_num=2,subplot=True,describe=True)
