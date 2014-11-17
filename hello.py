import  os
from flask import Flask

app=Flask(__name__) #main app
@app.route('/')
def hello():
	return 'Hello World'