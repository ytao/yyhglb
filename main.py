from flask import Flask,redirect
from flask import render_template
from flask import request
import with_excel as we
import conf as c
import json
import pdb
import sys

dataList_values={}
app = Flask(__name__)
_DEBUG=True
# _DEBUG=False

@app.route('/getAllRecords')
def getAllRecords():
    l=[]
    new_record=we.project_data()
    # new_record.readRecords(l)
    the_captions=[]
    the_datas=[]
    the_captions,the_datas=new_record.getRecords()
    return render_template('getAllRecords.html',the_captions=the_captions,the_datas=the_datas)

@app.route('/setDataTableLanguage')
def setDataTableLanguage():
    return render_template('chinese.json')



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/writeRecord',methods=['GET','POST'])
def writeRecord():
    '''
    处理数据增加的部分
    '''
    if request.method=='POST':
        new_record=we.project_data()
        if (new_record.init_success ==False):
            return
        # 得到行数信息
        editRow=request.form.get('editRow')
        if (editRow==''):
            editRow=-2
        else:
            editRow=int(editRow)
        # 得到三个日期数据
        error_date=request.form.get('error_date')
        propose_date=request.form.get('propose_date')
        actual_date=request.form.get('actual_date')

        if len(error_date)>1:
            c.dic_date['error_year'],c.dic_date['error_month'],c.dic_date['error_day'] =error_date.split('-')
        else:
            c.dic_date['error_year'], c.dic_date['error_month'],c.dic_date['error_day']='','',''

        if len(propose_date)>1:
            c.dic_date['propose_year'],c.dic_date['propose_month'],c.dic_date['propose_day'] =propose_date.split('-')
        else:
            c.dic_date['propose_year']='' 
            c.dic_date['propose_month']=''
            c.dic_date['propose_day']=''

        if len(actual_date)>1:
            c.dic_date['actual_year'],c.dic_date['actual_month'],c.dic_date['actual_day'] =actual_date.split('-')
        else:
            c.dic_date['actual_year']='' 
            c.dic_date['actual_month']=''
            c.dic_date['actual_day']=''

        # 得到其它数据
        for i in c.dic_error_information.keys():
            try:
                c.dic_error_information[i]=request.form.get(i)
            except:
                print('在i='+i+'时候出错了')

        # 得到人员信息
        list_persons=new_record.getPeopleList()
        dic_persons={}
        for x in list_persons:
            dic_persons[x]=request.form.get(x)
            if dic_persons[x]==None:
                dic_persons[x]=''

        # 写入数据
        new_record.writePeopleStatus(dic_persons,editRow)
        new_record.testWrite2(c.dic_error_information,c.dic_date,editRow)
        return render_template('success.html')


@app.route('/getOneRecord')
def getOneRecord():
    '''
    读取已有的记录
    '''
    # print(dataList_values)
    r=request.args.get('editRow')
    if (r==None):
        r=-2
    new_record=we.project_data()
    mydata={}
    mydata=new_record.readOneRecord(r)
    myconf={}
    myconf=new_record.readDataList()
    list_persons=new_record.getPeopleList()
    dic_persons=new_record.getPeopleStatus(r)
    return render_template('getOneRecord.html',dic_value=mydata,editRow=r,dataList=myconf,dic_persons=dic_persons,list_persons=list_persons)

# 程序启动
if __name__ == '__main__':
    if (_DEBUG==True):
        app.debug=True
    else:
        app.debug=False
    app.run(host='0.0.0.0',port=5000)
# vim : se fdc=2 :
