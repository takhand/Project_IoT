import json

g = [2,3,5,555]
cool = [1,2,4,577,85,g]
data = [ {'a' : 'A', 'b':(2,4), 'c':3.0, 'cool': cool},]
print 'DATA', repr(data)

unsort = json.dumps(data)
sort = json.dumps(data, sort_keys=True)
sort2 = sort
indent = json.dumps(data, sort_keys=True, indent=2)
separator = json.dumps(data, separators=(',', ':'))


print type(data)
print type(unsort)

print unsort
print sort

print unsort == sort
print sort == sort2
# print 'Indent', indent
print len(unsort)
print len(sort)
print len(indent)
print separator
print len(separator)