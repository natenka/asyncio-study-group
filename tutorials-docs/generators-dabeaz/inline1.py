from concurrent.futures import ThreadPoolExecutor
import time
#from inline1 import Task

class Task:
    def __init__(self, gen):
        self._gen = gen

    def step(self, value=None):
        #Run to the next yield
        try:
            fut = self._gen.send(value)
            #Future returned
            fut.add_done_callback(self._wakeup)
        except StopIteration as exc:
            pass

    def _wakeup(self, fut):
        #handler of results
        result = fut.result()
        self.step(result) #feedback loop (run to the next yield)


pool = ThreadPoolExecutor(8)

def func(x,y):
    time.sleep(10)
    return x+y


def do_func(x,y):
    result = yield pool.submit(func, x,y)
    print('Got:', result)

g = do_func(2,3)
t = Task(g)
t.step()

do_func(1,2)
#returns Future
next(do_func(1,2))

