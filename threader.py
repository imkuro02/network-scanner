from threading import Thread
from time import sleep

class Run_threads:
    def __init__(self,threads,num_range,numbers = []):
        self.threads = threads
        self.num_range = num_range
        self.numbers = numbers

    def generate_number(self,thread_index):
        print('im thread ',thread_index)
        my_numbers = (list(range(
            thread_index,
            self.num_range,
            self.threads)))
        for n in my_numbers:
            self.numbers.append(n)
        #print(thread_index,'<=thread',self.threads,self.num_range)
        
    def run(self):
        created_threads = []
        for index, thread in enumerate(range(self.threads),start=0):
            t = Thread(target=self.generate_number,args=(index,))
            t.start()
            created_threads.append(t)

        for thread in created_threads:
            thread.join()
            
        

a = Run_threads(4,100_000_00)
a.run()
#print(sorted(a.numbers))
                    
