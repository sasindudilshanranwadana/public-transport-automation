
from AppAgent import AppAgent


class AppAgentManager:
    def __init__(self, homes, canvas, university_location, buses, trains):
        self.agents = [AppAgent(
                name=f"Person {i + 1}",
                x=x,
                y=y,
                university_location=university_location,
                buses=buses,
                trains=trains,
                speed=0.25,
                canvas=canvas
            )
            for i, (x, y) in enumerate(homes)
        ]
            