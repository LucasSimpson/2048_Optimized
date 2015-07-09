from GeneticAlgorithm import BaseGeneticAlgorithm, ThreadedBaseGeneticAlgorithm
from NeuralNetwork import NeuralNetwork
from Genotype import BaseGenotype
from Game2048 import Game

import random, math

LAYERS = [5 * 16, 1024, 2]

def trans(x):
	if x == 0: 
		return [0] * 5
	bit = []
	while x:
		bit.append(x % 2)
		x >>= 1

	if len (bit) < 5:
		return [0] * (5 - len (bit)) + bit
	elif len (bit) > 5:
		return bit [-5:]
	else:
		return bit

def play_game (neuralNetwork, visual=False):
	game2048 = Game ()
	moves = [['a', 's'], ['d', 'w']]

	while (not game2048.is_stale ()):
		state = game2048.get_state ()

		inputs = []
		for num in state:
			val = 0 if num == 0 else math.log (num, 2)
			inputs += trans (int (val))

		outputs = neuralNetwork.eval (inputs)
		game2048.process_move (moves [outputs [0]] [outputs [1]], visual)

	return game2048.score

class Genotype2048 (BaseGenotype):
	size = NeuralNetwork.gene_length_from_layers (LAYERS)
	mutation = 5000 # 1 in *mutation*
	games = 5

	def get_fitness_score (self, genotype):
		nn = NeuralNetwork (LAYERS)
		nn.build_from_array (genotype)
		return 1.0 * sum ([play_game (nn) for a in range (self.games)]) / self.games

	def random_gene (self):
		return random.random () * 2 - 1



class GeneticAlgorithm2048 (ThreadedBaseGeneticAlgorithm):
	percent_pop_kept = 0.08

	def create_genotype (self):
		return Genotype2048 ()


ga = GeneticAlgorithm2048 (1000)

for a in range (100):
	ga.epoch ()

genotype = ga.alpha ()
nn = NeuralNetwork (LAYERS)
nn.build_from_array (genotype)

play_game (nn, visual=True)
