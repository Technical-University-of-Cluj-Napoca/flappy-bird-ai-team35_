import random
from bird import Bird

class Species:
    def __init__(self, representative):
        self.representative = representative.brain.copy()
        self.members = []
        self.fitness = 0.0

    def add(self, bird):
        self.members.append(bird)

    def calculate_fitness(self):
        if len(self.members) == 0:
            self.fitness = 0
        else:
            self.fitness = sum(b.fitness for b in self.members) / len(self.members)

    def sort_members(self):
        self.members.sort(key=lambda b: b.fitness, reverse=True)

    def get_champion(self):
        self.sort_members()
        return self.members[0]


class Population:
    def __init__(self, size, species_threshold, mutation_rate=0.1,mutation_strength=0.1):
        self.size = size
        self.species_threshold = species_threshold
        self.mutation_rate = mutation_rate
        self.mutation_strength = mutation_strength

        self.generation = 1
        self.birds = list[Bird] # TODO birds
        self.species = []

    def speciate(birds, threshold):
        species_list = []

        for bird in birds:
            placed = False

            for species in species_list:
                distance = bird.brain.distance(species.representative)

                if distance < threshold:
                    species.add(bird)
                    placed = True
                    break

            if not placed:
                new_species = Species(bird)
                new_species.add(bird)
                species_list.append(new_species)

        for s in species_list:
            s.calculate_fitness()

        return species_list

    def all_dead(self):
        return all(not bird.alive for bird in self.birds)

    def next_generation(self):
        self.species = speciate(self.birds, self.species_threshold)

        self.species.sort(key=lambda s: s.fitness, reverse=True)

        new_birds = []

        for s in self.species:
            champion = s.get_champion().clone()
            new_birds.append(champion)

        while len(new_birds) < self.size:
            species = self.select_species()
            parent = self.select_parent(species)

            child = parent.clone()
            child.brain.mutate(
                mutation_rate=self.mutation_rate,
                mutation_strength=self.mutation_strength
            )

            new_birds.append(child)

        self.birds = new_birds
        self.generation += 1

    def select_species(self):
        total_fitness = sum(s.fitness for s in self.species)

        if total_fitness == 0:
            return random.choice(self.species)

        r = random.uniform(0, total_fitness)
        running_sum = 0

        for s in self.species:
            running_sum += s.fitness
            if running_sum >= r:
                return s

        return self.species[0]

    def select_parent(self, species):
        total_fitness = sum(b.fitness for b in species.members)

        if total_fitness == 0:
            return random.choice(species.members)

        r = random.uniform(0, total_fitness)
        running_sum = 0

        for b in species.members:
            running_sum += b.fitness
            if running_sum >= r:
                return b

        return species.members[0]
