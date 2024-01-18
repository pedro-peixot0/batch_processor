# batch_storage_queue #

A multi-producer queue for processing data in batches. 
It is designed in a way that the user can set the method that triggers the processing of the data and the method that processes the data.

## Installation ##

Install directly via github

```
pip install git+https://www.github.com/pedro_amad0/batch_processor@main  # replace @main with @branchname for other branches
```

## Usage ##

### easy ###

You can use the `BatchProcessor` class to create a batch processor that will process the data in batches; when to process the data is set by the `processing_condition` parameter. The `processing_condition` parameter must be an instance of a class that inherits from `ProcessingCondition`.

In the example below, the `processing_condition` is set to `OnMaxBatchSize(10)`, which means that the data will be processed when the batch size reaches 10 items.

```python
from typing import Any
from batch_processor import BatchProcessor
from batch_processor.processing_conditions import OnMaxBatchSize


def processing_function (items: list[Any]):
    # do something with items
    print(f"processed the following items: {items}", flush=True)

# create the batch processor
# it only receives 2 inputs: the processing function and the processing condition
batch_processor = BatchProcessor(
    processing_function=processing_function,
    processing_condition=OnMaxBatchSize(10) 
)

for i in range(20):
    batch_processor.put(i)

batch_processor.close()
```
<br>

### advanced ###

You can also create your own batch processor by inheriting from `BatchProcessor` and overriding all abstractmethods. 
The code bellow is an example of that:

```python
from uuid import uuid4
import pandas as pd

from batch_processor import BatchProcessor
from batch_processor.processing_conditions import ProcessingCondition

# create a custom processing condition
class OnMaxNumberOfLines(ProcessingCondition):
    def __init__(self, max_number_of_lines: int):
        self._number_of_lines = 0
        self._max_number_of_lines = max_number_of_lines
    
    def is_full(self) -> bool:
        return self._number_of_lines >= self._max_number_of_lines
    
    def on_put(self, item: pd.DataFrame) -> None:
        # restrict the item type to pd.DataFrame
        if not isinstance(item, pd.DataFrame):
            raise TypeError("Item must be a DataFrame")

        self._number_of_lines += len(item)

    def on_get_all(self) -> None:
        self._number_of_lines = 0

# create a processing function that saves the items as csv
def save_csv(items: list[pd.DataFrame]):
    pd.concat(items).to_csv(f"{str(uuid4())}.csv")
    print(f"saved items as csv", flush=True)

# assign the processing function and the custom processing condition to a BatchProcessor
batch_processor = BatchProcessor(
    processing_function=save_csv,
    processing_condition=OnMaxNumberOfLines(10) # save when queue size is 100MB
)

# put some dataframes into the batch processor
test_df = pd.DataFrame({f"col{i}": f"{i}"*1000 for i in range(3)}, index=[0]) 

for i in range(100):
    batch_processor.put(test_df)

# close the batch processor
batch_processor.close()
```