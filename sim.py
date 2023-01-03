
import numpy as np
import sys

class Simulation:

    def __init__(self, total_time, num_servers, forwarding_prob_arr, _lambda, queue_max_size_arr, service_rate_arr):
        self.total_time = total_time
        self.num_servers = num_servers
        self.forwarding_prob_arr = forwarding_prob_arr
        self._lambda = _lambda
        self.queue_max_size_arr = queue_max_size_arr
        self.service_rate_arr = service_rate_arr

        self.clock = 0.0
        self.next_arrival_time = self.generate_next_arrival();
        self.server_next_done_time = [float('inf')] * num_servers
        self.server_curr_queue_size = [0] * num_servers
        self.num_in_system = 0
        self.num_waiting = 0
        self.total_waittime = 0
        self.total_servicetime = 0
        self.done = False

        self.total_requests = 0
        self.num_dropped = 0
        self.endtime = None
        self.average_waittime = None # only for requests that were not dropped
        self.average_servicetime = None # this includes wait and handle time

    def advance_time(self):
        if (self.done):
            return
        next_event_time = 0
        if (self.server_next_done_time[i] == float('inf') for i in range(num_servers)):
            next_event_time = self.next_arrival_time
            print("1",next_event_time)
        else:
            next_event_time = min(self.next_arrival_time, min(self.server_next_done_time))
            print("2", next_event_time)
        self.total_servicetime += self.num_in_system * (next_event_time - self.clock)
        self.total_waittime += self.num_waiting * (next_event_time - self.clock)
        self.clock = next_event_time
        if (next_event_time < self.total_time):
            if (self.next_arrival_time == next_event_time):
                self.handle_arrival_event()
        for i in range(num_servers):
            if (self.server_next_done_time[i] == next_event_time):
                self.server_curr_queue_size[i] -= 1
                self.num_in_system -= 1
                self.num_waiting -= 1
                if (self.server_curr_queue_size[i] > 0):
                    self.server_next_done_time[i] = self.generate_service_time()
                else:
                    self.server_next_done_time[i] = float('inf')
        if (self.clock >= self.total_time):
            if (self.server_curr_queue_size[i] == 0 for i in range(self.num_servers)):
                self.endtime = self.clock 
                self.average_waittime = self.total_waittime/(self.total_requests-self.dropped)
                self.average_servicetime = self.total_servicetime/(self.total_requests-self.dropped)
                self.done = True

    def handle_arrival_event(self):
        self.total_requests += 1
        chosen_server = np.random.choice(num_servers, p=forwarding_prob_arr)  
        if (self.queue_max_size_arr[chosen_server] + 1 == self.server_curr_queue_size[chosen_server]):
            self.num_dropped += 1
        else:
            self.server_curr_queue_size[chosen_server] += 1
            self.num_in_system += 1
            if (self.server_curr_queue_size[chosen_server] == 1):
                self.server_next_done_time[chosen_server] = self.generate_service_time(chosen_server) 
            else:
                self.num_waiting += 1
        self.next_arrival_time = self.clock + self.generate_next_arrival()

    def generate_next_arrival(self):
        return np.random.exponential(1.0/_lambda)

    def generate_service_time(self, server_idx):
        service_rate = service_rate_arr[server_idx]
        return np.random.exponential(1.0/service_rate)

    def run(self):
        while (not self.done):
            self.advance_time()

    def print_results(self):
        print(self.total_requests, self.num_dropped, self.endtime, self.average_waittime, self.average_servicetime)



if __name__ == '__main__':
    ########  argument processing  ########
    total_time = float(sys.argv[1])
    num_servers = int(sys.argv[2])
    forwarding_prob_arr = [None] * num_servers
    for i in range(num_servers):
        forwarding_prob_arr[i] = float(sys.argv[3+i])
    lambda_index = 3 + num_servers
    _lambda = float(sys.argv[lambda_index])
    queue_max_size_arr = [None] * num_servers
    for i in range(num_servers):
        queue_max_size_arr[i] = int(sys.argv[lambda_index+i+1])
    service_rate_arr = [None] * num_servers
    first_service_rate_index = lambda_index+num_servers+1
    for i in range(num_servers):
        service_rate_arr[i] = float(sys.argv[first_service_rate_index+i])
    ########  initializing simulation  ########
    s = Simulation(total_time, num_servers, forwarding_prob_arr, _lambda, queue_max_size_arr, service_rate_arr) 
    s.run()
    s.print_results()
