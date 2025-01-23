import os
import sys
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please set SUMO_HOME")

from os.path import dirname, basename, isfile, join
import glob

modules = glob.glob(join(dirname(__file__), "*.py"))
__all__ = [basename(f)[:-3] for f in modules if isfile(f) and not f.endswith('__init__.py')]


# Registration for EPyMARL
from gym.envs.registration import register
from resco_benchmark.multi_signal import MultiSignal
from resco_benchmark.config.map_config import map_configs
from resco_benchmark import states
from resco_benchmark import rewards


pwd = dirname(__file__)
log_dir = os.getcwd()

maps = [
    'grid4x4', 'arterial4x4',
    'ingolstadt1', 'ingolstadt7', 'ingolstadt21',
    'cologne1',
    'cologne3', 'cologne3_train', 'cologne3_low', 'cologne3_medium', 'cologne3_high',
    'cologne3_v2_train', 'cologne3_v2_low', 'cologne3_v2_medium', 'cologne3_v2_high',
    'cologne8', 'cologne8_train', 'cologne8_low', 'cologne8_medium', 'cologne8_high',
    'cologne8_v2_train', 'cologne8_v2_low', 'cologne8_v2_medium', 'cologne8_v2_high',
    'grid5_train', 'grid5_low', 'grid5_medium', 'grid5_high',
    'grid3x3_train', 'grid3x3_low', 'grid3x3_medium', 'grid3x3_high',
    'grid3x3_v2_train', 'grid3x3_v2_low', 'grid3x3_v2_medium', 'grid3x3_v2_high',
    'grid3x6_train', 'grid3x6_low', 'grid3x6_medium', 'grid3x6_high',
]
algs = ['ia2c', 'ippo', 'maa2c', 'mappo', 'coma', 'iql', 'maddpg', 'qmix', 'vdn', 'ia2c_ns', 'ippo_ns', 'maa2c_ns', 'mappo_ns', 'coma_ns', 'iql_ns', 'maddpg_ns', 'qmix_ns', 'vdn_ns']
for alg in algs:
    for map in maps:
        for trial in range(1, 30):
            map_config = map_configs[map]
            num_steps_eps = int((map_config['end_time'] - map_config['start_time']) / map_config['step_length'])
            route = map_config['route']
            if route is not None: route = join(pwd, route)

            name = alg+'-tr' + str(trial)
            network_file = join(pwd, map_config['net'])
            register(
                id=map+"-"+alg+"-v" + str(trial),
                entry_point="resco_benchmark.multi_signal:MultiSignal",
                kwargs={
                    'run_name': name,
                    'map_name': map,
                    'net': network_file,
                    'state_fn': states.drq_norm,
                    'reward_fn': rewards.wait_norm,
                    'route': route,
                    'gui': False,
                    'end_time': map_config['end_time'],
                    'step_length': 10,
                    'yellow_length': 4,
                    'step_ratio': 1,
                    'max_distance': 200,
                    'lights': (),
                    'log_dir': log_dir,
                    'libsumo': False,
                    'warmup': 0,
                    'gymma': True
                },
        )
