import time
from project.thread_pool import ThreadPool


def test_thread_pool_execution():
    pool = ThreadPool(3) 

    def sample_task():
        time.sleep(0.1)
        return 42

    results = []

    def callback(result):
        results.append(result)

    pool.enqueue(sample_task, callback)
    time.sleep(0.2)
    pool.dispose()

    assert results == [42]


def test_thread_pool_thread_count():
    num_threads = 5
    pool = ThreadPool(num_threads)
    assert len(pool.threads) == num_threads
    pool.dispose()


def test_thread_pool_dispose():
    pool = ThreadPool(2)
    pool.dispose()
    assert pool.shutdown_flag.is_set()
