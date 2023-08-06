# -------------------------------------------------------------------------------------------------
#  Copyright (C) 2015-2021 Nautech Systems Pty Ltd. All rights reserved.
#  https://nautechsystems.io
#
#  Licensed under the GNU Lesser General Public License Version 3.0 (the "License");
#  You may not use this file except in compliance with the License.
#  You may obtain a copy of the License at https://www.gnu.org/licenses/lgpl-3.0.en.html
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#  See the License for the specific language governing permissions and
#  limitations under the License.
# -------------------------------------------------------------------------------------------------

import asyncio

from libc.stdint cimport int64_t
from nautilus_trader.core.correctness cimport Condition
from nautilus_trader.live.execution_client cimport LiveExecutionClient as NautilusLiveExecutionClient
from nautilus_trader.model.events.account cimport AccountState
from nautilus_trader.model.identifiers cimport AccountId
from nautilus_trader.msgbus.bus cimport MessageBus

from nacre.model.report_position cimport ReportedAccount


cdef class LiveExecutionClient(NautilusLiveExecutionClient):
    cpdef void _set_venue(self, Venue venue) except *:
        Condition.not_none(venue, "venue")
        self.venue = venue

    cpdef void _set_account_id(self, AccountId account_id) except *:
        Condition.not_none(account_id, "account_id")
        # Override check
        # Condition.equal(self.id.value, account_id.issuer, "id.value", "account_id.issuer")

        self.account_id = account_id

    cpdef void generate_account_snapshot(self, AccountState account_state) except *:
        self._msgbus.publish_c(
            topic=f"events.snapshot.{self.account_id}",
            msg=account_state,
        )

    cpdef void generate_reported_account(self, list positions, list balances, int64_t ts_event) except *:
        account = ReportedAccount(
            account_id=self.account_id,
            positions=positions,
            balances=balances,
            event_id=self._uuid_factory.generate(),
            ts_event=ts_event,
            ts_init=self._clock.timestamp_ns(),
        )
        self._log.debug(f"Received position: {positions}")
        self._log.debug(f"Received balances: {balances}")
        self._send_reported_position_state(account)

    cpdef void _send_reported_position_state(self, ReportedAccount account) except *:
        self._msgbus.publish_c(
            topic=f"reported.position",
            msg=account,
        )
