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

import time
import weakref
from abc import abstractmethod
from typing import Optional, List

from .types import Address, AddressPairObject
from .net import Connection
from .port import Arrival, Departure
from .port import Docker, Gate, GateDelegate

from .dock import Dock, LockedDock


class StarDocker(AddressPairObject, Docker):
    """
        Star Docker
        ~~~~~~~~~~~

        @abstract properties:
            connection()
            delegate()

        @abstract methods:
            - pack(payload, priority)
            - heartbeat()
            - _get_arrival(data)
            - _check_arrival(ship)
    """

    def __init__(self, remote: Address, local: Optional[Address], gate: Gate):
        super().__init__(remote=remote, local=local)
        self.__gate_ref = weakref.ref(gate)
        self.__dock = self._create_dock()
        self.__conn_ref = None
        # remaining data to be sent
        self.__last_outgo: Optional[Departure] = None
        self.__last_fragments: List[bytes] = []

    def __del__(self):
        # make sure the relative connection is closed
        self._set_connection(connection=None)
        self.__dock = None

    # noinspection PyMethodMayBeStatic
    def _create_dock(self) -> Dock:
        """ Override for user-customized dock """
        return LockedDock()

    @property  # protected
    def gate(self) -> Gate:
        return self.__gate_ref()

    @property  # protected
    def delegate(self) -> Optional[GateDelegate]:
        return self.gate.delegate

    @property  # protected
    def connection(self) -> Optional[Connection]:
        conn = self._get_connection()
        if conn is None and self.__dock is not None:
            # docker not closed, get new connection from the gate
            conn = self.gate.get_connection(remote=self._remote, local=self._local)
            self._set_connection(connection=conn)
        return conn

    def _get_connection(self) -> Optional[Connection]:
        ref = self.__conn_ref
        if ref is not None:
            return ref()

    def _set_connection(self, connection: Optional[Connection]):
        # 1. replace with new connection
        old = self._get_connection()
        self.__conn_ref = None if connection is None else weakref.ref(connection)
        # 2. close old connection
        if old is not None and old is not connection:
            if old.opened:
                old.close()

    @property  # Override
    def alive(self) -> bool:
        conn = self.connection
        return conn is not None and conn.alive

    @property  # Override
    def remote_address(self) -> Address:  # (str, int)
        return self._remote

    @property  # Override
    def local_address(self) -> Optional[Address]:  # (str, int)
        conn = self._get_connection()
        return self._local if conn is None else conn.local_address

    # Override
    def process(self) -> bool:
        # 1. get connection which is ready for sending data
        conn = self.connection
        if conn is None or not conn.alive:
            # waiting for connection
            return False
        # 2. get data waiting to be sent out
        if len(self.__last_fragments) > 0:
            # get remaining fragments from last outgo task
            outgo = self.__last_outgo
            fragments = self.__last_fragments
            self.__last_outgo = None
            self.__last_fragments = []
        else:
            # get next outgo task
            now = int(time.time())
            outgo = self._next_departure(now=now)
            if outgo is None:
                # nothing to do now, return False to let the thread have a rest
                return False
            elif outgo.is_failed(now=now):
                # task timeout, return True to process next one
                error = TimeoutError('Request timeout')
                self.__outgo_error(error=error, ship=outgo, connection=self.connection)
                return True
            else:
                # get fragments from outgo task
                fragments = outgo.fragments
                if len(fragments) == 0:
                    # all fragments of this task have been sent already
                    # return True to process next one
                    return True
        # 3. process fragments of outgo task
        index = 0
        sent = 0
        try:
            remote = self.remote_address
            for fra in fragments:
                sent = conn.send(data=fra, target=remote)
                if sent < len(fra):
                    # buffer overflow?
                    break
                else:
                    # assert sent == len(fra)
                    index += 1
                    sent = 0  # clear counter
            if index < len(fragments):
                # task failed
                error = ConnectionError('only %d/%d fragments sent' % (index, len(fragments)))
            else:
                # task done
                return True
        except Exception as e:
            # socket error, callback
            error = e
        # 4. remove sent fragments
        while index > 0:
            fragments.pop(0)
            index -= 1
        # remove partially sent data of next fragment
        if sent > 0:
            last = fragments.pop(0)
            fragments.insert(0, last[sent:])
        # 5. store remaining data
        self.__last_outgo = outgo
        self.__last_fragments = fragments
        # 6. callback for error
        self.__outgo_error(error=error, ship=outgo, connection=conn)

    def __outgo_error(self, error: IOError, ship: Departure, connection: Connection):
        # callback for error
        delegate = self.delegate
        if delegate is not None:
            remote = self.remote_address
            local = self.local_address
            delegate.gate_error(error=error, ship=ship, source=local, destination=remote, connection=connection)

    # Override
    def process_received(self, data: bytes):
        # 1. get income ship from received data
        income = self._get_arrival(data=data)
        if income is None:
            # waiting for more data
            return None
        # 2. check income ship for response
        income = self._check_arrival(ship=income)
        if income is None:
            return None
        # 3. callback for processing income ship with completed data package
        delegate = self.delegate
        if delegate is not None:
            remote = self.remote_address
            local = self.local_address
            conn = self.connection
            delegate.gate_received(ship=income, source=remote, destination=local, connection=conn)

    @abstractmethod
    def _get_arrival(self, data: bytes) -> Optional[Arrival]:
        """
        Get income ship from received data

        :param data: received data
        :return income ship carrying data package/fragment
        """
        raise NotImplemented

    @abstractmethod
    def _check_arrival(self, ship: Arrival) -> Optional[Arrival]:
        """
        Check income ship for responding

        :param ship: income ship carrying data package/fragment/response
        :return income ship carrying completed data package
        """
        raise NotImplemented

    def _check_response(self, ship: Arrival) -> Optional[Departure]:
        """ Check and remove linked departure ship with same SN (and page index for fragment) """
        # check response for linked departure ship (same SN)
        linked = self.__dock.check_response(ship=ship)
        if linked is None:
            # linked departure task not found, or not finished yet
            return None
        # all fragments responded, task finished
        delegate = self.delegate
        if delegate is not None:
            remote = self.remote_address
            local = self.local_address
            conn = self.connection
            delegate.gate_sent(ship=linked, source=local, destination=remote, connection=conn)
        return linked

    def _assemble_arrival(self, ship: Arrival) -> Optional[Arrival]:
        """ Check received ship for completed package """
        return self.__dock.assemble_arrival(ship=ship)

    def _next_departure(self, now: int) -> Optional[Departure]:
        """ Get outgo ship from waiting queue """
        # this will be remove from the queue,
        # if needs retry, the caller should append it back
        return self.__dock.next_departure(now=now)

    # Override
    def append_departure(self, ship: Departure) -> bool:
        """ Append outgo Ship to the waiting queue """
        return self.__dock.append_departure(ship=ship)

    # Override
    def purge(self):
        """ Clear expired tasks """
        self.__dock.purge()

    # Override
    def close(self):
        self._set_connection(connection=None)
        self.__dock = None
