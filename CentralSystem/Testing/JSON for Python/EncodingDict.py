import json

data = [ { 'a':'A', 'b':(2,4), 'c':3.0, ('d',):'D tuple'}]

print 'first attempt'

try: 
	print json.dumps(data)
except (TypeError, ValueError) as err:
	print 'Error:', err

print 
print '2nd attempt'
print json.dumps(data, skipkeys=True)