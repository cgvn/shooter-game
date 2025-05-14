from random import random, randint
import matplotlib.pyplot as plt
from tqdm import tqdm
from typing import List, Type

class Shooter:
    def __init__(self, name: int, probability: float, target_list: List[int]):
        self.name = name
        self.probability = probability
        self.status = 'alive'
        self.target_list = target_list[:]
        self.target = -1

    def choose_target(self):
        pass

    def shoot_target(self) -> bool:
        return random() < self.probability

class ShootUp(Shooter):
    def choose_target(self):
        self.target_list.sort()
        idx = self.target_list.index(self.name)
        if idx < len(self.target_list) - 1:
            self.target = self.target_list[idx + 1]
        else:
            self.target = self.target_list[idx - 1]

class ShootDown(Shooter):
    def choose_target(self):
        self.target_list.sort()
        idx = self.target_list.index(self.name)
        self.target = self.target_list[idx - 1] if idx > 0 else self.target_list[-1]

class ShootUpRound(Shooter):
    def choose_target(self):
        self.target_list.sort()
        idx = self.target_list.index(self.name)
        self.target = self.target_list[(idx + 1) % len(self.target_list)]

class ShootRandom(Shooter):
    def choose_target(self):
        targets = [x for x in self.target_list if x != self.name]
        self.target = targets[randint(0, len(targets) - 1)]

SHOOTER_CLASSES = {
    'up': ShootUp,
    'down': ShootDown,
    'random': ShootRandom,
    'upRound': ShootUpRound
}

def initialize_game(num_shooters: int, shooter_type: str = 'up') -> List[Shooter]:
    target_list = list(range(1, num_shooters + 1))
    ShooterClass = SHOOTER_CLASSES[shooter_type]
    return [ShooterClass(name=i, probability=i/num_shooters, target_list=target_list) for i in target_list]

def play_round(shooters: List[Shooter], verbose=False) -> List[int]:
    alive_names = [s.name for s in shooters if s.status == 'alive']
    for s in shooters:
        if s.status == 'dead':
            continue
        s.target_list = [x for x in alive_names]
        s.choose_target()
        if s.shoot_target():
            for target_shooter in shooters:
                if target_shooter.name == s.target:
                    target_shooter.status = 'dead'
                    break
        if verbose:
            print(f"{s.name} targeted {s.target}. Hit: {s.shoot_target()}")
    return [s.name for s in shooters if s.status == 'alive']

def play_game(shooters: List[Shooter], verbose=False) -> int:
    round_no = 1
    while True:
        alive = play_round(shooters, verbose=verbose)
        if verbose:
            print(f"End of round {round_no}. Survivors: {alive}")
        if len(alive) == 1:
            return alive[0]
        round_no += 1

def simulate_games(num_games=100, num_shooters=25, shooter_type='up'):
    winners = []
    for _ in tqdm(range(num_games)):
        shooters = initialize_game(num_shooters, shooter_type)
        winner = play_game(shooters)
        winners.append(winner)
    return winners

def plot_results(winners: List[int], num_shooters: int):
    plt.hist(winners, bins=2 * num_shooters + 1)
    plt.xlabel('Shooter ID')
    plt.ylabel('Number of Wins')
    plt.title('Shooter Win Distribution')
    plt.show()

# Run simulation
if __name__ == "__main__":
    NUM_SHOOTERS = 25
    SHOOTER_TYPE = 'up'
    NUM_GAMES = 100

    winner_list = simulate_games(num_games=NUM_GAMES, num_shooters=NUM_SHOOTERS, shooter_type=SHOOTER_TYPE)
    plot_results(winner_list, NUM_SHOOTERS)
