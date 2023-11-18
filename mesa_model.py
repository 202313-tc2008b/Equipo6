from mesa import Agent, Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer

class BuildingAgent(Agent):
    def __init__(self, unique_id, model, pos, color):
        super().__init__(unique_id, model)
        self.pos = pos
        self.color = color

class ParkingLotAgent(Agent):
    def __init__(self, unique_id, model, pos, color):
        super().__init__(unique_id, model)
        self.pos = pos
        self.color = color

class RoundaboutAgent(Agent):
    def __init__(self, unique_id, model, pos, color):
        super().__init__(unique_id, model)
        self.pos = pos
        self.color = color

class TrafficLightAgent(Agent):
    def __init__(self, unique_id, model, pos, color):
        super().__init__(unique_id, model)
        self.pos = pos
        self.color = color

def agent_portrayal(agent):
    portrayal = {"Shape": "rect", "Filled": "true", "Layer": 0}
    if isinstance(agent, BuildingAgent):
        portrayal["Color"] = "blue"
        portrayal["w"] = 1
        portrayal["h"] = 1
    elif isinstance(agent, ParkingLotAgent):
        portrayal["Color"] = "yellow"
        portrayal["w"] = 0.5
        portrayal["h"] = 0.5
    elif isinstance(agent, RoundaboutAgent):
        portrayal["Color"] = "brown"
        portrayal["w"] = 1
        portrayal["h"] = 1
    elif isinstance(agent, TrafficLightAgent):
        portrayal["Color"] = "green"
        portrayal["w"] = 0.5
        portrayal["h"] = 0.5
    return portrayal

class CityModel(Model):
    def __init__(self, width, height):
        self.grid = MultiGrid(width, height, False)
        self.schedule = RandomActivation(self)
        self.current_id = 0

        building_coords = [
            ((2, 5), (11, 5)), ((2, 8), (4, 11)), ((7, 8), (11, 11)),
            ((2, 16), (21, 5)), ((8, 16), (11, 21)), ((16, 2), (17, 5)),
            ((20, 2), (21, 5)), ((16, 16), (21, 17)), ((16, 20), (21, 21))
        ]
        for coords in building_coords:
            x1, y1 = coords[0]
            x2, y2 = coords[1]
            for x in range(x1, x2 + 1):
                for y in range(y1, y2 + 1):
                    building = BuildingAgent(self.next_id(), self, (x, y), "blue")
                    self.grid.place_agent(building, (x, y))
                    self.schedule.add(building)

        parking_lots = [
            (9, 2), (2, 3), (17, 3), (11, 4), (20, 4), (6, 5), (8, 8), (21, 9),
            (4, 10), (11, 10), (16, 10), (2, 17), (17, 17), (20, 17), (5, 20), (8, 20),
            (19, 20)
        ]
        for pos in parking_lots:
            parking_lot = ParkingLotAgent(self.next_id(), self, pos, "yellow")
            self.grid.place_agent(parking_lot, pos)
            self.schedule.add(parking_lot)


        roundabout_coords = [(13, 13), (14, 14)]
        for pos in roundabout_coords:
            roundabout = RoundaboutAgent(self.next_id(), self, pos, "brown")
            self.grid.place_agent(roundabout, pos)
            self.schedule.add(roundabout)

        traffic_lights = [
            (16, 0), (16, 1), (14, 2), (15, 2), (7, 6), (7, 7),
            (5, 8), (6, 8), (0, 11), (1, 11), (2, 12), (2, 13),
            (11, 22), (11, 23), (12, 21), (13, 21), (14, 20), (15, 20),
            (16, 19), (16, 20), (21, 14), (21, 15), (22, 16), (23, 16)
        ]
        for pos in traffic_lights:
            traffic_light = TrafficLightAgent(self.next_id(), self, pos, "green")
            self.grid.place_agent(traffic_light, pos)
            self.schedule.add(traffic_light)

    def step(self):
        self.schedule.step()

    def next_id(self):
        self.current_id += 1
        return self.current_id


grid = CanvasGrid(agent_portrayal, 24, 24, 500, 500)
server = ModularServer(CityModel, [grid], "City Model", {"width": 24, "height": 24})
server.port = 8521 
server.launch()
