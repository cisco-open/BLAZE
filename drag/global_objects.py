"""This contains global objects."""

from design import Design

design = None

def init_design():
    """Instantiate a design instance."""
    global design
    design = Design()
