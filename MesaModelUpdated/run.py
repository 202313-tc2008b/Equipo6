from mesa.visualization import ModularServer
from mesa.visualization.modules import CanvasGrid
from utils.agents import VehicleAgent, ParkingSpaceAgent, StructureAgent, TrafficSignalAgent
from utils.models import UrbanTrafficModel
from utils.map import grid_size

def color_agent(agent):
    color = {}
    if isinstance(agent, VehicleAgent):
        color = {
                "Shape": "rect",
                "Color": "gray",
                "Filled": "true",
                "Layer": 0,
                "w": 1,
                "h": 1
                }
    if isinstance(agent, ParkingSpaceAgent):
        color = {
                "Shape": "rect",
                "Color": "yellow",
                "Filled": "true",
                "Layer": 0,
                "w": 1,
                "h": 1
                }
    if isinstance(agent, TrafficSignalAgent):
        if agent.state == 'red':
            color = {
                    "Shape": "rect",
                    "Color": "red",
                    "Filled": "true",
                    "Layer": 0,
                    "w": 1,
                    "h": 1
                    }
        else:
            color = {
                    "Shape": "rect",
                    "Color": "green",
                    "Filled": "true",
                    "Layer": 0,
                    "w": 1,
                    "h": 1
                    }
    if isinstance(agent, StructureAgent):
        color = {
                "Shape": "rect",
                "Color": agent.color,
                "Filled": "true",
                "Layer": 0,
                "w": 1,
                "h": 1
                }
    return color


grid = CanvasGrid(color_agent,grid_size, grid_size)

server = ModularServer(
    UrbanTrafficModel, 
    [grid], 
    "Traffic Model", 
    {"grid_width": grid_size, "grid_height": grid_size, "num_vehicles": 17}  # Adjust these keys to match your UrbanTrafficModel's __init__ parameters
)


server.port = 8521

server.launch()
