from itertools import count
from dataclasses import dataclass, field
import datetime

@dataclass
class Book:
    title: str
    author: str
    page: int
    id: int = field(default_factory=count(1, 1).__next__)
    category: str = field(default='Novel')
    status: int = field(default=None)
    rating: int = field(default=None)
