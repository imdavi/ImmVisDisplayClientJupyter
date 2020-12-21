from pandas import DataFrame
from grpc import Channel, insecure_channel
from .proto import ImmVisJupyterStub
from .utils import _normalise_data_frame, _map_data_frame_to_dataset_to_plot

GRPC_OPTION_MAX_RECEIVE_MESSAGE_LENGTH = 'grpc.max_receive_message_length'
GRPC_OPTION_MAX_SEND_MESSAGE_LENGTH = 'grpc.max_send_message_length'
MAX_MESSAGE_SIZE = 100 * 1024 *1024

class ImmVisJupyterClient:

    _grpc_channel: Channel = None

    _stub: ImmVisJupyterStub = None

    def __init__(self, hostname: str = 'localhost', port: int = 50051):
        self.hostname = hostname
        self.port = port

    def connect(self):
        target = '{hostname}:{port}'.format(hostname=self.hostname, port=str(self.port))

        options = [(GRPC_OPTION_MAX_RECEIVE_MESSAGE_LENGTH, MAX_MESSAGE_SIZE),
                   (GRPC_OPTION_MAX_SEND_MESSAGE_LENGTH, MAX_MESSAGE_SIZE)]

        self._grpc_channel = insecure_channel(target=target,  options=options)

        self._stub = ImmVisJupyterStub(self._grpc_channel)

    def disconnect(self):
        self._grpc_channel.close()
        self._grpc_channel = None
        pass

    def is_connected(self) -> bool:
        # We need to improve the way of checking if the client is connected.
        return self._grpc_channel is not None

    def plot_dataset(self, data_frame: DataFrame, normalise_before_send: bool = True):
        data_frame_to_plot : DataFrame = None

        if normalise_before_send: 
            data_frame_to_plot = _normalise_data_frame(data_frame)
        else:
            data_frame_to_plot = data_frame

        self._stub.PlotDataset(_map_data_frame_to_dataset_to_plot(data_frame_to_plot))
