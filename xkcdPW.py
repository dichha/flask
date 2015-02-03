
from flask import Flask, request, render_template,redirect, url_for
import random
app = Flask(__name__)
app.debug=True
@app.route('/')
def showForm():

	return '''
	<html>
		<head>
			<title>XKCD password Generator</title>
			<style>
				input{
					width:250px;
					left:200px;

				}
				#outerBody{
					width:450px;
					height:600px;
					background-color:#FFCC99;if len("".join(gpwList))<=TotalPWLen and len("".join(gpwList))>10:
			#done=Tru
					border: 1px;
				}	
				label{
					display: inline-block;
					float:left;
					clear:right;
					width:180px;
					text-align:left;
					text-decoration: underline;
					color:#FF6600;

				}
				input{
					display: inline-block;
					float: right;
				}
				


			</style>
		</head>
			<body>
			<div id="outerBody">
				<h1 style="color:blue;text-align:center;" >Password Generator</h1>
				<form id="pwQ" method='get' action='/showList'>
					<label for="longestW">LongestWord:</label><input type="number" min="0" name="LongestWord" placeholder="Enter length of longest word"/><br>
					<label for="shortestW">ShortestWord:</label><input type="number" min="0" name="ShortestWord" placeholder="Enter length of shortest word"/><br>
					<label for="pwLength">Length of overall word:</label><input type="number" min="0" name="PasswordLength" placeholder="Enter length of overall passwords" /><br>
					<label for="optimize">Optimize for typing speed</label><br><br>
					<input type="checkbox" id="optimise" name="Optimise" value="Yes">Yes<br>
					<input type="checkbox" id="optimise" name="Optimise" value="No">No<br>
					
					<label for="substitution">Substitution</label><br><br>
					<input type="checkbox" id="substitution" name="Substitution" value="3==e">3==e<br>
					<input type="checkbox" id="substitution" name="Substitution" value="0==o">0==o<br>
					<input type="checkbox" id="substitution" name="Substitution" value="1==l">1==l<br>
					<input type="checkbox" id="substitution" name="Substitution" value="5==s">5==s<br>
					<input type="checkbox" id="substitution" name="Substitution" value="4==a">4==a<br>
					<input type="checkbox" id="substitution" name="Substitution" value="9==g">9==g<br>
					<input type="checkbox" id="substitution" name="Substitution" value="!==i">!==i<br>
					<label for="capitalisation">Capitalisation</label><br><br>
					<input type="checkbox" id="capitalisation" name="capitalisation" value="First Word">First Word<br>
					<input type="checkbox" id="capitalisation" name="capitalisation" value="Second Word">Second Word<br>
					<input type="checkbox" id="capitalisation" name="capitalisation" value="Third Word">Third Word<br>
					<input type="checkbox" id="capitalisation" name="capitalisation" value="Fourth Word">Fourth Word<br>

					
					<input type="submit" id="submit" value="submit"/>
				</form>
			</div>
			</body>
	</html>'''
@app.route('/showList')
def evalForm():


	qs= request.query_string


	#return render_template("index.html", qs=qs)

	#print "<br>"
	arrayKV= qs.split('&')
	#print arrayKV
	LongestWordLen=int(arrayKV[0].split('=')[1])
	#print LongestWordLen
	ShortestWordLen=int(arrayKV[1].split('=')[1])
	#print ShortestWordLen
	TotalPWLen=int(arrayKV[2].split('=')[1])
	#print TotalPWLen
	optimiseO=str(arrayKV[3].split('=')[1])
	#print optimiseO
	if 'PasswordLength' in qs:
		arraySub=qs.split('&')
		#print arraySub
		subV=[]
		subK=[]
		capi=[]
		for i in range(len(arraySub)):
			if (str(arrayKV[i].split('=')[0]))=="Substitution":
				#(arrayKV[i].split('=')[0])
				subValue=(arrayKV[i].split('=')[1])
				sub=subValue.split('%3D%3D')
				if sub[0]=="%21":
					sub[0]="!"
					subK.append(sub[0])
					subV.append(sub[1])
				else:
					subV.append(sub[1])
					subK.append(sub[0])
			#print"<br>"
			if (str(arrayKV[i].split('=')[0]))=="capitalisation":
				capV=arrayKV[i].split('=')[1]
				cap=capV.replace('+',' ')
				#print (cap)
				if cap=="First Word":
					capi.append(0)
				elif cap=="Second Word":
					capi.append(1)
				elif cap=="Third Word":
					capi.append(2)
				elif cap=="Fourth Word":
					capi.append(3)
				else:
					capi=None
		#print(capi)

				


		#print"<br>"
	wordFile =open("wordList.txt")
	#wordFile = open("/usr/share/dict/words",'r')
	wordList = wordFile.readlines()
	#print(len(wordList))
	def optimiseType(word):
		leftHand="asdfgzxcvbqwert"
		rightHand="lkjhpoiuymn"
		score=0.0
		for i in range(len(word)-1):
			if word[i] in leftHand and word[i+1] in rightHand:
				score+= 1
			elif word[i] in rightHand and word[i+1] in leftHand:
				score+=1
			elif (word[i] in rightHand) ==(word[i+1] in leftHand):
				score+=2
		return (score/(len(word)-1))

	if optimiseO == "Yes":
		goodWords=[]
		for word in wordList:
			if optimiseType(word) >= 0.5:
				gWord=word[:-1]
				goodWords.append(gWord)
		#print(goodWords)
	else:
		goodWords=[]
		for word in wordList:
			aWord=word[:-1]
			goodWords.append(aWord)
		#print(goodWords)
	#def checkWordLen(num):

	def generatePW():
		done=False
		while not done:
			pwList=[]
			gpwList=[]
			sgpwList=[]
			capiPWword=[]
			for i in range(4):
				pwList.append(goodWords[random.randrange(len(goodWords))])
			for j in range(len(pwList)):
				wLen=len(pwList[j])
				if (wLen>=ShortestWordLen) and(wLen<=LongestWordLen):
					gpwList.append(pwList[j])
			#print(gpwList)
			for k in range(len(gpwList)):
				word=gpwList[k]
				#print (word)
				for v in range(len(subV)):
					if subV[v] in word:
						word=word.replace(subV[v],subK[v])
						sgpwList.append(word)
			for s in range(len(sgpwList)):
				sWord=sgpwList[s]
				for c in capi:
					#print(c)
					if c==s:
						#print(s)
						for l in sWord:
							#print(l)
							#letter=(sWord[l])
							if l.isalpha() and l.islower():
								l=l.upper()
								#print(l)
								capiPWword.append(l)
								
							else:
								capiPWword.append(l)
						capiW="".join(capiPWword)
						#print(capiW)
						sgpwList[s]=capiW


					else:
						break
						

							
			#print(sgpwList)

			if len("".join(sgpwList))<=TotalPWLen and len("".join(sgpwList))>10:
				done=True


		return"|".join(sgpwList),len("".join(sgpwList))
		#	xkcd="|".join(sgpwList)
		#	lenXKCD=len("".join(sgpwList))


		


		
	pw=[]
	count=[]
	for j in range(10):
		xkcd,lenXKCD=generatePW()
		pw.append(xkcd)
		count.append(lenXKCD)

	return render_template("index.html", pw_count=zip(pw,count))





if __name__ == '__main__':
	app.run()
