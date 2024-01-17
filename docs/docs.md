# Coroutine, Threading, Multiprocessing

![total.png](images/total.png)

### Multiprocessing is Celery + Celery Queue

### Threading
   * low Performance because of thread switching cost
   * GUL 5ms mechanism

![thread-1.png](images/thread-1.png)

![thread-2.png](images/thread-2.png)

### Coroutine 
    * Runs within a 1 main thread and in event loop, GIL doesn't affect
    * Is cheap to start
    * Is easy to get return value
    * Pre info about blocking function received by yield or await
    * Select as async waiting mechanism 

![coroutine_cycle_code.png](images/coroutine_cycle_code.png)

![coroutine_cycle_1.png](images/coroutine_cycle_1.png)

![coroutine_cycle_2.png](images/coroutine_cycle_2.png)

![coroutine_cycle_3.png](images/coroutine_cycle_3.png)
