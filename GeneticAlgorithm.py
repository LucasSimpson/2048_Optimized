import random, multiprocessing

cores = multiprocessing.cpu_count ()


class BaseGeneticAlgorithm (object):
	percent_pop_kept = 0.05

	def __init__ (self, population):
		self.epoch_counter = 0
		self.population = population
		self.genotypes = []
		for a in range (population):
			genotype = self.create_genotype ()
			self.genotypes += [genotype]
		self.genotypes = self.sorted_pop ()

	def epoch (self, new_pop=None):
		if new_pop:
			self.population = new_pop
			self.genotypes = self.sorted_pop ()

		self.genotypes = self.make_new_pop ()
		self.genotypes = self.sorted_pop ()

		scores = [gene.score for gene in self.genotypes]
		print 'Fitness (' + str (self.epoch_counter) + '): ' + str (max (scores)) + ', avg: ' + str (1.0 * sum(scores)/len(scores))
		self.epoch_counter += 1

	def make_new_pop (self):
		keep = int (self.population * self.percent_pop_kept)
		new_genotypes = self.genotypes [0:keep]

		self.score_total = None
		for a in range (self.population - keep):
			gene1, gene2 = self.rouletteSelection ()
			new_genotypes += [gene1.mate (gene2)]

		return new_genotypes

	def sorted_pop (self):
		return sorted (self.genotypes, key=lambda x: -x.score)

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

	def alpha (self):
		self.genotypes = sorted (self.genotypes, key=lambda x: -x.score)
		return self.genotypes [0].genes 

	def create_genotype (self):
		raise NotImplemented ()

	def __str__ (self):
		r = ''
		for gene in self.genotypes:
			r += str (gene.score) + '\n'
		return r


def threadable_mate_genes (gene1, gene2):
	return gene1.mate (gene2)

class ThreadedBaseGeneticAlgorithm (BaseGeneticAlgorithm):
	cores = multiprocessing.cpu_count ()

	def make_new_pop (self):
		pool = multiprocessing.Pool (processes=cores)

		keep = int (self.population * self.percent_pop_kept)
		new_genotypes = self.genotypes [0:keep]

		self.score_total = None
		results = []
		for a in range (self.population - keep):
			gene1, gene2 = self.rouletteSelection ()
			results += [pool.apply_async (threadable_mate_genes, args=(gene1, gene2,))]

		new_genotypes += [r.get () for r in results]
		return new_genotypes
