import random

class BaseGenotype (object):
	size = 200
	mutation = 5000

	def __init__ (self, genes=None):
		if not genes:
			self.genes = [self.random_gene () for a in range (self.size)]
		else:
			if len (genes) != self.size:
				raise Exception ("Gene sizes do not match.")
			self.genes = genes
		self.eval_score ()

	def eval_score (self):
		self.score = int (self.get_fitness_score (self.genes))

	def mate (self, other):
		if self.size != other.size:
			raise Exception ("Gene sizes do not match.")

		flop = random.randint (0, self.size)
		new_gene = self.genes [0:flop] + other.genes [flop:]
		if random.randint (0, self.mutation) < self.size:
			new_gene [random.randint (0, self.size - 1)] = self.random_gene ()

		return self.__class__ (new_gene)

	def get_fitness_score (self):
		raise NotImplemented ()

	def random_gene (self):
		raise NotImplemented ()		

	def __str__ (self):
		return str (self.genes)