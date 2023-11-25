from mesa import Agent

class VehicleAgent(Agent):
    def __init__(self, id, system_model, position, trajectory):
        super().__init__(id, system_model)
        self.position = position
        self.trajectory = trajectory

    def navigate(self):
        if not self.trajectory:
            return
        next_position = self.trajectory[0]
        cell_occupants = self.model.grid.get_cell_list_contents([next_position])

        traffic_signals = [obj for obj in cell_occupants if isinstance(obj, TrafficSignalAgent)]
        parking_areas = [obj for obj in cell_occupants if isinstance(obj, ParkingSpaceAgent)]
        other_vehicles = [obj for obj in cell_occupants if isinstance(obj, VehicleAgent) and obj != self]

        if not traffic_signals or traffic_signals[0].signal == "green":
            if not parking_areas or not parking_areas[0].occupied:
                if not other_vehicles:
                    self.model.grid.move_agent(self, next_position)
                    self.position = next_position
                    self.trajectory.pop(0)
                    if parking_areas:
                        parking_areas[0].reserve()

    def act(self):
        self.navigate()


class ParkingSpaceAgent(Agent):
    def __init__(self, id, system_model, position):
        super().__init__(id, system_model)
        self.position = position
        self.occupied = False

    def reserve(self):
        self.occupied = True

    def release(self):
        self.occupied = False


class StructureAgent(Agent):
    def __init__(self, id, system_model, position, hue):
        super().__init__(id, system_model)
        self.position = position
        self.hue = hue

    def act(self):
        pass


class TrafficSignalAgent(Agent):
    def __init__(self, id, system_model, position, signal):
        super().__init__(id, system_model)
        self.position = position
        self.signal = signal # Signals: "red", "green"
        self.countdown = 5  # Initial Timer

    def switch_signal(self):
        if self.signal == 'red' and self.countdown == 0:
            self.signal = 'green'
            self.countdown = 2  # Duration for green signal
        elif self.signal == 'green' and self.countdown == 0:
            self.signal = 'red'
            self.countdown = 5  # Duration for red signal
        else:
            self.countdown -= 1

    def act(self):
        self.switch_signal()
