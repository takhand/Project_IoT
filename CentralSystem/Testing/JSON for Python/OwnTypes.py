import json 
import json_myobj

obj = json_myobj.MyObj('Instance value goes here')


print '1st attempt'
try:
	print json.dumps(obj)
except TypeError, err: 
	print 'Error:', err


def convert_to_builtin_type(obj):
	print 'default(' , repr(obj) , ')'
	d = { '__class__':obj.__class__.__name__,
		  '__module__':obj.__module__,
		}
	d.update(obj.__dict__)
	return d

def dict_to_object(d):
	if '__class__' in d: 
		class_name = d.pop('__class__')
		module_name = d.pop('__module__')
		module = __import__(module_name)
		print 'MODULE:' , module 
		class_ = getattr(module, class_name)
		print 'CLASS:', class_
		args = dict( (key.encode('ascii'), value) for key, value in d.items())
		print 'INSTANCE ARGS:' , args
		inst = class_(**args)

	else: 
		inst = d
	return inst 

encoded_object = '[ {"s": "instane value goes here", "__module__" : "json_myobj", "__class__": "MyObj"}]'

myobj_instance = json.loads(encoded_object, object_hook=dict_to_object)
print myobj_instance



# print
# print 'With Default'
# print json.dumps(obj, default=convert_to_builtin_type)