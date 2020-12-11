import json
import random
import math
from single_byte_xor import SingleByteXorAttacker


ALPHABET = bytearray('abcdefghijklmnopqrstuvwxyz'.encode())
with open('./bigrams_percentages.json') as bigrams:
    TWO_LETTER_FREQUENCES = json.load(bigrams)
with open('./trigrams_percentages.json') as trigrams:
    THREE_LETTER_FREQUENCES = json.load(trigrams)


class Substitution:
    def __init__(self, alphabet: bytearray):
        self.alphabet = alphabet

    def encrypt(self, text_b: bytearray, keys_b: list):
        text_b = text_b[:]
        for i in range(len(text_b)):
            key_b = keys_b[i % len(keys_b)]
            try:
                alphabet_index = self.alphabet.index(text_b[i])
                text_b[i] = key_b[alphabet_index]
            except ValueError:
                continue
        return text_b

    def decrypt(self, encrypted_text_b: bytearray, keys_b: list):
        encrypted_text_b = encrypted_text_b[:]
        for i in range(len(encrypted_text_b)):
            key_b = keys_b[i % len(keys_b)]
            try:
                key_index = key_b.index(encrypted_text_b[i])
                encrypted_text_b[i] = self.alphabet[key_index]
            except ValueError:
                continue
        return encrypted_text_b


class Individual:
    def __init__(self, key: bytearray):
        self.key = bytearray(key.decode().lower().encode())


class IndividualSet(list):
    ONE_LETTER_FITTING_COEFFICIENT = 1.5
    TWO_LETTERS_FITTING_COEFFICIENT = 9
    THREE_LETTERS_FITTING_COEFFICIENT = 125     # 123

    fitness = None

    def __init__(self, _type, *args):
        self._type = _type
        super(IndividualSet, self).__init__(*args)

    def __repr__(self):
        return f"IndividualSet {[ind.key for ind in self]}"

    def __eq__(self, other):
        if isinstance(other, IndividualSet):
            return super(IndividualSet, self).__eq__(other)
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.__repr__())

    def append(self, item):
        if not isinstance(item, self._type):
            raise TypeError(f'item is not of type {self._type}')
        super(IndividualSet, self).append(item)

    def calc_fitness(self, encrypted_text_b: bytearray):
        keys_b = [ind.key for ind in self]
        substitution = Substitution(ALPHABET)
        decrypted_text_b = substitution.decrypt(encrypted_text_b, keys_b)
        fitness_1 = self.ONE_LETTER_FITTING_COEFFICIENT * SingleByteXorAttacker.get_fitting_coefficient(decrypted_text_b)
        fitness_2 = self.TWO_LETTERS_FITTING_COEFFICIENT * self.calc_fitting_coefficient(decrypted_text_b, TWO_LETTER_FREQUENCES)
        fitness_3 = self.THREE_LETTERS_FITTING_COEFFICIENT * self.calc_fitting_coefficient(decrypted_text_b, THREE_LETTER_FREQUENCES)
        deviation = abs(fitness_1 - fitness_2) / 3 + abs(fitness_2 - fitness_3) / 3 + abs(fitness_1 - fitness_3) / 3
        # print(fitness_1)
        # print(fitness_2)
        # print(fitness_3)
        # print(deviation)
        self.fitness = (fitness_1 + fitness_2 + fitness_3 + deviation)
        return self.fitness

    def calc_fitting_coefficient(self, decrypted_text_b, n_grams: dict):
        deviation_sum = 0

        for key, frequency in n_grams.items():
            search_index = 0
            number_of_matches = 0

            while True:
                try:
                    search_index = decrypted_text_b.index(key.encode(), search_index) + 1
                    number_of_matches += 1
                except ValueError:
                    break

            n_gram_frequency = number_of_matches * 100 / (len(decrypted_text_b) - len(key) + 1)
            deviation_sum += abs(n_gram_frequency - frequency)

        return deviation_sum / len(n_grams)


class SubstitutionAttacker:
    def __init__(self,
                 individual_set_members_count=1,
                 min_population_size=50,
                 max_population_size=100,
                 iterations_count=1000,
                 mutations_percentage=0.1,
                 best_percentage=30):
        self.individual_set_members_count = individual_set_members_count
        self.min_population_size = min_population_size
        self.max_population_size = max_population_size
        self.iterations_count = iterations_count
        self.mutations_percentage = mutations_percentage
        self.best_percentage = best_percentage

    def attack(self, encrypted_text):
        encrypted_text_b = bytearray(encrypted_text.lower().encode())
        best_population = self.evaluate(encrypted_text_b)
        print("======Best matches======")
        substitution = Substitution(ALPHABET)
        for ind_set in best_population:
            keys_b = [ind.key for ind in ind_set]
            print(f"Possible keys: {ind_set}")
            print(f"Decrypted text: {substitution.decrypt(encrypted_text_b, keys_b)}")

    def generate_population(self, size):
        population = set()

        for i in range(0, size):
            individual_set = IndividualSet(Individual)
            for j in range(0, self.individual_set_members_count):
                key = ALPHABET[:]
                random.shuffle(key)
                individual = Individual(key)
                individual_set.append(individual)
            population.add(individual_set)
        return population

    def evaluate(self, encrypted_text_b):
        population = list(self.generate_population(self.max_population_size))
        for p in population:
            p.calc_fitness(encrypted_text_b)

        for i in range(0, self.iterations_count):
            print(f"Iteration: {i}")
            ordered_population = sorted(population, key=lambda ind_set: ind_set.fitness)
            best_count = math.floor(len(ordered_population) * self.best_percentage / 100)
            best_population = ordered_population[0:best_count]
            print(f"Best keys: {best_population[0]}")
            print(f"Best fitness: {best_population[0].fitness}")
            population = best_population

            while len(population) < self.min_population_size:
                first_set, second_set = self.crossover(random.choice(population), random.choice(population))
                first_set.calc_fitness(encrypted_text_b)
                second_set.calc_fitness(encrypted_text_b)
                population.append(first_set)
                population.append(second_set)

            population = list(set(population))
        return population

    def crossover(self, first_set: IndividualSet, second_set: IndividualSet):
        first_child_set = IndividualSet(Individual)
        second_child_set = IndividualSet(Individual)

        for i in range(0, self.individual_set_members_count):
            first_set_key = first_set[i].key[:]
            second_set_key = second_set[i].key[:]
            first_child_key = ALPHABET[:]
            second_child_key = ALPHABET[:]

            positions = [(i, random.randrange(0, 2)) for i in range(0, len(ALPHABET))]

            for index, indicator in positions:
                if indicator == 0:
                    first_child_key[index] = first_set[i].key[index]
                    second_set_key.remove(first_set[i].key[index])
                else:
                    second_child_key[index] = second_set[i].key[index]
                    first_set_key.remove(second_set[i].key[index])

            for index, indicator in positions:
                if indicator == 0:
                    second_child_key[index] = first_set_key[0]
                    first_set_key.pop(0)
                else:
                    first_child_key[index] = second_set_key[0]
                    second_set_key.pop(0)

            needs_mutation = random.random() < self.mutations_percentage
            while needs_mutation:
                random_pos = random.randrange(1, len(ALPHABET))
                first_letter_index = random.randrange(0, random_pos)
                second_letter_index = random.randrange(random_pos, len(ALPHABET))
                first_child_key[first_letter_index], first_child_key[second_letter_index] = first_child_key[second_letter_index], first_child_key[first_letter_index]
                needs_mutation = random.random() < self.mutations_percentage

            needs_mutation = random.random() < self.mutations_percentage
            while needs_mutation:
                random_pos = random.randrange(1, len(ALPHABET))
                first_letter_index = random.randrange(0, random_pos)
                second_letter_index = random.randrange(random_pos, len(ALPHABET))
                second_child_key[first_letter_index], second_child_key[second_letter_index] = second_child_key[second_letter_index], second_child_key[first_letter_index]
                needs_mutation = random.random() < self.mutations_percentage

            first_child_set.append(Individual(first_child_key))
            second_child_set.append(Individual(second_child_key))

        return first_child_set, second_child_set

