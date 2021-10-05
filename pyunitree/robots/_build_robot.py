
def _build_robot(handler, transmitter, receiver):
    handler.set_transmitter(transmitter)
    handler.set_receiver(receiver)
    robot = handler
    return robot
