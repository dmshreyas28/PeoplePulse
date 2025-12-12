"""Routers package."""
from .predict import router as predict_router
from .simulate import router as simulate_router
from .employees import router as employees_router

__all__ = ["predict_router", "simulate_router", "employees_router"]
