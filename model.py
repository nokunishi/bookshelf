from itertools import count
from dataclasses import dataclass, field
import datetime

@dataclass
class Book:
    title: str
    author: str
    page: int
    pos: int = field(default_factory=count(1, 1).__next__)
    status: int = field(default=None)
    rating: int = field(default=None)
    started: datetime = field(default=None)
    due: datetime = field(default=None)
