import string,random

print("Generating a new auth token")
ipA = input("Enter the device IP Adress: ")
letters = string.ascii_letters
resStr = ''.join(random.choice(letters) for i in range(16))
f = open("tokens.txt","a")
f.write(ipA + ":" + resStr + "\n")
f.close
print("Your new auth Token is: " + resStr)
print("ATTENTION: This token will only work with the specified IP Adress (except the discover Function)")