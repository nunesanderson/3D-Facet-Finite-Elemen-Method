clear_all()
import numpy

x = numpy.arange(10, dtype=numpy.int32).reshape((-1,2))

print x.shape

cleared = numpy.delete(x, [0,2,3], 0)
print cleared.shape