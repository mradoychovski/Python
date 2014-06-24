"""
Cookie Clicker Simulator
"""
import math
import SimpleGUICS2Pygame.simpleplot as simpleplot

# Used to increase the timeout, if necessary
import SimpleGUICS2Pygame.codeskulptor as codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState(object):
    """
    Simple class to keep track of the game state.
    """

    def __init__(self):
        self._total_cookies = 0.0
        self._current_cookies = 0.0
        self._current_time = 0.0
        self._current_cps = 1.0
        self._history_list = [(0.0, None, 0.0, 0.0)]

    def __str__(self):
        """
        Return human readable state
        """
        total_cookies = "Total Cookies: %s " % str(self._total_cookies)
        current_cookies = "Current Cookies: %s " % str(
            self._current_cookies)
        current_time = "Current Time: %s " % str(self._current_time)
        current_cps = "Current CPS: %s " % str(self._current_cps)
        result = total_cookies + current_cookies + \
            current_time + current_cps
        return result[:-1]

    def get_cookies(self):
        """
        Return current number of cookies
        (not total number of cookies)

        Should return a float
        """
        return self._current_cookies

    def get_cps(self):
        """
        Get current CPS

        Should return a float
        """
        return self._current_cps

    def get_time(self):
        """
        Get current time

        Should return a float
        """
        return self._current_time

    def get_history(self):
        """
        Return history list

        History list should be a list of tuples of the form:
        (time, item, cost of item, total cookies)

        For example: (0.0, None, 0.0, 0.0)
        """
        return self._history_list

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        current_cookies = self._current_cookies
        if current_cookies >= cookies:
            return 0.0
        return math.ceil((cookies - current_cookies) / self._current_cps)

    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0
        """
        if time > 0:
            self._current_time += time
            self._current_cookies += time * self._current_cps
            self._total_cookies += self._current_cps * time

    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if cost <= self._current_cookies:
            self._current_cookies -= cost
            self._current_cps += additional_cps
            self._history_list.append(
                (self._current_time, item_name, cost, self._total_cookies))


def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to game.
    """
    binfo_cloning = build_info.clone()
    clicker = ClickerState()
    while clicker.get_time() <= duration:
        current_time = clicker.get_time()
        cookies = clicker.get_cookies()
        cps = clicker.get_cps()
        time_left = duration - current_time
        item = strategy(cookies, cps, time_left, binfo_cloning)
        if item is None:
            clicker.wait(time_left)
            break
        elapsed_time = clicker.time_until(binfo_cloning.get_cost(item))
        if elapsed_time <= time_left:
            clicker.wait(elapsed_time)
            cost = binfo_cloning.get_cost(item)
            additional_cps = binfo_cloning.get_cps(item)
            clicker.buy_item(item, cost, additional_cps)
            binfo_cloning.update_item(item)
        else:
            clicker.wait(time_left)
            break
    #print clicker.get_history()
    return clicker


def strategy_cursor(cookies, cps, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic strategy does not properly check whether
    it can actually buy a Cursor in the time left.  Your strategy
    functions must do this and return None rather than an item you
    can't buy in the time left.
    """
    item = "Cursor"
    cost = build_info.get_cost(item)
    if cookies + cps * time_left >= cost:
        return "Cursor"
    return None


def strategy_none(cookies, cps, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that you can use to help debug
    your simulate_clicker function.
    """
    del cookies, cps, time_left, build_info
    return None


def strategy_cheap(cookies, cps, time_left, build_info):
    """
     This strategy always select the cheapest item.
    """
    min_cost = float('inf')
    cheap_item = ""
    for item in build_info.build_items():
        cost = build_info.get_cost(item)
        if min_cost > cost and cookies + cps * time_left >= cost:
            min_cost = cost
            cheap_item = item
    if cheap_item != "":
        return cheap_item
    else:
        return None

def strategy_expensive(cookies, cps, time_left, build_info):
    """
    This strategy always select the most expensive
    item you can afford in the time left.
    """
    max_cost = float('-inf')
    expensive_item = ""
    for item in build_info.build_items():
        cost = build_info.get_cost(item)
        if cost > max_cost and cookies + cps * time_left >= cost:
            max_cost = cost
            expensive_item = item
    if expensive_item != "":
        return expensive_item
    else:
        return None


def strategy_best(cookies, cps, time_left, build_info):
    """
    This is the best strategy that you can come up with.
    """
    max_best = 0.0
    best_item = ""
    for item in build_info.build_items():
        cost = build_info.get_cost(item)
        ratio = build_info.get_cps(item) / cost
        if ratio > max_best and (cookies + cps * time_left)*0.8 >= cost:
            max_best = ratio
            best_item = item
    if best_item != "":
        return best_item
    else:
        return None


def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation with one strategy
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    history = state.get_history()
    history = [(item[0], item[3]) for item in history]
    simpleplot.plot_lines(strategy_name, 1000, 400, 'Time',
        'Total Cookies', [history], True, ['history'], True)


def run():
    """
    Run the simulator.
    """
    run_strategy("Cursor", SIM_TIME, strategy_cursor)

    # Add calls to run_strategy to run additional strategies
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    run_strategy("None", SIM_TIME, strategy_none)

run()
