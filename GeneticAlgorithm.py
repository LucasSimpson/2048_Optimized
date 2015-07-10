import random, multiprocessing, numpy

cores = multiprocessing.cpu_count ()


class BaseGeneticAlgorithm (object):
	percent_pop_kept = 0.05

	form_r = '{:>15}'
	form_l = '{:<15}'

	def __init__ (self, population, filename=None):
		if filename:
			pass # load from file
		else:
			self.epoch_counter = 0
			self.population = population
			self.genotypes = []
			for a in range (population):
				genotype = self.create_genotype ()
				self.genotypes += [genotype]
		
		self.genotypes = self.sorted_pop ()
		self.print_start_table ()

	def save_to_file (self, filename):
		# save to file
		# - epoch counter
		# - population
		# - all genotypes
		pass

	def epoch (self, new_pop=None):
		if new_pop:
			self.population = new_pop
			self.genotypes = self.sorted_pop ()

		self.genotypes = self.make_new_pop ()
		self.genotypes = self.sorted_pop ()

		self.print_epoch_stats ()
		
		self.epoch_counter += 1

	def make_new_pop (self):
		keep = int (self.population * self.percent_pop_kept)
		new_genotypes = self.genotypes [0:keep]

		for gene in new_genotypes:
			gene.eval_score ()

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

	def print_epoch_stats (self):
		scores = [gene.score for gene in self.genotypes]
		best = str (max (scores))
		mean = str (numpy.mean (numpy.array (scores)))
		std = str (numpy.std (numpy.array (scores)))
		print self.form_l.format (self.epoch_counter) + self.form_l.format (best) + self.form_l.format (mean) + self.form_l.format (std)

	def print_start_table (self):
		print self.form_l.format ('Generation') + self.form_l.format ('Fitness') + self.form_l.format ('Mean') + self.form_l.format ('Standard deviation')

	def __str__ (self):
		r = ''
		for gene in self.genotypes:
			r += str (gene.score) + '\n'
		return r


def threadable_mate_genes (gene1, gene2):
	return gene1.mate (gene2)

def threadable_create_genotype (geneticAlgorithm):
	return geneticAlgorithm.create_genotype ()

class ThreadedBaseGeneticAlgorithm (BaseGeneticAlgorithm):
	cores = multiprocessing.cpu_count () - 1

	def __init__ (self, population, filename=None):
		if filename:
			pass # load from file
		else:
			pool = multiprocessing.Pool (processes=cores)

			self.epoch_counter = 0
			self.population = population
			self.genotypes = []
			results = []
			for a in range (population):
				results += [pool.apply_async (threadable_create_genotype, args=(self,))]
			
			self.genotypes += [r.get () for r in results]

			pool.close ()
			pool.join ()
		
		self.genotypes = self.sorted_pop ()
		self.print_start_table ()

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

		pool.close ()
		pool.join ()
    	
		return new_genotypes
