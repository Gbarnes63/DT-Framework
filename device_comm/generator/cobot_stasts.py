
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

class CobotStatsGenerator:
    def __init__(self, ident: Identifier, topic: str, energy_range, temp_range, statuses, seed=None):
        self.ident = ident
        self.topic = topic
        self.energy_range = tuple(energy_range)
        self.temp_range = tuple(temp_range)
        self.statuses = statuses
        if seed is not None:
            random.seed(seed)

    @classmethod
    def from_config(cls, cfg: Dict, seed=None):
        c = cfg["generators"]["cobot"]
        ident = Identifier(uuid=c["id"]["uuid"], asset_id=c["id"]["asset_id"])
        return cls(
            ident=ident,
            topic=c["topic"],
            energy_range=c["energy_kwh_range"],
            temp_range=c["temperature_c_range"],
            statuses=["Idle", "Moving", "Gripping"],  # fixed list since weights removed
            seed=seed
        )

    def sample(self):
        return {
            "topic": self.topic,
            "id": {"uuid": self.ident.uuid, "asset_id": self.ident.asset_id},
            "status": random.choice(self.statuses),
            "energy_kwh": round(random.uniform(*self.energy_range), 3),
            "temperature_c": round(random.uniform(*self.temp_range), 2),
                       "timestamp": datetime.utcnow().isoformat()
        }
    
config_path = os.path.join(os.path.dirname(__file__), '..', 'generator_config.json')
with open(config_path, 'r') as f:
    cfg = json.load(f)

# gen = CobotStatsGenerator.from_config(cfg, seed=cfg.get('seed'))

# for _ in range(10):
#     print(json.dumps(gen.sample(), indent=4))