from random import random, randint
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm


class Shooter:
    """
    Represents a shooter in the game.

    Attributes:
        name (int): Unique identifier for the shooter.
        probability (float): Probability of hitting the target.
        target_list (list[int]): List of potential targets.
    """
    NO_TARGET = -1

    def __init__(self, name: int, probability: float, target_list: list[int]):
        self.name = name
        self.probability = probability
        self.status = 'alive'
        self.target = self.NO_TARGET
        self.target_list = target_list.copy()
        self.index = None

    def find_self(self):
        """Finds the index of the shooter in the target list."""
        self.index = next((i for i, target in enumerate(self.target_list) if target == self.name), None)

    def remove_self(self):
        """Removes the shooter from the target list."""
        if self.index is not None:
            self.target_list.pop(self.index)

    def choose_target(self):
        """To be implemented by subclasses."""
        raise NotImplementedError("This method should be implemented by subclasses.")

    def shoot_target(self) -> bool:
        """Attempts to shoot the target."""
        return random() < self.probability


class ShootUp(Shooter):
    def choose_target(self):
        """Shoots the next target in sorted order."""
        self.target_list.sort()
        self.find_self()
        target_index = self.index + 1 if self.index + 1 < len(self.target_list) else self.index - 1
        self.target = self.target_list[target_index]


class ShootUpRound(Shooter):
    def choose_target(self):
        """Shoots the next target in sorted order, wrapping around."""
        self.target_list.sort()
        self.find_self()
        target_index = self.index + 1 if self.index + 1 < len(self.target_list) else 0
        self.target = self.target_list[target_index]


class ShootDown(Shooter):
    def choose_target(self):
        """Shoots the previous target in sorted order."""
        self.target_list.sort()
        self.find_self()
        target_index = self.index - 1 if self.index - 1 >= 0 else len(self.target_list) - 1
        self.target = self.target_list[target_index]


class ShootRandom(Shooter):
    def choose_target(self):
        """Shoots a random target."""
        self.find_self()
        self.remove_self()
        target_index = randint(0, len(self.target_list) - 1)
        self.target = self.target_list[target_index]


def find_index(target_list: list[int], name: int) -> int:
    """Finds the index of a shooter by name in the target list."""
    return next((i for i, target in enumerate(target_list) if target == name), -1)


def initialize_game(num_shooters: int, shooter_type: str = 'up') -> list[Shooter]:
    """
    Initializes the game with a specified number of shooters and shooter type.

    Args:
        num_shooters (int): Number of shooters in the game.
        shooter_type (str): Type of shooter ('up', 'down', 'random', 'upRound').

    Returns:
        list[Shooter]: List of initialized shooters.
    """
    target_list = list(range(1, num_shooters + 1))
    return [SHOOTER_TYPES[shooter_type](shooter_id, shooter_id / num_shooters, target_list)
            for shooter_id in target_list]


def play_round(shooters: list[Shooter], verbose: bool = False) -> list[int]:
    """
    Plays a single round of the game.

    Args:
        shooters (list[Shooter]): List of shooters.
        verbose (bool): Whether to log verbose output.

    Returns:
        list[int]: List of survivors' names.
    """
    shooter_names = [shooter.name for shooter in shooters]
    for shooter in shooters:
        if shooter.status == 'dead':
            continue
        target_list = [s.name for s in shooters if s.status == 'alive']
        shooter.target_list = target_list.copy()
        shooter.choose_target()
        if shooter.shoot_target():
            target_index = find_index(shooter_names, shooter.target)
            shooters[target_index].status = 'dead'
        if verbose:
            print(f"Target list: {target_list}")
            print(f"{shooter.name} aimed at {shooter.target}. Kill is {'successful' if shooter.shoot_target() else 'unsuccessful'}.")
    return [shooter.name for shooter in shooters if shooter.status == 'alive']


def play_game(shooters: list[Shooter], verbose: bool = False) -> int:
    """
    Plays the game until only one shooter remains.

    Args:
        shooters (list[Shooter]): List of shooters.
        verbose (bool): Whether to log verbose output.

    Returns:
        int: The name of the winning shooter.
    """
    round_no = 1
    target_list = [shooter.name for shooter in shooters if shooter.status == 'alive']
    while len(target_list) > 1:
        target_list = play_round(shooters=shooters, verbose=verbose)
        if verbose:
            print(f"End of round {round_no}. Survivors: {target_list}")
        round_no += 1
    return target_list[0]


SHOOTER_TYPES = {
    'up': ShootUp,
    'down': ShootDown,
    'random': ShootRandom,
    'upRound': ShootUpRound
}


if __name__ == "__main__":
    # Collect statistics
    NUM_SHOOTERS = 25
    SHOOTER_TYPE = 'up'
    NUM_GAMES = 100

    winner_list = []
    for _ in tqdm(range(NUM_GAMES)):
        shooters = initialize_game(num_shooters=NUM_SHOOTERS, shooter_type=SHOOTER_TYPE)
        winner = play_game(shooters=shooters, verbose=False)
        winner_list.append(winner)

    # Plot results
    plt.hist(winner_list, bins=2 * NUM_SHOOTERS + 1)
    plt.xlabel('Shooter ID')
    plt.ylabel('Number of Wins')
    plt.title(f'Shooter Game Results for {NUM_GAMES} Games')
    plt.show()
