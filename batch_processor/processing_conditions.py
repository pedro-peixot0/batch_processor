from typing import Any
from abc import ABC, abstractmethod


class ProcessingCondition(ABC):
    '''
    This class is used by the `BatchProcessor` to decide when to call the `processing_function`.
    '''
    @abstractmethod
    def __init__(self):
        ''''
        This method is used to initialize the condition.
        
        It should receive all the parameters needed.
        '''

    @abstractmethod
    def is_full(self) -> bool:
        '''
        This method is used to check if the queue is full.
        It is called every time an item is put in the queue.
       
        You don't need to worry about thread safety, this 
        function is called inside a mutex.
        
        It should return True if the queue is full, False otherwise.

        A True value means that the `processing_function` will be called
        '''

    @abstractmethod
    def on_put(self, item: Any) -> None:
        ''''
        This method is called when an item is put in the queue.

        You don't need to worry about thread safety, this
        function is called inside a mutex.

        It is useful to update the internal state of the condition.
        '''

    @abstractmethod
    def on_get_all(self) -> None:
        ''''
        This method is called when all the items are taken from the queue.
        
        You don't need to worry about thread safety, this
        function is called inside a mutex.

        It is useful to update the internal state of the condition.
        '''

class OnMaxBatchSize(ProcessingCondition):
    def __init__(self, max_queue_size: int):
        super().__init__()
        self.max_queue_size = max_queue_size
        self.current_queue_size = 0

    def is_full(self) -> bool:
        return self.current_queue_size >= self.max_queue_size

    def on_put(self, item: Any) -> None:
        self.current_queue_size += 1

    def on_get_all(self) -> None:
        self.current_queue_size = 0
