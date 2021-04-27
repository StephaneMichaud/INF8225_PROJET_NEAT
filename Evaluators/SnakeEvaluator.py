from functools import reduce
from itertools import product
from copy import deepcopy

import gym
from sneks.envs.snek import SingleSnek
import numpy as np
import math


# https://github.com/grantsrb/Gym-Snake


class SnakeEvaluator:
    def __init__(self):
        self.env = SingleSnek(size=(16,16), step_limit=math.inf, dynamic_step_limit=1000, obs_type='raw', n_food=1, die_on_eat=False, render_zoom=20, add_walls=False)
        self.grid_size = [16,16]
        self.INCREMENT_COMBINATIONS = list(product([0,-1,1],[0,-1,1]))
        self.INCREMENT_COMBINATIONS.pop(0)
        self.initialize_attributes()
        self.ACTIONS = [0,1,2,3]
        self.NB_ACTIONS =4
        self.FOOD_ID = 64
        self.HEAD_ID = 101
        self.BODY_ID = 100
        self.VOID_ID = 0

    def initialize_attributes(self):
        self.env.reset()  # Constructs an instance of the game

    def get_nb_inputs_nn(self):
        return 2*8+1

    def get_nb_outputs_nn(self):
        return self.NB_ACTIONS

    def convert_nn_output_to_action(self, nn_output):
        return self.ACTIONS[np.argmax(nn_output)]

    def in_bound(self, y, x):
        return x>= 0 and x<  self.grid_size[1] and y>=0 and y <  self.grid_size[0]

    def get_output_index(self, case_id):
        return  0 if case_id == self.FOOD_ID else 1

    def get_bound_distance(self, y, x, inc_y, inc_x):
        if inc_y == inc_x == 0:
            return 0
        
        distance_x = 0.0
        distance_y = 0.0
        if inc_y != 0:
            distance_y += y if inc_y == -1 else self.grid_size[0] - y
        if inc_x != 0:
            distance_x += x if inc_x == -1 else self.grid_size[1] - x


        return math.sqrt((distance_y)**2 + (distance_x)**2) / math.sqrt(self.grid_size[0]**2 + self.grid_size[1]**2)

    def get_cases_distance(self, y_a, x_a, y_b, x_b):
        return math.sqrt((y_a - y_b)**2 + (x_a - x_b)**2) / math.sqrt(self.grid_size[0]**2 + self.grid_size[1]**2)


    def detector(self, state, head_pos, inc_y, inc_x):
        position = head_pos.copy()
        cpt = 0
        output = [0, 0]
        while True:
            cpt+=1
            position[0] += inc_y
            position[1] += inc_x

            in_bounds = self.in_bound(position[0], position[1])
            if in_bounds:
                unit_id = state[position[0], position[1]]
                if unit_id == self.VOID_ID:
                    continue
                else:
                    if output[self.get_output_index(unit_id)] == 0:
                        output[self.get_output_index(unit_id)] = self.get_cases_distance(head_pos[0], head_pos[1], position[0], position[1])
            else:
                break
        if output[1] == 0:
            output[1] = self.get_bound_distance(head_pos[0], head_pos[1], inc_y, inc_x)
        return output

    def prepare_to_input(self, state, snake_head_position):
        nn_input = [1]

        for increment in self.INCREMENT_COMBINATIONS:
            increment_x, increment_y = increment
            nn_input += self.detector(state,snake_head_position,increment_x,increment_y)

        return nn_input

    def adjust_fitness(self, genome, reward, head_pos, food_pos, body_size):
        if reward == 1:
            genome.fitness +=  1000 * body_size
        if not food_pos is None and not head_pos is None:
            genome.fitness += body_size - float(body_size)/2 * self.get_cases_distance(head_pos[0], head_pos[1],food_pos[0],food_pos[1])


    def get_case_pos(self, state, id):
        for i in range(0, self.grid_size[0]):
            for j in range(0, self.grid_size[1]):
                if state[i][j] == id:
                    return [i,j]
        return None
                
    def get_food_pos(self, state):
        return self.get_case_pos(state, self.FOOD_ID)

    def get_head_pos(self, state):
        return self.get_case_pos(state, self.HEAD_ID)

    def get_distance_to_food(self, food_pos, head_position):
        return abs(head_position[0]-food_pos[0])+abs(head_position[1]-food_pos[1])+1


    def show_genome(self, genome):
        np.random.seed(genome.generation)
        seed_gens = np.random.randint(1000, size=5)
        for s in seed_gens:
            state = self.env.seed(s)
            state = self.env.reset()
            food_pos = self.get_head_pos(state)
            is_snake_alive = True
            while is_snake_alive:
                self.env.render()
                nn_input = self.prepare_to_input(state, self.get_head_pos(state))
                nn_output = genome.feed_forward(nn_input)
                action = self.convert_nn_output_to_action(nn_output)
                state, reward, done, _ = self.env.step(action)
                is_snake_alive = not done
        self.env.close()

    def evaluate_genomes(self, current_population):
        '''Evaluates the current population'''
        best_gen = None

        
        np.random.seed(current_population[0].generation)
        seed_gens = np.random.randint(10000, size=5)
        for genome in current_population:
            for s in seed_gens:
                body_size = 1
                genome.fitness = 0
                state = self.env.seed(s)
                state = self.env.reset()
                food_pos = self.get_head_pos(state)
                is_snake_alive = True
                while is_snake_alive:

                    nn_input = self.prepare_to_input(state, self.get_head_pos(state))
                    nn_output = genome.feed_forward(nn_input)
                    action = self.convert_nn_output_to_action(nn_output)
                    state, reward, done, _ = self.env.step(action)
                    is_snake_alive = not done
                    self.adjust_fitness(genome, reward, self.get_head_pos(state), food_pos, body_size)

                    if reward == 1:
                        body_size+=1
                        food_pos = self.get_head_pos(state)
            genome.fitness = genome.fitness / len(seed_gens)
            if best_gen is None:
                best_gen  = genome
            elif genome.fitness > best_gen.fitness:
                best_gen = genome
            
        
        if best_gen.fitness > 10:
            self.show_genome(best_gen)
                
