

Прочитала, что лучше использовать ensure_future вместо create_task:

ensure_future is method to create Task from coroutine. It creates task different ways based on argument (including using of create_task for coroutines and future-like objects).

create_task is abstract method of AbstractEventLoop. Different event loops can implement this function different ways.

[Source](https://stackoverflow.com/questions/36342899/asyncio-ensure-future-vs-baseeventloop-create-task-vs-simple-coroutine)


Another important difference is that in addition to accepting coroutines, ensure_future also accepts any awaitable object; create_task on the other hand just accepts coroutines.
[Source](https://stackoverflow.com/questions/33980086/whats-the-difference-between-loop-create-task-asyncio-async-ensure-future-and).


