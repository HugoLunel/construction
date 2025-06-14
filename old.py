from collections import defaultdict
from dataclasses import dataclass
from datetime import datetime
from uuid import uuid4
from intervaltree import IntervalTree
from pprint import pprint

@dataclass(frozen=True)
class Task:
    id: str
    name: str
    employee_ids: set[str]
    machine_ids: set[str]
    begin_time: datetime
    end_time: datetime


employee_schedules: dict[str, IntervalTree] = defaultdict(IntervalTree)
machine_schedules: dict[str, IntervalTree] = defaultdict(IntervalTree)
tasks: dict[str, Task] = {}

def assert_no_overlap(
    employee_ids: set[str],
    machine_ids: set[str],
    begin_time: datetime,
    end_time: datetime,
) -> None:
    for employee_id in employee_ids:
        schedule = employee_schedules.get(employee_id, IntervalTree())
        if schedule.overlaps(begin_time.timestamp(), end_time.timestamp()):
            raise ValueError(
                f"Employee {employee_id} is not available during the requested time."
            )

    for machine_id in machine_ids:
        schedule = machine_schedules.get(machine_id, IntervalTree())
        if schedule.overlaps(begin_time.timestamp(), end_time.timestamp()):
            raise ValueError(
                f"Machine {machine_id} is not available during the requested time."
            )


def create_task(
    name: str,
    employee_ids: list[str],
    machine_ids: list[str],
    begin_time: datetime,
    end_time: datetime,
) -> None:
    assert_no_overlap(employee_ids, machine_ids, begin_time, end_time)

    task_id = str(uuid4())

    for employee_id in employee_ids:
        employee_schedules[employee_id].addi(
            begin_time.timestamp(), end_time.timestamp(), task_id
        )

    for machine_id in machine_ids:
        machine_schedules[machine_id].addi(
            begin_time.timestamp(), end_time.timestamp(), task_id
        )

    task = Task(
        id=task_id,
        name=name,
        employee_ids=employee_ids,
        machine_ids=machine_ids,
        begin_time=begin_time,
        end_time=end_time,
    )
    tasks[task_id] = task


# def get_schedule(employee_id: str) -> list[Task]:
#     schedule = employee_schedules[employee_id]
#     task_ids = schedule.data


create_task(
    name="Task 1",
    employee_ids=["employee1", "employee2"],
    machine_ids=["machine1", "machine2"],
    begin_time=datetime(2023, 10, 1, 8, 0),
    end_time=datetime(2023, 10, 1, 12, 0),
)

create_task(
    name="Task 2",
    employee_ids=["employee1"],
    machine_ids=["machine1"],
    begin_time=datetime(2023, 10, 1, 12, 0),
    end_time=datetime(2023, 10, 1, 14, 0),
)

employee_id = "employee1"
print(f"Schedule for employee {employee_id}:")
schedule = employee_schedules.get(employee_id, IntervalTree())
for interval in sorted(schedule):
    task_id = interval.data
    task = tasks[task_id]
    print(f"- {task.name}: {task.begin_time} to {task.end_time}")
