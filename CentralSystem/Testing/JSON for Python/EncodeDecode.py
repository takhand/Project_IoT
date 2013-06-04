import json
import json_myobj

# encoder = json.JSONEncoder()
# data = [ { 'a':'A', 'b':(2, 4), 'c':3.0 } ]

# for part in encoder.iterencode(data):
#     print 'PART:', part

class MyEncoder(json.JSONEncoder):

	def default(self, obj):
		print 'default(' , repr(obj), ')'
		# Convert objects to a dictionary of their representation
		d = {'__class__':obj.__class__.__name__,  
				'__module__':obj.__module__,
				}
		d.update(obj.__dict__) 
		return d

obj = json_myobj.MyObj('internal data')
print obj
print MyEncoder().encode(obj)

