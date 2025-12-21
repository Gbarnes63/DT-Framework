import random
from dataclasses import dataclass
from typing import Dict
from datetime import datetime
import json
import os

@dataclass(frozen=True)
class Identifier:
    uuid: str | None = None
    asset_id: str | None = None

class ShelfStatsGenerator:
    def __init__(self, ident: Identifier, topic: str, actions, part_count_range, location, seed=None):
        self.ident = ident
        self.topic = topic
        self.actions = actions
        self.part_count_range = tuple(part_count_range)
        self.location = location
        if seed is not None:
            random.seed(seed)

    @classmethod
    def from_config(cls, cfg: Dict, seed=None):
        c = cfg["generators"]["shelf"]
        ident = Identifier(uuid=c["id"]["uuid"], asset_id=c["id"]["asset_id"])
        return cls(
            ident=ident,
            topic=c["topic"],
            actions=c["actions"],
            part_count_range=c["part_count_range"],
            location=c["location"],
            seed=seed
        )

    def sample(self):
        return {
            "topic": self.topic,
            "id": {"uuid": self.ident.uuid, "asset_id": self.ident.asset_id},
            "action": random.choice(self.actions),
            "part_count": random.randint(*self.part_count_range),
            "location": self.location,
            "timestamp": datetime.utcnow().isoformat()
        }
    
config_path = os.path.join(os.path.dirname(__file__), '..', 'generator_config.json')
with open(config_path, 'r') as f:
    cfg = json.load(f)

# gen = ShelfStatsGenerator.from_config(cfg, seed=cfg.get('seed'))

# for _ in range(10):
#     print(json.dumps(gen.sample(), indent=4))
