import threading
import queue
from typing import Callable, Optional, Any, Tuple, List


class ThreadPool:
    def __init__(self, num_threads: int):
        self.num_threads: int = num_threads
        self.tasks: queue.Queue[Tuple[Callable[[], Any], Optional[Callable[[Any], None]]]] = queue.Queue()
        self.threads: List[threading.Thread] = []
        self.shutdown_flag: threading.Event = threading.Event()

        for _ in range(num_threads):
            thread = threading.Thread(target=self._worker)
            thread.daemon = True
            thread.start()
            self.threads.append(thread)

    def _worker(self) -> None:
        while not self.shutdown_flag.is_set():
            try:
                task, callback = self.tasks.get(timeout=1)  # Таймаут для проверки shutdown_flag
                result = task()
                if callback:
                    callback(result)
                self.tasks.task_done()
            except queue.Empty:
                continue

    def enqueue(self, task: Callable[[], Any], callback: Optional[Callable[[Any], None]] = None) -> None:
        if not self.shutdown_flag.is_set():
            self.tasks.put((task, callback))

    def dispose(self) -> None:
        self.shutdown_flag.set()
        for thread in self.threads:
            thread.join()
