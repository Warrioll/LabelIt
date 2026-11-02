from nicegui import ui, events
from Box import Box
from typeguard import typechecked
from DatasetImage import DatasetImage
import state

@typechecked
class LabelsClass:
    innerId:int
    classId:int
    className:str


