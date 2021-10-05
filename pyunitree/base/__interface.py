from numpy import zeros
from ._constants import NUM_MOTORS, POSITION_GAINS, DAMPING_GAINS, INIT_ANGLES
from time import perf_counter
from multiprocessing import Process, Manager


# TODO: Set the process priority



class Interface:
    """Creating the Interface to run with specified 
       in separate process"""

    def __init__(self, update_rate=1000, level='high'):
        self.level = level
        self.update_rate = update_rate
        if self.level == 'high':
            self.command_size = 10
        else:
            self.level = 'low'
            self.command_size = 60


        self.__zero_command = zeros(self.command_size)

        self.__shared = Manager().Namespace()
        self.__shared.command = self.__zero_command
        # self.__shared.update_rate = update_rate

        self.__shared.process_is_working = False

        self.state = Manager().Namespace()
        # self.state.time = 0
        self.level = level

        self.__transmitter_setted = False
        self.__receiver_setted = False

        self._interface_process = Process(target=self.__interface)

    def set_transmitter(self, transmitter):
        self.transmitter = transmitter
        self.__transmitter_setted = True

    def set_receiver(self, receiver):
        self.receiver = receiver
        self.__receiver_setted = True

    def bind_interface(self, receiver, transmitter):
        self.set_transmitter(transmitter)
        self.set_receiver(receiver)

    def __del__(self):
        self.stop(output=True)
        print('Interface process is deleted from memory...')

    def start(self):
        if not (self.__transmitter_setted and self.__receiver_setted):
            # print('')
            self.__del__()
        else:
            print(
                f'the {self.level} interface process will start soon with rate {self.update_rate}')
            self._interface_process.start()
        print('Waiting for process to start...')

    def stop(self, output=False):
        self._interface_process.join(timeout=0.)
        self._interface_process.terminate()
        # self._interface_process.terminate()
        if output:
            print('Interface process was terminated')

    def __interface(self):

        try:
            self.__shared.process_is_working = True

            initial_time = perf_counter()
            tick = 0
            while True:
                actual_time = perf_counter() - initial_time

                if actual_time - tick >= 1/self.update_rate:

                    self.transmitter(self.__shared.command)
                    state = self.receiver()
                    # print(state.imu.rpy)
                    self.state = state

                    tick = actual_time

        except KeyboardInterrupt:
            print('Exit')

    def set_command(self, command):
        self.__shared.command = command
