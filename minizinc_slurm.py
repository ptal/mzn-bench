#!/usr/bin/env python3
import os

from dataclasses import dataclass, field
from datetime import timedelta
from minizinc import Solver
from pathlib import Path
from typing import Any, Dict, Optional

this_dir = Path(os.path.dirname(os.path.realpath(__file__)))

# Configure SLURM attributes
job_name = "MiniZinc Benchmark"
cpu_per_task = 1
mem = 4096
nodelist = ["critical001"]

# Configure benchmark attributes
instances = this_dir / "instances.csv"
timeout = timedelta(minutes=15)
output_dir = this_dir / "results"

# Configure MiniZinc Configurations
@dataclass
class Configuration:
    name: str
    solver: Solver
    minizinc: Optional[Path] = None
    processes: Optional[int] = None
    random_seed: Optional[int] = None
    free_search: bool = False
    optimisation_level: Optional[int] = None
    other_flags: Dict[str, Any] = field(default_factory=dict)

configurations = [
    Configuration("Gecode", Solver.lookup("gecode")),
    Configuration("Chuffed", Solver.lookup("chuffed")),
]

# The actual script that schedules SLURM tasks
if __name__ == "__main__":
    num_instances = sum(1 for line in open(config.instances)) - 1
    num_solvers = len(config.solvers)

    script = this_dir / "run_instance.sh"
    assert(script.exists())

    hard_timeout = timeout + timedelta(minutes=1)

    os.execlp("sbatch", "sbatch", "--output=/dev/null", f"--array=1-{num_instances*num_solvers}", f"--time={timeout}", str(script.resolve()))
