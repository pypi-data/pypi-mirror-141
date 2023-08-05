from ..renderer import Renderer
from .schema import BaseSchema


class BaseRenderer(Renderer):
    schema = BaseSchema
