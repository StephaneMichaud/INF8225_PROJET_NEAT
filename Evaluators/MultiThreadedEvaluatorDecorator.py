from threading import Thread

class MultiThreadedEvaluatorDecorator:
    def __init__(self, evaluator, n_workers):
        self.n_workers = n_workers
        self.evaluator = evaluator

    def get_nb_inputs_nn(self):
        return self.evaluator.get_nb_inputs_nn()

    def get_nb_outputs_nn(self):
        return self.evaluator.get_nb_outputs_nn()

    def evaluate_genomes(self, current_population):
        '''Evaluates the current population'''
        n_genomes = len(current_population)
        workers_process = []
        for i in range(0, n_genomes, int(n_genomes/self.n_workers)):
            workers_process.append(
                Thread(
                    target=self._evaluate_genomes_worker, 
                    args=(current_population[i:min(int(i+n_genomes/self.n_workers), n_genomes)], )
                          )
                                    )

        for worker in workers_process:
            worker.start()
        for worker in workers_process:
            worker.join()

    
    def _evaluate_genomes_worker(self, worker_population):
        self.evaluator.evaluate_genomes(worker_population)


