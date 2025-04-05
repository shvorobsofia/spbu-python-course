import threading
import queue
from typing import Callable, Optional, Any, Tuple, List


class ThreadPool:
    """A thread pool for executing tasks asynchronously in multiple threads.

    This class manages a pool of worker threads that process tasks from a queue.
    Tasks are executed in parallel, and an optional callback can be provided to
    handle the result of each task. The thread pool can be safely shut down using
    the `dispose` method.

    Attributes:
        num_threads (int): The number of worker threads in the pool.
        tasks (queue.Queue[Tuple[Callable[[], Any], Optional[Callable[[Any], None]]]]):
            A queue of tasks to be executed, where each task is a tuple of a callable
            and an optional callback.
        threads (List[threading.Thread]): The list of worker threads.
        shutdown_flag (threading.Event): A flag to signal the threads to stop.
    """

    def __init__(self, num_threads: int):
        """Initialize the thread pool with a specified number of worker threads.

        Args:
            num_threads (int): The number of threads to create in the pool. Must be
                a positive integer.

        Raises:
            ValueError: If `num_threads` is less than or equal to 0.
        """
        if num_threads <= 0:
            raise ValueError("Number of threads must be a positive integer")

        self.num_threads: int = num_threads
        self.tasks: queue.Queue[
            Tuple[Callable[[], Any], Optional[Callable[[Any], None]]]
        ] = queue.Queue()
        self.threads: List[threading.Thread] = []
        self.shutdown_flag: threading.Event = threading.Event()

        for _ in range(num_threads):
            thread = threading.Thread(target=self._worker)
            thread.daemon = True
            thread.start()
            self.threads.append(thread)

    def _worker(self) -> None:
        """Worker function that processes tasks from the queue.

        This method runs in each worker thread and continuously retrieves tasks
        from the queue until the shutdown flag is set. Each task is executed, and
        if a callback is provided, it is called with the task's result.

        The method uses a timeout to periodically check the shutdown flag, allowing
        the thread to exit gracefully when the pool is disposed.
        """
        while not self.shutdown_flag.is_set():
            try:
                task, callback = self.tasks.get(
                    timeout=1
                )  # Таймаут для проверки shutdown_flag
                result = task()
                if callback:
                    callback(result)
                self.tasks.task_done()
            except queue.Empty:
                continue

    def enqueue(
        self, task: Callable[[], Any], callback: Optional[Callable[[Any], None]] = None
    ) -> None:
        """Add a task to the queue for execution.

        The task will be executed by one of the worker threads as soon as possible.
        If a callback is provided, it will be called with the result of the task.

        Args:
            task (Callable[[], Any]): A callable that takes no arguments and returns
                a result of any type.
            callback (Optional[Callable[[Any], None]]): An optional callable that
                takes the result of the task as an argument and returns nothing.
                Defaults to None.

        Notes:
            If the thread pool has been disposed (i.e., `dispose` has been called),
            the task will not be enqueued.
        """
        if not self.shutdown_flag.is_set():
            self.tasks.put((task, callback))

    def dispose(self) -> None:
        """Shut down the thread pool and wait for all threads to finish.

        This method sets the shutdown flag, which causes all worker threads to stop
        processing new tasks, and then waits for all threads to complete their current
        tasks and terminate.

        Notes:
            After calling this method, no new tasks can be enqueued. Any tasks still
            in the queue will not be processed.
        """
        self.shutdown_flag.set()
        for thread in self.threads:
            thread.join()
