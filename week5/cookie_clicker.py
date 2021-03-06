"""
Cookie Clicker Simulator
"""

import simpleplot
import math

# Used to increase the timeout, if necessary
import codeskulptor
codeskulptor.set_timeout(20)

import poc_clicker_provided as provided

# Constants
SIM_TIME = 10000000000.0

class ClickerState:
    """
    Simple class to keep track of the game state.
    """
    
    def __init__(self):
        self._total_cookies_produced = 0.0
        self._current_number_cookies = 0.0
        self._current_time = 0.0
        self._current_cps = 1.0
        self._history = [(0.0, None, 0.0, 0.0)]
        
    def __str__(self):
        """
        Return human readable state
        """
        result = "Time: " +  str(self._current_time) + "\n" \
                 + "Current Cookies: " + str(self._current_number_cookies) + "\n" \
                 + "CPS: " + str(self._current_cps) + "\n" \
                 + "Total Cookies: " + str(self._total_cookies_produced)
        return result
        
    def get_cookies(self):
        """
        Return current number of cookies 
        (not total number of cookies)
        
        Should return a float
        """
        return self._current_number_cookies
    
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

        For example: [(0.0, None, 0.0, 0.0)]

        Should return a copy of any internal data structures,
        so that they will not be modified outside of the class.
        """
        return self._history

    def time_until(self, cookies):
        """
        Return time until you have the given number of cookies
        (could be 0.0 if you already have enough cookies)

        Should return a float with no fractional part
        """
        delta_cookies = cookies - self._current_number_cookies

        if delta_cookies < 0:
            return 0.0
        #return int(delta_cookies * 1.0 / self._current_cps + 0.99999999999999999999) * 1.0
        return math.ceil(delta_cookies * 1.0 / self._current_cps) * 1.0
    
    def wait(self, time):
        """
        Wait for given amount of time and update state

        Should do nothing if time <= 0.0
        """
        if time > 0.0:
            self._total_cookies_produced += self._current_cps * time
            self._current_number_cookies += self._current_cps * time
            self._current_time += time
    
    def buy_item(self, item_name, cost, additional_cps):
        """
        Buy an item and update state

        Should do nothing if you cannot afford the item
        """
        if self._current_number_cookies >= cost:
            self._current_number_cookies -= cost
            self._current_cps += additional_cps
            self._history.append((self._current_time, item_name, cost, self._total_cookies_produced))
    
def simulate_clicker(build_info, duration, strategy):
    """
    Function to run a Cookie Clicker game for the given
    duration with the given strategy.  Returns a ClickerState
    object corresponding to the final state of the game.
    """

    # Replace with your code
    current_build_info = build_info.clone()
    clicker_state = ClickerState()
    while clicker_state.get_time() <= duration:
        item_to_buy = strategy(clicker_state.get_cookies(), \
                               clicker_state.get_cps(), \
                               clicker_state.get_history(), \
                               duration - clicker_state.get_time(), \
                               current_build_info)
        if item_to_buy is None:
            break
        purchase_time = clicker_state.time_until(current_build_info.get_cost(item_to_buy))
        if purchase_time > duration - clicker_state.get_time():
            break
        clicker_state.wait(purchase_time)
        clicker_state.buy_item(item_to_buy, current_build_info.get_cost(item_to_buy), \
                               current_build_info.get_cps(item_to_buy))
        current_build_info.update_item(item_to_buy)
    clicker_state.wait(duration - clicker_state.get_time())
    return clicker_state

def strategy_cursor_broken(cookies, cps, history, time_left, build_info):
    """
    Always pick Cursor!

    Note that this simplistic (and broken) strategy does not properly
    check whether it can actually buy a Cursor in the time left.  Your
    simulate_clicker function must be able to deal with such broken
    strategies.  Further, your strategy functions must correctly check
    if you can buy the item in the time left and return None if you
    can't.
    """
    return "Cursor"

def strategy_none(cookies, cps, history, time_left, build_info):
    """
    Always return None

    This is a pointless strategy that will never buy anything, but
    that you can use to help debug your simulate_clicker function.
    """
    return None

def strategy_cheap(cookies, cps, history, time_left, build_info):
    """
    Always buy the cheapest item you can afford in the time left.
    """
    cookies_afford = cookies + cps * time_left
    items = build_info.build_items()
    result = None
    cheapest_cost = -1
    for item in items:
        cost = build_info.get_cost(item)
        if cheapest_cost == -1:
            cheapest_cost = cost
        if cheapest_cost >= cost and cookies_afford >= cost:
            result = item
            cheapest_cost = cost
    return result

def strategy_expensive(cookies, cps, history, time_left, build_info):
    """
    Always buy the most expensive item you can afford in the time left.
    """
    cookies_afford = cookies + cps * time_left
    items = build_info.build_items()
    result = None
    expensive_cost = -1
    for item in items:
        cost = build_info.get_cost(item)
        if expensive_cost <= cost and cookies_afford >= cost:
            result = item
            expensive_cost = cost
    return result

def strategy_best(cookies, cps, history, time_left, build_info):
    """
    The best strategy that you are able to implement.
    """
    
    # calculate the slope = upgrade_cost / cps incremental, pick the lowest slope
    cookies_afford = cookies + cps * time_left
    items = build_info.build_items()
    result = None
    tmp_slope = -1
    for item in items:
        cost = build_info.get_cost(item)
        inc_cps = build_info.get_cps(item)
        slope = cost / inc_cps
        if cookies_afford >= cost:
            if tmp_slope == -1: 
                tmp_slope = slope
            if tmp_slope >= slope:
                result = item
                tmp_slope = slope
    return result

def run_strategy(strategy_name, time, strategy):
    """
    Run a simulation for the given time with one strategy.
    """
    state = simulate_clicker(provided.BuildInfo(), time, strategy)
    print strategy_name, ":", state
    #print state.get_history()
    print

    # Plot total cookies over time

    # Uncomment out the lines below to see a plot of total cookies vs. time
    # Be sure to allow popups, if you do want to see it

    # history = state.get_history()
    # history = [(item[0], item[3]) for item in history]
    # simpleplot.plot_lines(strategy_name, 1000, 400, 'Time', 'Total Cookies', [history], True)

def run():
    """
    Run the simulator.
    """    
    # run_strategy("Cursor", SIM_TIME, strategy_cursor_broken)

    # Add calls to run_strategy to run additional strategies
    run_strategy("Cheap", SIM_TIME, strategy_cheap)
    run_strategy("Expensive", SIM_TIME, strategy_expensive)
    run_strategy("Best", SIM_TIME, strategy_best)
    
run()

