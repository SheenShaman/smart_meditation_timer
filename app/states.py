from enum import Enum


class BreathPhase(Enum):
    INHALE = "inhale"
    EXHALE = "exhale"


class SessionState(Enum):
    IDLE = "idle"
    RUNNING = "running"
    PAUSED = "paused"
    STOPPED = "stopped"
