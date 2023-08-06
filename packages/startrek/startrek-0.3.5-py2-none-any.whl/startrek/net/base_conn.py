# -*- coding: utf-8 -*-
#
#   Star Trek: Interstellar Transport
#
#                                Written in 2021 by Moky <albert.moky@gmail.com>
#
# ==============================================================================
# MIT License
#
# Copyright (c) 2021 Albert Moky
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
# ==============================================================================

import socket
import time
import weakref
from typing import Optional

from ..types import Address, AddressPairObject
from ..fsm import StateDelegate

from .channel import Channel
from .connection import Connection
from .delegate import ConnectionDelegate as Delegate
from .state import ConnectionState, StateMachine, TimedConnection


class BaseConnection(AddressPairObject, Connection, TimedConnection, StateDelegate):

    EXPIRES = 16  # seconds

    def __init__(self, remote: Address, local: Optional[Address], channel: Channel, delegate: Delegate):
        super().__init__(remote=remote, local=local)
        self.__channel_ref = None if channel is None else weakref.ref(channel)
        self.__delegate = weakref.ref(delegate)
        # active times
        self.__last_sent_time = 0
        self.__last_received_time = 0
        # Finite State Machine
        self.__fsm: Optional[StateMachine] = None

    def __del__(self):
        # make sure the relative channel is closed
        self._set_channel(channel=None)
        self._set_state_machine(fsm=None)

    def _get_state_machine(self) -> Optional[StateMachine]:
        return self.__fsm

    def _set_state_machine(self, fsm: Optional[StateMachine]):
        # 1. replace with new machine
        old = self.__fsm
        self.__fsm = fsm
        # 2. stop old machine
        if old is not None and old is not fsm:
            old.stop()

    def _create_state_machine(self) -> StateMachine:
        fsm = StateMachine(connection=self)
        fsm.delegate = self
        return fsm

    @property
    def delegate(self) -> Delegate:
        return self.__delegate()

    @property
    def channel(self) -> Optional[Channel]:
        return self._get_channel()

    def _get_channel(self) -> Optional[Channel]:
        ref = self.__channel_ref
        if ref is not None:
            return ref()

    def _set_channel(self, channel: Optional[Channel]):
        # 1. replace with new channel
        old = self._get_channel()
        self.__channel_ref = None if channel is None else weakref.ref(channel)
        # 2. close old channel
        if old is not None and old is not channel:
            if old.opened:
                old.close()

    @property  # Override
    def opened(self) -> bool:
        channel = self.channel
        return channel is not None and channel.opened

    @property  # Override
    def bound(self) -> bool:
        channel = self.channel
        return channel is not None and channel.bound

    @property  # Override
    def connected(self) -> bool:
        channel = self.channel
        return channel is not None and channel.connected

    @property  # Override
    def alive(self) -> bool:
        # channel = self.channel
        # return channel is not None and channel.alive
        return self.opened and (self.connected or self.bound)

    @property  # Override
    def remote_address(self) -> Address:  # (str, int)
        return self._remote

    @property  # Override
    def local_address(self) -> Optional[Address]:  # (str, int)
        channel = self._get_channel()
        return self._local if channel is None else channel.local_address

    # Override
    def close(self):
        self._set_channel(channel=None)
        self._set_state_machine(fsm=None)

    @property  # Override
    def last_sent_time(self) -> int:
        return self.__last_sent_time

    @property  # Override
    def last_received_time(self) -> int:
        return self.__last_received_time

    # Override
    def is_sent_recently(self, now: int) -> bool:
        return now < self.__last_sent_time + self.EXPIRES

    # Override
    def is_received_recently(self, now: int) -> bool:
        return now < self.__last_received_time + self.EXPIRES

    # Override
    def is_long_time_not_received(self, now: int) -> bool:
        return now > self.__last_received_time + (self.EXPIRES << 3)

    # Override
    def received(self, data: bytes, remote: Optional[Address], local: Optional[Address]):
        self.__last_received_time = int(time.time())
        delegate = self.delegate
        if delegate is not None:
            delegate.connection_received(data=data, source=remote, destination=local, connection=self)

    def _send(self, data: bytes, target: Optional[Address]) -> int:
        channel = self.channel
        if channel is None or not channel.alive:
            # raise socket.error('socket channel lost: %s' % channel)
            return -1
        sent = channel.send(data=data, target=target)
        if sent > 0:
            self.__last_sent_time = int(time.time())
        return sent

    # Override
    def send(self, data: bytes, target: Optional[Address] = None) -> int:
        # try to send data
        error = None
        sent = -1
        try:
            sent = self._send(data=data, target=target)
            if sent < 0:  # == -1:
                error = ConnectionError('failed to send: %d byte(s) to %s' % (len(data), target))
        except socket.error as e:
            error = e
            # socket error, close current channel
            self._set_channel(channel=None)
        # callback
        delegate = self.delegate
        if delegate is not None:
            local = self.local_address
            if error is None:
                if sent <= 0:
                    data = b''
                elif sent < len(data):
                    data = data[:sent]
                delegate.connection_sent(data=data, source=local, destination=target, connection=self)
            else:
                delegate.connection_error(error=error, data=data, source=local, destination=target, connection=self)
        return sent

    #
    #   States
    #

    @property  # Override
    def state(self) -> ConnectionState:
        fsm = self._get_state_machine()
        if fsm is None:
            return ConnectionState.ERROR
        else:
            return fsm.current_state

    # Override
    def tick(self):
        fsm = self._get_state_machine()
        if fsm is not None:
            # drive state machine forward
            fsm.tick()

    def start(self):
        fsm = self._create_state_machine()
        fsm.start()
        self._set_state_machine(fsm=fsm)

    def stop(self):
        self._set_channel(channel=None)
        self._set_state_machine(fsm=None)

    #
    #   StateDelegate
    #

    # Override
    def enter_state(self, state: ConnectionState, ctx: StateMachine):
        pass

    # Override
    def exit_state(self, state: ConnectionState, ctx: StateMachine):
        current = ctx.current_state
        if current == ConnectionState.READY:
            if state != ConnectionState.MAINTAINING:
                # change state to 'connected', reset times to just expired
                timestamp = int(time.time()) - self.EXPIRES - 1
                self.__last_sent_time = timestamp
                self.__last_received_time = timestamp
        # callback
        delegate = self.delegate
        if delegate is not None:
            delegate.connection_state_changed(previous=state, current=current, connection=self)

    # Override
    def pause_state(self, state: ConnectionState, ctx: StateMachine):
        pass

    # Override
    def resume_state(self, state: ConnectionState, ctx: StateMachine):
        pass
