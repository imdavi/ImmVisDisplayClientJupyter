from pandas import DataFrame
from ..proto import DatasetToPlot, DatasetRow

def _map_data_frame_to_dataset_to_plot(data_frame: DataFrame) -> DatasetToPlot:
    return DatasetToPlot(
        rows=list(map(lambda row: DatasetRow(rowValues=row),
                 data_frame.values))
    )