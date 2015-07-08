import random

from Genotype import Genotype2048

class BaseGeneticAlgorithm (object):
	percent_pop_kept = 0.05

	def __init__ (self, population):
		self.epoch_counter = 0
		self.population = population
		self.genotypes = []
		for a in range (population):
			genotype = self.create_genotype ()
			self.genotypes += [genotype]

	def epoch (self, new_pop=None):
		keep = int (self.population * self.percent_pop_kept)
		if new_pop:
			self.population = new_pop

		self.genotypes = sorted (self.genotypes, key=lambda x: -x.score)		
		new_genotypes = self.genotypes [0:keep]

		self.score_total = None
		for a in range (self.population - keep):
			gene1, gene2 = self.rouletteSelection ()
			new_genotypes += [gene1.mate (gene2)]

		self.genotypes = new_genotypes

		scores = [gene.score for gene in self.genotypes]
		print 'Fitness (' + str (self.epoch_counter) + '): ' + str (max (scores)) + ', avg: ' + str (1.0 * sum(scores)/len(scores))
		self.epoch_counter += 1

	def rouletteSelection (self):
		if not self.score_total:
			self.score_total = 0
			for gene in self.genotypes:
				self.score_total += gene.score

		bin1 = random.randint (0, self.score_total - 1)
		bin2 = random.randint (0, self.score_total - 1)
		result1, result2 = None, None
		current = 0
		for gene in self.genotypes:
			current += gene.score

			if not result1 and current >= bin1:
				result1 = gene

			if not result2 and current >= bin2:
				result2 = gene

			if result1 and result2:
				break 

		return result1, result2

	def create_genotype (self):
		raise NotImplemented ()

	def __str__ (self):
		r = ''
		for gene in self.genotypes:
			r += str (gene.score) + '\n'
		return r




class GeneticAlgorithm2048 (BaseGeneticAlgorithm):


	def create_genotype (self):
		return Genotype2048 ()




ga = GeneticAlgorithm2048 (100)

while (True):
	ga.epoch ()