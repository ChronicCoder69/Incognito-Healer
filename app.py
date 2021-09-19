from flask import Flask, request, jsonify, render_template
from flask_mail import Mail,Message
import pickle
import numpy as np
import pymongo
app = Flask(__name__)
model = pickle.load(open('modelA.pkl', 'rb'))
# Create Mongo Client using username and password

client = pymongo.MongoClient("mongodb+srv://paras123:paras123@blog.w2rbt.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")


app.config['DEBUG']=True
app.config['TESTING']=False
app.config['MAIL_SERVER']= 'smtp.gmail.com'
app.config['MAIL_PORT']=587
app.config['MAIL_USE_TLS']=True
app.config['MAIL_USE_SSL']=False
app.config['MAIL_USERNAME']='incognitohealer@gmail.com'
app.config['MAIL_PASSWORD']='incognito123'
app.config['MAIL_DEFAULT_SENDER']=('incognitohealer@gmail.com')
app.config['MAIL_MAX_EMAILS']=None
app.config['MAIL_ASCII_ATTACHMENTS']= False

mail=Mail(app)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict1',methods=['POST'])
def predict1():
    int_features = [x for x in request.form.values()]
    l = []
    #['S ADITYA', 's.aditya04042001@gmail.com', '21/07/2001', '9:00 to 10:00', ' Child psychiatrist', '']
    for i in range(len(int_features)-1):
        l.append(int_features[i])
    name=l[0]
    email=l[1]
    date=l[2]
    time=l[3]
    department=l[4]
    msg = Message('INCOGNITO HEALER', recipients=[email])
    msg.html = 'MESSAGE FROM INCOGNITO HEALER!'+'<br><br</br></br>'+"<br>Name : </br>"+name+'\n'+"<br>Department : </br>"+department+'\n'+"<br>Date : </br>"+date+'\n'+"<br>Time : </br>"+time+'\n'+'<br><br</br></br>'+"<br> join in this meet  at suitable slot</br>"+'<br>https://meet.google.com/cjo-raps-jwf</br>'
    mail.send(msg)
    return render_template('index.html')
@app.route('/predict3',methods=['POST'])
def predict3():
   if request.method=='POST':
       name = request.form.get("name")
       text = request.form.get("Feed")
       data = {
           'Name': name,
           'Feedback': text
       }
   with client:
        db = client.Feedbackform
        db.prediction.insert_one(data)

   return render_template('index.html')


@app.route("/practice")
def practice():
    """ return the rendered template """
    return render_template("practice.html")

@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    int_features = [ x for x in request.form.values()]
    l=[]

    for i in range(len(int_features)-1):
        l.append(int_features[i+1])
    l = [int(i) for i in l]
    final_features = [np.array(l)]
    prediction = model.predict(final_features)
    output = prediction[0]
    if output == 0:
        output='NO'
        return render_template('practice.html', prediction_text='{} you dont want  to talk with Counsellor '.format(output))
    else:
        output = 'YES'
        return render_template('practice.html',prediction_text='{} you have to talk with Counsellor'.format(output))


@app.route('/predict_api',methods=['POST'])
def predict_api():
    '''
    For direct API calls trought request
    '''
    data = request.get_json(force=True)
    prediction = model.predict([np.array(list(data.values()))])

    output = prediction[0]
    return jsonify(output)


if __name__ == '__main__':
    app.run()
