# Notes for Report

## Data/Features

### sklearn_pandas: `DataFrameMapper`

 - A convenient way to split up features into categorical features vs. continuous features.
 - Attempted to train the model having the source and destination ports as well as the protocol as categorical columns.
 - This, however, failed because we kept running into the problem of new ports  (categories) appearing in the test data that hadn't been seen before in the training data.
 - Ended up rejecting this change because the addition of these features was not worth finding a workaround to the problem with unseen ports.
