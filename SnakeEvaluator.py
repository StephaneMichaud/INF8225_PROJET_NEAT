from functools import reduce
from itertools import product

import gym
import gym_snake
import numpy as np


# https://github.com/grantsrb/Gym-Snake


class SnakeEvaluator:
    def __init__(self):
        self.env = gym.make('snake-v0')
        self.INCREMENT_COMBINATIONS = list(product([0,-1,1],[0,-1,1]))
        self.INCREMENT_COMBINATIONS.pop(0)
        self.initialize_attributes()

    def get_unit_type(self,color):
        if self.equal_colors(color,self.BODY_COLOR):
            return 0
        if self.equal_colors(color,self.HEAD_COLOR):
            return 2
        if self.equal_colors(color,self.FOOD_COLOR):
            return 1
        if self.equal_colors(color,self.SPACE_COLOR):
            return 3
        
        return 3

    def initialize_attributes(self):
        self.env.reset()  # Constructs an instance of the game
        self.game_controller = self.env.controller
        self.snake = self.game_controller.snakes[0]
        self.BODY_COLOR = self.game_controller.grid.BODY_COLOR
        self.HEAD_COLOR = self.game_controller.grid.HEAD_COLOR
        self.FOOD_COLOR = self.game_controller.grid.FOOD_COLOR
        self.SPACE_COLOR = self.game_controller.grid.SPACE_COLOR
        self.GRID_SIZE_X = self.game_controller.grid.grid_size[0]
        self.GRID_SIZE_Y = self.game_controller.grid.grid_size[1]
        self.ACTIONS = [self.snake.UP, self.snake.RIGHT,
                        self.snake.DOWN, self.snake.LEFT]
        self.NB_ACTIONS = len(self.ACTIONS)


    def get_nb_inputs_nn(self):
        return 3*8+1



    def get_nb_outputs_nn(self):
        return self.NB_ACTIONS



    def convert_nn_output_to_action(self, nn_output):
        return self.ACTIONS[np.argmax(nn_output)]

    def equal_colors(self, color_a, color_b):
        return reduce(lambda x, y: x and y, map(lambda p, q: p == q, color_a, color_b), True)

    def get_unit_color(self, grid_object, offset_x, offset_y):
        return grid_object.grid[int(offset_x)+int(self.env.unit_size/2)][int(offset_y)+int(self.env.unit_size/2)]
        # for x in range(0, self.env.unit_size):
        #     for y in range(0, self.env.unit_size):
        #         current_pixel_color = grid_object.grid[x+offset_x, y+offset_y]
        #         if self.equal_colors(self.BODY_COLOR, current_pixel_color):
        #             return 2
        #         elif self.equal_colors(self.HEAD_COLOR, current_pixel_color):
        #             return 3
        #         elif self.equal_colors(self.FOOD_COLOR, current_pixel_color):
        #             return 4
        #         elif self.equal_colors(self.BODY_COLOR, current_pixel_color):
        #             return 5
        #         else:
        #             continue

        # if it gets here without returning, it means every pixel was of the color of the background
        # return 0

    def calculate_distance_activation(self, snake_head_position, increment_x, increment_y):
        distance = 0.0
        total_distance = 0.0
        if increment_x != 0:
            total_distance += self.GRID_SIZE_X
            if increment_x == -1:
                distance += snake_head_position[0]
            else:
                distance += self.GRID_SIZE_X - snake_head_position[0]

        if increment_y != 0:
            total_distance += self.GRID_SIZE_Y
            if increment_y == -1:
                distance += snake_head_position[1]
            else:
                distance += self.GRID_SIZE_Y - snake_head_position[1]
        
        return distance/total_distance

    def detector(self, grid_object, snake_head_position, increment_x, increment_y):
        position = snake_head_position.copy()

        cpt = 0
        while True:
            cpt+=1
            position[0] += increment_x*self.env.unit_size
            position[1] += increment_y*self.env.unit_size
            
            in_bounds = position[0] >= 0 and position[1] >= 0 and position[0] < self.GRID_SIZE_X and position[1] <= self.GRID_SIZE_Y
            if in_bounds:
                unit_color = self.get_unit_color(grid_object, position[0], position[1])
                if self.equal_colors(self.SPACE_COLOR,unit_color):
                    continue
                else:
                    output = [0, 0, 0]
                    output[self.get_unit_type(unit_color)] = (abs(increment_x)+abs(increment_y))*cpt\
                        /float(self.GRID_SIZE_X*abs(increment_x)+self.GRID_SIZE_Y*abs(increment_y))

                            
                    output[2] = self.calculate_distance_activation(snake_head_position, increment_x, increment_y)

                    return output
            else:
                break
        
        return [0,0,self.calculate_distance_activation(snake_head_position, increment_x, increment_y)]

    def prepare_to_input(self, grid_object, snake_head_position):
        nn_input = [1]

        for increment in self.INCREMENT_COMBINATIONS:
            increment_x, increment_y = increment
            nn_input += self.detector(grid_object,snake_head_position,increment_x,increment_y)

        # for x in range(0, grid_object.grid_size[0]):
        #     for y in range(0, grid_object.grid_size[1]):
        #         nn_input.append(self.get_unit_type(
        #             grid_object, x*self.env.unit_size, y*self.env.unit_size))
        return nn_input

    def get_snake_default_fitness(self):
        return self.GRID_SIZE_X*self.GRID_SIZE_Y

    def adjust_fitness(self, genome, reward, total_time_steps):
        genome.fitness += self.get_snake_default_fitness()*reward
        genome.fitness -= 1  # penalty for time passing

    def evaluate_genomes(self, current_population):
        '''Evaluates the current population'''

        for genome in current_population:
            self.initialize_attributes()
            genome.fitness = self.get_snake_default_fitness()
            total_time_steps = 0
            is_snake_alive = True
            while is_snake_alive:
                nn_input = self.prepare_to_input(self.game_controller.grid, self.snake.head)
                nn_output = genome.feed_forward(nn_input)
                action = self.convert_nn_output_to_action(nn_output)

                state = self.env.step(action)
                self.env.render()
                reward = state[1]  # index for reward

                self.adjust_fitness(genome, reward, total_time_steps)

                is_snake_alive = state[3]['snakes_remaining'] == 1
                total_time_steps += 1
