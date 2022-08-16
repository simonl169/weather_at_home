import os

def df():
  s = os.statvfs('//')
  print(os.statvfs('//'))
  return ('{0} MB'.format((s[0]*s[3])/1048576))


print(df())