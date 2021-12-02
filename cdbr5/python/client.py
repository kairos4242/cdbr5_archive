import socket
import struct
import time
import timeit
import random


import abc
import tensorflow as tf
import numpy as np

from tf_agents.environments import py_environment
from tf_agents.environments import tf_environment
from tf_agents.environments import tf_py_environment
from tf_agents.environments import utils
from tf_agents.specs import array_spec
from tf_agents.environments import wrappers
from tf_agents.environments import suite_gym
from tf_agents.trajectories import time_step as ts

#sending a MAX_SIZE is sending a reset, sending a MAX_SIZE - 1 is sending just a request for information with no action taken
#0,1,2 and 3 are movement in one of the four directions, currently coding that logic in the thing
#in future all the ints 4+ will be abilities and suchlike

#s.close()

class CDBREnv(py_environment.PyEnvironment):

  def __init__(self):
    self._action_spec = array_spec.BoundedArraySpec(
        shape=(), dtype=np.int32, minimum=0, maximum=3, name='action')
    self._observation_spec = array_spec.BoundedArraySpec(
        shape=(1,4), dtype=np.int32, minimum=0, maximum=1366, name='observation')
    self._episode_ended = False
    self._current_time_step = None

    #custom stuff for init
    self.TCP_IP = '127.0.0.1'
    self.TCP_PORT = 8008

    self.buffer_u16 = "H"
    self.buffer_u8 = "b"

    self.MAX_INT_SIZE = 65536

    self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.s.connect((self.TCP_IP, self.TCP_PORT))
    self._state = self.send_no_action()

  def close_socket(self):
    self.s.close()

  def send_and_receive(self, int_to_send = random.randint(1, 128)):
    #data is a u16
    message = 50
    data = int_to_send
    buffer_type = self.buffer_u8+self.buffer_u16
    buffer = struct.pack('<'+buffer_type,*[message,data])

    self.s.send(buffer)
    #time.sleep(.1)
    data = self.s.recv(2048)
    #this was initially 1024, as the size of the buffer game maker is supposedly sending over is 1024
    #however, game maker turned out to actually be sending a larger packet than that, the precise size I'm not sure of
    #it was causing every second request to fail as there was still unread junk in the buffer it was reading instead of the new packet it thought it was reading
    #print('Received raw', repr(data))
    #print('Received', repr(data)[50:])
    #print('Sanitized received: ', self.parse_buffer(repr(data)[50:]))
    return self.parse_buffer(repr(data)[50:])

  def send_reset(self):
    return self.send_and_receive(self.MAX_INT_SIZE - 1)

  def send_no_action(self):
    return self.send_and_receive(self.MAX_INT_SIZE - 2)

  def test_timing(self):
      time_val = timeit.timeit("send_and_receive()", "from __main__ import send_and_receive; import random", number=1000)
      print("Time: " + str(time_val) + " seconds")

  def parse_buffer(self,buffer_to_parse):
    #handles parsing the data that game maker sends back, returns an array of the game state
    chopped_buffer = buffer_to_parse.partition("\\")[0]
    arrayed_buffer = chopped_buffer.split(",")
    return [int(i) for i in arrayed_buffer]

  def action_spec(self):
    return self._action_spec

  def observation_spec(self):
    return self._observation_spec

  def _reset(self):
    self._episode_ended = False
    self.send_reset()#should this be here? worth looking into
    return ts.restart(np.array([self._state], dtype=np.int32))

  def _step(self, action):

    if self._episode_ended:
      # The last action ended the episode. Ignore the current action and start
      # a new episode.
      return self.reset()

    if action == 3:
        #move down
        self._state = self.send_and_receive(3)
    elif action == 2:
        #move left
        self._state = self.send_and_receive(2)
    elif action == 1:
      #move up
      self._state = self.send_and_receive(1)
    elif action == 0:
      #move right
      self._state = self.send_and_receive(0)
    else:
      raise ValueError(f'`action` should be 0, 1, 2 or 3. Instead, it is {action}')

    if self._episode_ended or (self._state == [0, 0, 0, 0]):
      #this reward is wrong, maybe we should have a third val on our observation spec for a ticking clock, and rewards decline based on how long it takes before the agent can find them
      #or maybe compare our agents performance to optimal performance and penalize them based on how suboptimal their performance is
      reward = 1#temp, why not
      self._episode_ended = True
      return ts.termination(np.array([self._state], dtype=np.int32), reward)
    else:
      return ts.transition(
          np.array([self._state], dtype=np.int32), reward=0.0, discount=1.0)


#let's see if just doing this without any qualifiers works?
env = CDBREnv()
utils.validate_py_environment(env, episodes=5)

external_state = env.send_no_action()
""" for i in range(100):
  time.sleep(0.2)
  if external_state[0] == 1:
    #env.step(0)
    external_state = env.step(0).observation.tolist()[0]
  elif external_state[0] == -1:
    external_state = env.step(2).observation.tolist()[0]
    #env.step(2)
  elif external_state[1] == 1:
    external_state = env.step(1).observation.tolist()[0]
    #env.step(1)
  elif external_state[1] == -1:
    external_state = env.step(3).observation.tolist()[0]
    #env.step(3)
  elif external_state == [0,0]:
    env._reset()
    external_state = env.send_no_action()
  print(f"Response: {external_state}") """
env.close_socket()