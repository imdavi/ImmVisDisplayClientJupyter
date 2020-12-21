from pandas import DataFrame
from numpy import issubdtype, number
from sklearn.preprocessing import MinMaxScaler

def _normalise_data_frame(data_frame: DataFrame) -> DataFrame:
    result = data_frame.copy()

    for column_name in result.columns:
        column = result[column_name]

        if not issubdtype(column.dtype, number):
            result[column_name] = column.factorize()[0]

        # result[column_name] = (column - min_value) / \
        #     (max_value - min_value)

    result[result.columns] = MinMaxScaler().fit_transform(result[result.columns])

    return result