from collections import deque

from threading import Thread, Lock
from typing import Any, Callable

from batch_processor.processing_conditions import ProcessingCondition


class BatchProcessor:
    '''
    This class is used to store data in batches.
    Whenever the queue reaches a certain condation, specified by the user, 
    the data is sent to a storage function also provided by the user.

    The storage function is checked wihin a queue mutex, so that in case of
    multiple threads, there are no conflicts.

    The storage function is ran in a separate thread, as to not block the 
    execution of the main thread.
    '''
    def __init__(
        self,
        processing_function: Callable[[list[Any]], None],
        processing_condition: ProcessingCondition
    ) -> None:
        self.data_batch = deque()
        self.mutex = Lock()

        self.processing_function = processing_function
        self.processing_condition = processing_condition

    def put(self, item: Any) -> None:
        '''
        This method is used to put data in the queue.
        '''
        with self.mutex:
            self.processing_condition.on_put(item)
            self._put(item)

            if self.processing_condition.is_full():
                thread = Thread(
                    target=self.processing_function,
                    args=(self._get_all(),)
                )
                thread.start()

    def _get_all(self) -> list[Any]:
        '''
        This method is used to get all the data from the queue.
        '''
        items = []

        while True:
            try:
                items.append(self._get())
            except IndexError:
                break

        self.processing_condition.on_get_all()

        return items

    def close(self) -> None:
        '''
        This method is used to close the queue and send all the remaining data
        '''
        with self.mutex:
            items = self._get_all()
            self.processing_condition.on_get_all()

            if items:
                self.processing_function(items)

            self.data_batch = None

    # Put a new item in the queue
    def _put(self, item):
        self.data_batch.append(item)

    # Get an item from the queue
    def _get(self):
        return self.data_batch.popleft()
