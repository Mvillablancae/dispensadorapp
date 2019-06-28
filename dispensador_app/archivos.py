import sys
a = open("archivo.txt","w")

a.write(sys.argv[1])

a.close()
