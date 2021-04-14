import gym
import gym_snake
from functools import reduce


class SnakeEvaluator:
    def __init__(self):
        self.env = gym.make('snake-v0')
        self.game_controller = self.env.controller
        self.snake = self.game_controller.snakes[0]
        self.BODY_COLOR = self.game_controller.grid.BODY_COLOR
        self.HEAD_COLOR = self.game_controller.grid.HEAD_COLOR
        self.FOOD_COLOR = self.game_controller.grid.FOOD_COLOR
        self.SPACE_COLOR = self.game_controller.grid.SPACE_COLOR
        self.ACTIONS = [self.snake.UP, self.snake.RIGHT, self.snake.DOWN, self.snake.LEFT]
        self.NB_ACTIONS = len(self.ACTIONS)
        
        self.CONTROL_RANGES = [i/(float(self.NB_ACTIONS)-1) for i in range(0, self.NB_ACTIONS+1)]



    def convert_nn_output_to_action(self, nn_output):
        nn_output = nn_output[0]
        for i in range(0, self.NB_ACTIONS):
            if nn_output > self.CONTROL_RANGES[i] and nn_output < self.CONTROL_RANGES[i+1]:
                return self.ACTIONS[i]

        raise Exception()



    def equal_colors(self, color_a, color_b):
        return reduce(lambda x, y: x and y, map(lambda p, q: p == q, color_a, color_b), True)



    def get_unit_type(self, grid_object, offset_x, offset_y):
        
        for x in range(0, self.env.unit_size):
            for y in range(0, self.env.unit_size):
                current_pixel_color = grid_object.grid.grid_pixels[x+offset_x, y+offset_y]
                if self.equal_colors(self.BODY_COLOR, current_pixel_color):
                    return 2
                elif self.equal_colors(self.HEAD_COLOR, current_pixel_color):
                    return 3
                elif self.equal_colors(self.FOOD_COLOR, current_pixel_color):
                    return 4
                elif self.equal_colors(self.BODY_COLOR, current_pixel_color):
                    return 5
                else:
                    continue
        
        # if it gets here without returning, it means every pixel was of the color of the background
        return 0
    


    def convert_grid_to_input(self, grid_object):
        nn_input = [ 1 ]
        for x in range(0, grid_object.grid_size[0]):
            for y in range(0, grid_object.grid_size[1]):
                nn_input.append(self.get_unit_type(grid_object, x*self.env.unit_size, y*self.env.unit_size))

        return nn_input



    def snake_alive(self):
        return self.snake != None


    def get_snake_default_fitness(self):
        return self.game_controller.grid.grid_size[0]*self.game_controller.grid.grid_size[1]

    
    def adjust_fitness(self, genome, reward, total_time_steps):
        genome += self.get_snake_default_fitness()*reward
        genome -= 1 # penalty for time passing


    def evaluate_genomes(self, current_population):
        '''Evaluates the current population'''

        for genome in current_population:
            observation = self.env.reset() # Constructs an instance of the game
            genome.fitness = self.get_snake_default_fitness()
            total_time_steps = 0
            while self.snake_alive():
                nn_input = self.convert_grid_to_input(self.game_controller.grid)
                nn_output = genome.feed_forward(nn_input)
                action = self.convert_nn_output_to_action(nn_output)

                reward = observation.step(action)
                self.adjust_fitness(genome, reward, total_time_steps)

                total_time_steps+=1
            
            
                

            
            