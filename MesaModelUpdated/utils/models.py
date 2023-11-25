import random
from mesa import Model
from mesa.space import MultiGrid
from mesa.time import RandomActivation
from .agents import VehicleAgent, ParkingSpaceAgent, StructureAgent, TrafficSignalAgent
from .map import RoadIntersections, ParkingSpots, Buildings, TrafficLights
from .utils import generate_graph, execute_astar_algorithm, calculate_manhattan_distance

class UrbanTrafficModel(Model):
    """
    A model for simulating urban traffic with vehicle agents navigating to their destinations.
    """

    def __init__(self, grid_width, grid_height, num_vehicles):
        self.RoadNetwork = generate_graph(RoadIntersections)
        self.vehicle_count = num_vehicles
        self.city_grid = MultiGrid(grid_width, grid_height, True)
        self.simulation_schedule = RandomActivation(self)
        super().__init__()
        self.grid = MultiGrid(grid_width, grid_height, True)
        agent_id = 1

        # Initialize agents
        # Vehicle agents
        start_points = list(RoadIntersections.keys())
        random.shuffle(start_points)
        destinations = ParkingSpots[:]
        for _ in range(len(destinations)):
            start = start_points.pop()
            destination = destinations.pop()
            route = execute_astar_algorithm(self.RoadNetwork, start, destination, calculate_manhattan_distance)
            vehicle = VehicleAgent(agent_id, self, start, route)
            agent_id += 1
            self.simulation_schedule.add(vehicle)
            self.city_grid.place_agent(vehicle, start)

        # Parking space agents
        for parking_coord in ParkingSpots:
            parking = ParkingSpaceAgent(agent_id, self, parking_coord)
            agent_id += 1
            self.simulation_schedule.add(parking)
            self.city_grid.place_agent(parking, parking_coord)

        # Building agents
        for building_info in Buildings:
            building_location, building_color = building_info
            building = StructureAgent(agent_id, self, building_location, building_color)
            agent_id += 1
            self.simulation_schedule.add(building)
            self.city_grid.place_agent(building, building_location)

        # Traffic light agents
        for signal_info in TrafficLights:
            signal_location, signal_state = signal_info
            light = TrafficSignalAgent(agent_id, self, signal_location, signal_state)
            agent_id += 1
            self.simulation_schedule.add(light)
            self.city_grid.place_agent(light, signal_location)

    def simulate_step(self):
        self.simulation_schedule.step()

    def retrieveVehiclePositions(self):
        vehicle_positions = []
        for agent in self.simulation_schedule.agents:
            if isinstance(agent, VehicleAgent):
                id, (x, y) = agent.unique_id, agent.pos
                vehicle_positions.append([id, x, y])
        return sorted(vehicle_positions, key=lambda x: x[0])
