from flask import Flask , render_template
from Connection import  Connection
import pandas as pd
import numpy as np

app=Flask(__name__)
DBConnection=Connection()

pd.ResultSetProducts=DBConnection.select_df('products')
pd.ResultSetProductOrder=DBConnection.select_df('order_product')
pd.ResultSetDepartment=DBConnection.select_df('departments')    
pd.ResultSetOrder=DBConnection.select_df('orders')

@app.route('/')
def index():
    data={}
    
    ResultSet=DBConnection.select('departments','count(*)')
    data['DepartmentCount']=ResultSet[0][0]
    ResultSet = DBConnection.select('aisles','count(*)')
    data['aisles'] = ResultSet[0][0]

    ResultSet = DBConnection.select('orders','count(*)')
    data['orders'] = ResultSet[0][0]

    ResultSet = DBConnection.select('products','count(product_id)')
    data['products'] = ResultSet[0][0]

    
    return render_template('index.html',data=data)
@app.route('/products')
def product():
    data={}

    #### Most Frequenly Ordered Products ########
    pd.ResultSet=pd.ResultSetProductOrder.groupby('product_id')['product_id'].aggregate({'ProductCount':'count'}).reset_index()
    pd.ResultSet=pd.merge(pd.ResultSet,pd.ResultSetProducts,how='left',on=['product_id'])  
    pd.ResultSet=pd.ResultSet.sort_values(by='ProductCount',ascending=False).reset_index()
    data['MostFrequentProduct']=pd.ResultSet[:10]

    

    #### Show % of Reordered product in whole dataset
    pd.ResultSet=pd.ResultSetProductOrder.groupby('reordered')['reordered'].aggregate({'RorderFreq':'count'}).reset_index()
    pd.ResultSet['Percentage']=pd.ResultSet['RorderFreq']*100/sum(pd.ResultSet['RorderFreq'])
    data['ReorderedPercentage']=pd.ResultSet
    print pd.ResultSet

    

    #### List Top Products which has higher probability 
    pd.ResultSet=pd.ResultSetProductOrder.groupby('product_id')['reordered'].aggregate({'TotalReorder':'count','ReorderSum':'sum'})
    # Computer Probability
    pd.ResultSet['Probability']=pd.ResultSet['ReorderSum']/pd.ResultSet['TotalReorder']
    pd.ResultSet=pd.ResultSet[pd.ResultSet.ReorderSum>=75].sort_values('ReorderSum',ascending=False).reset_index()
    # Merge
    pd.ResultSet=pd.merge(pd.ResultSet,pd.ResultSetProducts[['product_id','product_name']],how='left',on=['product_id'])
    pd.ResultSet.sort_values('Probability',ascending=False).reset_index()
    data['ReorderedProbability']=pd.ResultSet.head(10)
    

    return render_template('product.html',data=data)

@app.route('/departments')
def department():
    data={}

    pd.ResultSet=pd.ResultSetProducts.groupby('department_id')['product_id'].aggregate({'DepartmentCount':'count'}).reset_index()
    pd.ResultSet=pd.merge(pd.ResultSet,pd.ResultSetDepartment[['department_id','department']],how='left',on=['department_id'])
    pd.ResultSet=pd.ResultSet.sort_values('DepartmentCount',ascending=False).reset_index()
    
    data['MostImportantDeptProduct']=pd.ResultSet.head(10)
    

    # Most Important Department By Order 
    pd.ResultSet=pd.merge(pd.ResultSetOrder,pd.ResultSetProductOrder[['order_id','product_id']],how='inner',on=['order_id'])
    pd.ResultSet=pd.merge(pd.ResultSet,pd.ResultSetProducts[['product_id','department_id']],how='inner',on=['product_id'])
    pd.ResultSet=pd.merge(pd.ResultSet,pd.ResultSetDepartment,how='inner',on=['department_id'])

    pd.ResultSet=pd.ResultSet.groupby('department')['order_id'].aggregate({'DepartmentByOrder':'count'}).reset_index()
    pd.ResultSet=pd.ResultSet.sort_values('DepartmentByOrder',ascending=False).reset_index()
   

    data['DepartmentByOrder']=pd.ResultSet.head(10)
    

    return render_template('department.html',data=data)
if __name__=='__main__':
    app.run(debug=True)