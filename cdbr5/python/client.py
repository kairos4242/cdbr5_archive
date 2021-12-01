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

def send_and_receive(int_to_send = random.randint(1, 128)):
    #data is a u16
    message = 50
    data = int_to_send
    buffer_type = buffer_u8+buffer_u16
    buffer = struct.pack('<'+buffer_type,*[message,data])

    s.send(buffer)
    #time.sleep(.1)
    data = s.recv(2048)
    #this was initially 1024, as the size of the buffer game maker is supposedly sending over is 1024
    #however, game maker turned out to actually be sending a larger packet than that, the precise size I'm not sure of
    #it was causing every second request to fail as there was still unread junk in the buffer it was reading instead of the new packet it thought it was reading
    print('Received raw', repr(data))
    print('Received', repr(data)[50:])
    print('Sanitized received: ', parse_buffer(repr(data)[50:]))
    return parse_buffer(repr(data)[50:])

def send_reset():
  return send_and_receive(MAX_INT_SIZE - 1)

def send_no_action():
  return send_and_receive(MAX_INT_SIZE - 2)

def test_timing():
    time_val = timeit.timeit("send_and_receive()", "from __main__ import send_and_receive; import random", number=1000)
    print("Time: " + str(time_val) + " seconds")

def parse_buffer(buffer_to_parse):
  #handles parsing the data that game maker sends back, returns an array of the game state
  chopped_buffer = buffer_to_parse.partition("\\")[0]
  arrayed_buffer = chopped_buffer.split(",")
  return [int(i) for i in arrayed_buffer]

#sending a MAX_SIZE is sending a reset, sending a MAX_SIZE - 1 is sending just a request for information with no action taken
#0,1,2 and 3 are movement in one of the four directions, currently coding that logic in the thing
#in future all the ints 4+ will be abilities and suchlike

TCP_IP = '127.0.0.1'
TCP_PORT = 8008

buffer_u16 = "H"
buffer_u8 = "b"

MAX_INT_SIZE = 65536

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
for i in range(3):
  time.sleep(5)
  response = send_and_receive(1)
  print(f"Response: {response}")
response = send_reset()
print(f"Response: {response}")
#s.close()

class CDBREnv(py_environment.PyEnvironment):

  def __init__(self):
    self._action_spec = array_spec.BoundedArraySpec(
        shape=(), dtype=np.int32, minimum=0, maximum=3, name='action')
    self._observation_spec = array_spec.BoundedArraySpec(
        shape=(2,), dtype=np.int32, minimum=0, name='observation')
    self._state = send_no_action()
    self._episode_ended = False

  def action_spec(self):
    return self._action_spec

  def observation_spec(self):
    return self._observation_spec

  def _reset(self):
    self._state = 0
    self._episode_ended = False
    send_reset()#should this be here? worth looking into
    return ts.restart(np.array([self._state], dtype=np.int32))

  def _step(self, action):

    if self._episode_ended:
      # The last action ended the episode. Ignore the current action and start
      # a new episode.
      return self.reset()

    # Make sure episodes don't go on forever.
    if action == 3:
        #move left
        self._state = send_and_receive(3)
    if action== 2:
        #move down
        self._state = send_and_receive(2)
    if action == 1:
      #move right
      self._state = send_and_receive(1)
    elif action == 0:
      #move up
      self._state = send_and_receive(0)
    else:
      raise ValueError('`action` should be 0, 1, 2 or 3.')

    if self._episode_ended or (self._state == [0, 0]):
      reward = self._state - 21 if self._state <= 21 else -21
      return ts.termination(np.array([self._state], dtype=np.int32), reward)
    else:
      return ts.transition(
          np.array([self._state], dtype=np.int32), reward=0.0, discount=1.0)