import random

class Genotype2048 (object):
	size = 200
	mutation = 5000

	def __init__ (self, genes=None):
		if not genes:
			self.genes = [self.random_gene () for a in range (self.size)]
		else:
			if len (genes) != self.size:
				raise Exception ("Gene sizes do not match.")
			self.genes = genes

		self.score = self.get_fitness_score ()

	def random_gene (self):
		return random.randint (0, 1000)		

	def mate (self, other):
		if self.size != other.size:
			raise Exception ("Gene sizes do not match.")

		flop = random.randint (0, self.size)
		new_gene = []
		for a in range (len (self.genes)):

			if random.randint (0, self.mutation) == 0:
				new_gene += [self.random_gene ()]
			elif a < flop:
				new_gene += [self.genes [a]]
			else:
				new_gene += [other.genes [a]]

		return self.__class__ (new_gene)

	def get_fitness_score (self):
		score = 0
		for gene in self.genes:
			score += gene
		return score

	def __str__ (self):
		return str (self.genes)