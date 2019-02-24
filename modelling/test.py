import pandas as pd
import numpy as np
import datetime
import time
import math
import util

start = time.time()
sparse_dict = util.create_sparse_matrix("new.csv", replace=False)
print("time", time.time() - start)



