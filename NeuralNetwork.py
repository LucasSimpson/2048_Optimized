from numpy import *

class Layer (object):
	mask = vectorize (lambda x: 1 if x > 0 else 0)

	def __init__ (self, inputs, neurons):
		self.inputs = inputs
		self.neurons = neurons
		self.size = self.inputs * self.neurons + self.neurons
		self.weights = None
		self.activation_levels = None

	def build_from_array (self, values):
		self.weights = array (values [:self.inputs * self.neurons]).reshape (self.inputs, self.neurons)
		self.activation_levels = array (values [self.inputs * self.neurons:]).reshape (1, self.neurons)

	def eval (self, inputs):
		tmp = inputs.dot (self.weights)
		tmp = tmp - self.activation_levels
		tmp = self.mask (tmp)
		return tmp

	def __str__ (self):
		return str (self.weights) + '\n' + str (self.activation_levels)


class NeuralNetwork (object):
	def __init__ (self, layers):
		self.layers = [Layer (layers [a], layers [a + 1]) for a in range (len (layers) - 1)]

	def build_from_array (self, values):
		indices = [0]
		for a in range (len (self.layers)):
			indices += [indices [a] + self.layers [a].size]
			self.layers [a].build_from_array (values [indices [a]:indices [a + 1]])

	def eval (self, inputs_):
		result = array (inputs_).reshape (1, len (inputs_))
		for layer in self.layers:
			result = layer.eval (result)
		return result [0].tolist ()

	def __str__ (self):
		r = ''
		for index, layer in enumerate (self.layers):
			r += '\nLevel ' + str (index) + '\n'
			r += str (layer)
		return r + '\n'

	@staticmethod
	def gene_length_from_layers (layers_):
		return sum ([(layers_ [a] + 1) * layers_ [a + 1] for a in range (len (layers_) - 1)])