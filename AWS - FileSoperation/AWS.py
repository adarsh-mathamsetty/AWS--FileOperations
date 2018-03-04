from flask import Flask,request, make_response
import boto3
import string
import hashlib

app = Flask(__name__)

s3=boto3.resource('s3', aws_access_key_id='AKIAJCLN37JRAF7QBRRA', aws_secret_access_key='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', region_name='us-east-2')
bucket=s3.Bucket('bucket1files')
bucket1=s3.Bucket('credentials1')

@app.route('/')
def index():
  #return app.send_static_file('home.html') 
	return app.send_static_file('index.html')


@app.route('/logout')
def logout():
  #return app.send_static_file('home.html')
	return app.send_static_file('index.html')

"""@app.route('/login', methods=['POST'])
def login():

  username= request.form['uname']
  password= request.form['psw']
  for obj in bucket1.objects.all():
    data = obj.get()["Body"].read()
    splits=string.split(data,',')
    
    for vals in splits:
      values=str(vals)
      value=string.split(values,' ')
      
      if(username==value[0] and password==value[1]):
        return app.send_static_file('index.html')
    return "Invalid credentials" """

@app.route('/upload', methods=['POST'])
def upload():
  f= request.files['file']
  comment = request.form.get('comment')
  file_name=f.filename
  content=f.read()
   
  
  s3.Bucket('bucket1files').put_object(Key=file_name, Body=content)
  comment = request.form.get('comment')
  
  file = open("comment.txt","w")
  file.write(comment)
  file1 = open("comment.txt","rb")
  data=file1.read()
  s3.Bucket('bucket1files').put_object(Key="comment.txt", Body=data)
  
  #image = Image.open(file_name)
  #image.show()
  #if file_name[-3:] == 'jpg':
	#print image
  
   
  return "uploaded succesfully"

@app.route('/download', methods=['POST', 'GET'])
def download():
  file_name = request.args.get('dwnfile', '')
  for obj in bucket.objects.all():
    if file_name == obj.key:
      data = obj.get()["Body"].read()
      response = make_response(data)
      response.headers["Content-Disposition"] = "attachment; filename=" + file_name
      return response
  return "File Not Found"


@app.route('/delete', methods=['POST','GET'])
def delete():
  filename = request.args.get('delfile', '')
  for obj in bucket.objects.all():
    if filename == obj.key:
	  obj.delete()
	  return 'Deleted'
  return "File not Found"

@app.route('/list1', methods=['POST','GET'])
def list1():

	
  lists=''
  for obj in bucket.objects.all():
    lists=lists+obj.key+"<br>"
    print(obj.key)
    size = obj.size
    print size
    Modified = obj.last_modified
    print Modified
    
  return lists
  

if __name__ == '__main__':
  app.run()