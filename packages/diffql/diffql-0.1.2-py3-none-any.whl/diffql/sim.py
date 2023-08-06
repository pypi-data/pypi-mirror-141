import os
from concurrent.futures import ProcessPoolExecutor
import itertools
import numpy as np
from pathlib import Path
import pickle
from diffql.learning import DataBuffer
from diffql.envs.fixed_wing import CCVFighterDTLinearEnv
from diffql.envs.basic import MechanicalDTEnv
import matplotlib.pyplot as plt


def sim(case_number, env, agent, seed=None, dir_log=".", plot_fig=False, save_data=True):
    _dir_log = Path(dir_log, f"env_{case_number:03d}")
    if plot_fig or save_data:
        _dir_log.mkdir(parents=True, exist_ok=True)
    filepath = Path(_dir_log, "data.h5")

    databuffer = DataBuffer()

    state = env.reset(seed=seed)
    action_command_list = []
    info_list = []
    while True:
        action_command = agent(state)
        # action projection
        if not env.action_space.contains(action_command):
            action = np.minimum(action_command, env.action_space.high)
            action = np.maximum(action, env.action_space.low)
        else:
            action = action_command
        time = env.clock.current_time()
        next_state, reward, done, info = env.step(action)
        # data append
        databuffer.append(state, action, reward, next_state, t=time, d=done)
        action_command_list.append(action_command)
        info_list.append(info)

        if done:
            sim_data = {
                "time": databuffer.t,
                "state": databuffer.s,
                "action": databuffer.a,
                "action_command": action_command_list,
                "info": info_list,
            }
            if save_data:
                with open(filepath, "wb") as f:
                    pickle.dump(sim_data, f)
            break
        state = next_state
    env.close()
    if plot_fig:
        _ = plot_figure(sim_data, _dir_log, env)
    return databuffer


def parsim(N, envs, agents, dir_log=".", workers=None, plot_fig=False, save_data=True, seeds=None):
    if seeds is None:
        seeds = [None for i in range(N)]
    if workers is None:
        workers = os.cpu_count()
    # Initialize concurrent
    with ProcessPoolExecutor(workers) as exe:
        results = exe.map(sim, range(1, 1+N), envs, agents, seeds, itertools.repeat(dir_log), itertools.repeat(plot_fig), itertools.repeat(save_data))
    return list(results)


def plot_figure(data, _dir_log, env):
    time = np.array(data["time"])
    if type(env) is CCVFighterDTLinearEnv:
        states_hist = np.rad2deg(np.array(data["state"])).T.tolist()
        actions_hist = np.rad2deg(np.array(data["action"])).T.tolist()
        action_commands_hist = np.rad2deg(np.array(data["action_command"])).T.tolist()
        state_ylabels = ['AOA (deg)', 'q (deg/s)', r'$\gamma$ (deg)']
        action_ylabels = [r'$\delta_{e}$ (deg)', r'$\delta_{f}$ (deg)']
        ylim_states = [(np.rad2deg(env.observation_space.low[i])-1.0, np.rad2deg(env.observation_space.high[i])+1.0) for i in range(env.observation_space_shape[0])]
        for ylim_state in ylim_states:
            if np.isinf(ylim_state[0]):
                ylim_states = None
                break
            if np.isinf(ylim_state[1]):
                ylim_states = None
                break
        ylim_actions = [(np.rad2deg(env.action_space.low[i])-5.0, np.rad2deg(env.action_space.high[i])+5.0) for i in range(env.action_space_shape[0])]
        for ylim_action in ylim_actions:
            if np.isinf(ylim_action[0]):
                ylim_actions = None
                break
            if np.isinf(ylim_action[1]):
                ylim_actions = None
                break
    elif type(env) is MechanicalDTEnv:
        states_hist = np.array(data["state"]).T.tolist()
        actions_hist = np.array(data["action"]).T.tolist()
        action_commands_hist = np.array(data["action_command"]).T.tolist()
        state_ylabels = [r"$x_{1}$", r"$x_{2}$", r"$x_{3}$", r"$x_{4}$"]
        action_ylabels = [r"$u_{1}$", r"$u_{2}$"]
        ylim_states = [(env.observation_space.low[i]-1.0, env.observation_space.high[i]+1.0) for i in range(env.observation_space_shape[0])]
        for ylim_state in ylim_states:
            if np.isinf(ylim_state[0]):
                ylim_states = None
                break
            if np.isinf(ylim_state[1]):
                ylim_states = None
                break
        ylim_actions = [(env.action_space.low[i]-1.0, env.action_space.high[i]+1.0) for i in range(env.action_space_shape[0])]
        for ylim_action in ylim_actions:
            if np.isinf(ylim_action[0]):
                ylim_actions = None
                break
            if np.isinf(ylim_action[1]):
                ylim_actions = None
                break
    else:
        states_hist = np.array(data["state"]).T.tolist()
        actions_hist = np.array(data["action"]).T.tolist()
        action_commands_hist = np.array(data["action_command"]).T.tolist()
        state_ylabels = None
        action_ylabels = None
        ylim_states = None
        ylim_actions = None

    # plot states trajectory
    fig1, ax1 = plt.subplots(len(states_hist))
    for i, x in enumerate(states_hist):
        if len(states_hist) == 1:
            _ax1 = ax1
        else:
            _ax1 = ax1[i]
        _ax1.step(time, x, "b-", where="post")
        if state_ylabels is not None:
            _ax1.set_ylabel(state_ylabels[i])
        _ax1.grid()
        if ylim_states is not None:
            _ax1.set_ylim(*ylim_states[i])  # ylim
        if i == len(states_hist)-1:
            _ax1.set_xlabel('Time [sec]')
    plt.suptitle('State trajectory')
    plt.tight_layout()
    plt.savefig(_dir_log.joinpath("state.png"), dpi=150)
    plt.clf()
    plt.close()

    # plot action trajectory
    fig2, ax2 = plt.subplots(len(actions_hist))
    for i, (actions, action_commands) in enumerate(zip(actions_hist, action_commands_hist)):
        if len(actions_hist) == 1:
            _ax2 = ax2
        else:
            _ax2 = ax2[i]
        _ax2.step(time, actions, "b-",
                  where="post", label="action",)
        _ax2.step(time, action_commands, "r--",
                  where="post", label="action_commands",)
        _ax2.legend(loc="upper right")
        if action_ylabels is not None:
            _ax2.set_ylabel(action_ylabels[i])
        _ax2.grid()
        if ylim_actions is not None:
            _ax2.set_ylim(*ylim_actions[i])  # ylim
        if i == len(actions_hist)-1:
            _ax2.set_xlabel('Time [sec]')
    plt.suptitle('action trajectory')
    plt.savefig(_dir_log.joinpath("action.png"), dpi=150)
    plt.clf()
    plt.close()

    figs = {
        "state_hist": fig1,
        "action_hist": fig2
    }
    return figs
