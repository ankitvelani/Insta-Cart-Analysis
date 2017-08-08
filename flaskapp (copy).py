from flask import Flask , render_template
from Connection import  Connection

app=Flask(__name__)
DBConnection=Connection()

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

if __name__=='__main__':
    app.run(debug=True)