import time
import random
import multiprocessing
from concurrent.futures import ProcessPoolExecutor, as_completed
import psutil
from typing import Dict, Tuple
from BiNeuron.data.constants_for_functions import (TYPES_POWER, POINTS_PER_CORE,
                                                    REF_POINTS, HARD_VALUE, EASY_VALUE,
                                                    VERY_HARD_VALUE)
import logging


logger = logging.getLogger(__name__)

def get_system_info() -> Dict:
    """
    Retrieves system hardware information: CPU cores, max frequency, and RAM in GB.
    :return: Contains 'cpu_cores', 'cpu_max_freq_mhz', and 'ram_gb'.
    """
    logger.info("Challenge get_system_info")
    cpu_count = multiprocessing.cpu_count()
    ram_bytes = psutil.virtual_memory().total
    ram_gb = ram_bytes / (1024 ** 3)
    freq = psutil.cpu_freq()

    if freq and freq.max:
        cpu_max_freq_mhz = freq.max
    else:
        cpu_max_freq_mhz = None

    logger.info("Your computer's system information has been identified.")
    return {
        "cpu_cores": cpu_count,
        "cpu_max_freq_mhz": cpu_max_freq_mhz,
        "ram_gb": ram_gb
    }

def monte_carlo_pi(n_points: int) -> int:
    """
    Estimates Pi using the Monte Carlo method for a given number of points.
    :param n_points: Number of random points to generate.
    :return: Count of points that fall inside the unit circle.
    """
    logger.info("Challenge monte_carlo_pi")
    inside = 0

    for _ in range(n_points):
        x = random.random()
        y = random.random()

        if x*x + y*y <= 1.0:
            inside += 1

    return inside

def run_benchmark() -> Tuple:
    """
    Runs a parallel Monte Carlo Pi benchmark across all CPU cores.
    :return: (points_per_second, pi_approximation)
    """
    logger.info("Challenge run_benchmark")
    cpu_cores = multiprocessing.cpu_count()
    total_points = POINTS_PER_CORE * cpu_cores
    chunk_sizes = [POINTS_PER_CORE] * cpu_cores
    start_time = time.time()

    with ProcessPoolExecutor(max_workers=cpu_cores) as executor:
        futures = [executor.submit(monte_carlo_pi, chunk) for chunk in chunk_sizes]
        inside_counts = [f.result() for f in as_completed(futures)]

    elapsed = time.time() - start_time
    total_inside = sum(inside_counts)
    pi_approx = 4.0 * total_inside / total_points
    points_per_second = total_points / elapsed

    logger.info("A benchmark has been launched to obtain the power of the user's computer.")
    return points_per_second, pi_approx

def calculate_score(points_per_second: float, ram_gb: float) -> int:
    """
    Computes a performance score based on benchmark points/sec and RAM.
    :param points_per_second: Points processed per second.
    :param ram_gb: Available RAM in GB.
    :return: Rounded final score (0-100).
    """
    logger.info("Challenge calculate_score")
    cpu_score = min(100, (points_per_second / REF_POINTS) * 100)
    ram_score = min(100, (ram_gb / 32) * 100)
    final_score = 0.75 * cpu_score + 0.25 * ram_score

    logger.info("A calculation was made to obtain the total power.")
    return round(final_score)

def main() -> int:
    """
    Orchestrates the full benchmark process and returns the final score.
    :return: Overall performance score.
    """
    logger.info("Challenge main")
    info = get_system_info()
    ram = info["ram_gb"]
    points_per_sec, pi_approx = run_benchmark()
    score = calculate_score(points_per_sec, ram)

    logger.info("The total number of computer power at the end of the benchmarks is obtained.")
    return score

def determining_type_computer() -> str:
    """
    Determines the computer's power category based on benchmark score.
    :return: One of the TYPES_POWER constants (e.g., 'weak', 'average', 'powerful', 'very_powerful').
    """
    logger.info("Challenge determining_type_computer")
    answer = main()

    if answer > VERY_HARD_VALUE:
        logger.info("You have a very powerful computer (to run local AI).")
        return TYPES_POWER[3]
    if HARD_VALUE < answer <= VERY_HARD_VALUE:
        logger.info("You have a powerful computer (to run a local AI).")
        return TYPES_POWER[2]
    elif EASY_VALUE < answer <= HARD_VALUE:
        logger.info("You have an average computer (for running a local AI).")
        return TYPES_POWER[1]
    else:
        logger.info("You have a weak computer (to run a local AI).")
        return TYPES_POWER[0]
