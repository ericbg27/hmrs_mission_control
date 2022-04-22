
from ..world_collector import *

from mission_control.coordination.coalition_formation import CoalitionFormationProcess, Bid
from mission_control.data_model import Estimate, InviableEstimate


def test_flat_plan(cf_process: CoalitionFormationProcess, ihtn_collect, collection_ihtn):
    nav_to_room3 = collection_ihtn.navto_room3.value
    pick_up_object = collection_ihtn.pick_up_object.value
    obtained_task = cf_process.flat_plan(ihtn_collect)
    diff = set(obtained_task) ^ {nav_to_room3, pick_up_object}
    assert not diff


def test_get_compatible_workers(cf_process: CoalitionFormationProcess, ihtn_collect, collection_robots, collection_robots_a_b_and_d):
    task_list = cf_process.flat_plan(ihtn_collect)
    comp_workers = list(cf_process.get_compatible_workers(task_list, collection_robots))
    # robot_a and robot_b have the skills, robot_c does not
    diff =  set(comp_workers) ^ set(collection_robots_a_b_and_d)
    assert not diff

def test_check_viable(cf_process: CoalitionFormationProcess, collection_robots):
    worker = collection_robots[0]
    bid = Bid(worker = worker, estimate = Estimate(time = 3, energy = 0.1))
    assert cf_process.check_viable(bid, None) == True

def test_check_inviable(cf_process: CoalitionFormationProcess, collection_robots):
    worker = collection_robots[0]
    bid = Bid(worker = worker, estimate = Estimate(time = 3, energy = 10))
    res =  cf_process.check_viable(bid, None)
    assert res == False
    assert bid.estimate.is_inviable == True


def test_check_not_viable(cf_process: CoalitionFormationProcess, collection_robots):
    worker = collection_robots[0]
    bid = Bid(worker = worker, estimate = InviableEstimate(reason='no route'))
    assert cf_process.check_viable(bid, None) == False


def test_sort_and_select_bids(cf_process: CoalitionFormationProcess, collection_robots):
    worker = collection_robots[0]
    bid1 = Bid(worker = worker, estimate = Estimate(time = 3, energy = 5))

    worker = collection_robots[1]
    bid2 = Bid(worker = worker, estimate = Estimate(time = 2, energy = 5))

    worker = collection_robots[1]
    bid3 = Bid(worker = worker, estimate = Estimate(time = 2.5, energy = 5))
    sorted_bids = cf_process.rank_bids([bid1, bid2, bid3])
    assert sorted_bids[0] == bid2
    assert sorted_bids[1] == bid3
    assert sorted_bids[2] == bid1

    task = ElementaryTask('noop')
    sorted_bids
    plan_rank_map = {}
    plan_rank_map[task] = sorted_bids
    result = cf_process.select_bids(plan_rank_map)
    assert result[task] == sorted_bids[0]




