### [netdev](https://github.com/selfuryon/netdev)


```
$ time python 2_pyneng_async_example.py

real    0m1.287s
user    0m0.648s
sys     0m0.052s

$ time python 2a_pyneng_sync_example.py

real    0m21.298s
user    0m0.656s
sys     0m0.148s


$ time python 2b_pyneng_concurrent_futures_example.py

real    0m7.650s
user    0m0.640s
sys     0m0.156s
```
