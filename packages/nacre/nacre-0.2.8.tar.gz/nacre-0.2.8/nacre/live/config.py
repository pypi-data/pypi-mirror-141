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

# from typing import Any, Dict, Optional
from typing import Optional

# from nautilus_trader.cache.config import CacheConfig
# from nautilus_trader.infrastructure.config import CacheDatabaseConfig
# from nautilus_trader.live.config import LiveDataEngineConfig
# from nautilus_trader.live.config import LiveExecEngineConfig
# from nautilus_trader.live.config import LiveRiskEngineConfig
from nautilus_trader.live.config import TradingNodeConfig as NautilusTradingNodeConfig

from nacre.components.exposer import ExposerConfig
from nacre.infrastructure.config import PubSubConfig


# from nautilus_trader.persistence.config import PersistenceConfig
# from pydantic import PositiveFloat


class TradingNodeConfig(NautilusTradingNodeConfig):
    """
    Configuration for ``TradingNode`` instances.

    pubsub: PubSubConfig, optional
        The config for external msgbus pubsub
    exposer: ExposerConfig, optional
        The config for exposer
    """

    pubsub: Optional[PubSubConfig] = None
    exposer: Optional[ExposerConfig] = None
