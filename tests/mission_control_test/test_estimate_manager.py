

from .collector_world import *

from mission_control.estimate.estimate import EstimateManager
from mission_control.estimate.core import create_context_gen, SkillDescriptorRegister
from mission_control.core import POI, worker_factory
from mission_control.mission.ihtn import ElementaryTask

from lagom import Container

from enum import Enum
from mission_control.estimate.commons.routes_ed import RoutesEnvironmentDescriptor, Map
from mission_control.estimate.commons.navigation_sd import NavigationSkillDescriptor, Move

class task_types(Enum):
    NAV = 'navigate'
    SIMPLE_ACTION = 'simple_action'

sr_poi = POI('storage_room')
room1_poi = POI('room1')
room3_poi = POI('room3')
task1 = ElementaryTask(type=task_types.NAV, destination=room3_poi)
task2 = ElementaryTask(type=task_types.NAV, destination=room1_poi)
task3 = ElementaryTask(type=task_types.NAV, destination=room3_poi)
task_list = [task1, task2, task3]

container = Container()
# env desc
container[Map] = Map(pois =[], segments=[])
routes_ed = container[RoutesEnvironmentDescriptor]

# skill desc
nav_sd = container[NavigationSkillDescriptor]

# skill desc container singleton
sd_register = SkillDescriptorRegister( (task_types.NAV, nav_sd))
container[SkillDescriptorRegister] = sd_register

# estimate manager
em:EstimateManager = container[EstimateManager]

class ca(Enum):
    move = 'move'
    power_source_battery = 'battery'
    power_source_grid = 'power_grid'



worker1 = worker_factory(position = sr_poi, 
        capabilities=[
            Move(avg_speed = 15, u='m/s'),
            # power_source_battery( 
            #     { capacity:1000, u:'Ah'},
            #     { charge:900, u:'Ah'}, ),
        ],
        skills=[task_types.NAV],
        # models=[
        #     c('constant_power_consumption', rate=300, u='Ah'),
        # ]
        )

task_context_gen = create_context_gen(worker1, task_list)
task_ctxs = list(task_context_gen)
last_ctx = task_ctxs[2]


def test_estimate_navigation_task_in_context():
    estimate = em.estimate_task_in_context(last_ctx)
    assert estimate is not None


def test_estimate():
    bid = em.estimate(worker1, task_list)
    assert bid.estimate.time == 20


def test_estimate_no_route():
    assert False

# def test_get_compatible_workers(cf_manager: CoalitionFormationManager, ihtn_collect, collection_robots_a_and_b):
#     robot_a = collection_robots_a_and_b[0]
#     # mock a path between robot_a and room3 with distance 100
#     # robot_a avg_speed

#     bid  = cf_manager.estimate(robot_a, task_list)