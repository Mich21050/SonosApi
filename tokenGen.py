import string,random

def genSave(ipA):
    letters = string.ascii_letters
    resStr = ''.join(random.choice(letters) for i in range(16))
    f = open("tokens.txt","a")
    f.write(ipA + ":" + resStr + "\n")
    f.close
    return resStr

print("Generating a new auth token")
ipA = input("Enter the device IP Adress: ")
print("Your new auth Token is: " + genSave(ipA))
print("ATTENTION: This token will only work with the specified IP Adress (except the discover Function)")