import shutil, fnmatch, os

n = len(fnmatch.filter(os.listdir("randomcricket"), '*.txt')) - 2

print (n)

shutil.move('scorecard.txt','randomcricket/scorecard{}.txt'.format(n))