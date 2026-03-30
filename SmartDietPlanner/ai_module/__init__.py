"""
AI Module for Smart Diet Planner
This package contains all AI-related functionality
"""

from .ai_engine import (
    get_ai_recommendation,
    DietAdvisorAgent,
    StateSpace,
    SearchEngine,
    ReasoningEngine,
    FuzzyLogicEngine,
    SemanticNetwork,
    FrameSystem
)

__all__ = [
    'get_ai_recommendation',
    'DietAdvisorAgent',
    'StateSpace',
    'SearchEngine',
    'ReasoningEngine',
    'FuzzyLogicEngine',
    'SemanticNetwork',
    'FrameSystem'
]
