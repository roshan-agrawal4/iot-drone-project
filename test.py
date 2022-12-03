from firebase import firebase
mydb = firebase.FirebaseApplication('https://drone-system-iot-default-rtdb.firebaseio.com/', None)
name=input("name")
data={"Name": name, "Age": 25}
mydb.post("testing", data)
