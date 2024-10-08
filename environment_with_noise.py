# environment_with_noise.py

import gymnasium as gym
import numpy as np
import matplotlib.pyplot as plt
import math
import argparse

class NoisyObservationWrapper(gym.ObservationWrapper):
    def __init__(self, env, noise_std=0.1):
        super(NoisyObservationWrapper, self).__init__(env)
        self.noise_std = noise_std
        self.observation_space = env.observation_space
        
        # Define the range for each observation component
        self.obs_ranges = [
            2.4,  # cart position range is [-2.4, 2.4]
            0.5,  # cart velocity range is approximated as [-50, 50]
            math.radians(12),  # pole angle range is [-12 degrees, 12 degrees]
            math.radians(0.5)  # pole angular velocity range is approximated as [-50 degrees/s, 50 degrees/s]
        ]

    def observation(self, obs):
        noise = np.random.normal(0, self.noise_std, size=obs.shape) * self.obs_ranges
        noisy_obs = obs + noise
        return noisy_obs

def setup_noisy_environment(noise_std=0.1):
    """
    Sets up the CartPole-v1 environment with noisy observations and runs a random policy to test it.
    """
    # Initialize the CartPole-v1 environment with and without noisy observations
    env = gym.make('CartPole-v1')
    noisy_env = NoisyObservationWrapper(env, noise_std)

    cart_positions = []
    pole_angles = []
    noisy_cart_positions = []
    noisy_pole_angles = []

    # Run a single episode with a random policy in the noisy environment
    observation, info = noisy_env.reset()
    done = False

    while not done:
        action = noisy_env.action_space.sample()  # Random action
        noisy_observation, reward, done, _, _ = noisy_env.step(action)
        observation, reward, done, _, _ = env.step(action)
        
        cart_positions.append(observation[0])  # Ground truth cart position
        pole_angles.append(observation[2])  # Ground truth pole angle
        noisy_cart_positions.append(noisy_observation[0])  # Noisy cart position
        noisy_pole_angles.append(noisy_observation[2])  # Noisy pole angle
        print(f"Noisy Observation: {noisy_observation} | Ground Truth: {observation} | Reward: {reward} | Done: {done}")

    env.close()
    noisy_env.close()

    # Plot the cart positions and pole angles
    plot_comparisons(cart_positions, noisy_cart_positions, pole_angles, noisy_pole_angles)


def plot_comparisons(cart_positions, noisy_cart_positions, pole_angles, noisy_pole_angles):
    """
    Plots the ground truth and noisy cart positions and pole angles over time.
    """
    time_steps = range(len(cart_positions))

    plt.figure(figsize=(12, 6))

    plt.subplot(2, 1, 1)
    plt.plot(time_steps, cart_positions, label='Ground Truth Cart Position')
    plt.plot(time_steps, noisy_cart_positions, label='Noisy Cart Position', linestyle='--')
    plt.xlabel('Time Steps')
    plt.ylabel('Cart Position')
    plt.title('Cart Position over Time')
    plt.legend()

    plt.subplot(2, 1, 2)
    plt.plot(time_steps, pole_angles, label='Ground Truth Pole Angle')
    plt.plot(time_steps, noisy_pole_angles, label='Noisy Pole Angle', linestyle='--')
    plt.xlabel('Time Steps')
    plt.ylabel('Pole Angle (radians)')
    plt.title('Pole Angle over Time')
    plt.legend()

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Set the noise standard deviation level for the environment.")
    parser.add_argument('--noise_std', type=float, default=0.1, help='Standard deviation of the noise to be added to observations.')
    args = parser.parse_args()

    setup_noisy_environment(noise_std=args.noise_std)
