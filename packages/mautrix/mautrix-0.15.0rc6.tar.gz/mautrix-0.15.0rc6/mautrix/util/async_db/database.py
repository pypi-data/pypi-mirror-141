# Copyright (c) 2022 Tulir Asokan
#
# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at http://mozilla.org/MPL/2.0/.
from __future__ import annotations

from typing import Any, AsyncContextManager, Type
from abc import ABC, abstractmethod
import logging
import sys

from yarl import URL

from mautrix import __optional_imports__
from mautrix.util.logging import TraceLogger

from .connection import LoggingConnection
from .scheme import Scheme
from .upgrade import UpgradeTable, upgrade_tables

if __optional_imports__:
    from asyncpg import Record


class Database(ABC):
    schemes: dict[str, Type[Database]] = {}
    log: TraceLogger

    scheme: Scheme
    url: URL
    _db_args: dict[str, Any]
    upgrade_table: UpgradeTable

    def __init__(
        self,
        url: URL,
        upgrade_table: UpgradeTable,
        db_args: dict[str, Any] | None = None,
        log: TraceLogger | None = None,
    ) -> None:
        self.url = url
        self._db_args = {**db_args} if db_args else {}
        self.upgrade_table = upgrade_table
        self.log = log or logging.getLogger("mau.db")
        assert isinstance(self.log, TraceLogger)

    @classmethod
    def create(
        cls,
        url: str | URL,
        *,
        db_args: dict[str, Any] | None = None,
        upgrade_table: UpgradeTable | str | None = None,
        log: logging.Logger | TraceLogger | None = None,
    ) -> Database:
        url = URL(url)
        try:
            impl = cls.schemes[url.scheme]
        except KeyError as e:
            if url.scheme in ("postgres", "postgresql"):
                raise RuntimeError(
                    f"Unknown database scheme {url.scheme}."
                    " Perhaps you forgot to install asyncpg?"
                ) from e
            elif url.scheme in ("sqlite", "sqlite3"):
                raise RuntimeError(
                    f"Unknown database scheme {url.scheme}."
                    " Perhaps you forgot to install aiosqlite?"
                ) from e
            raise RuntimeError(f"Unknown database scheme {url.scheme}") from e
        if isinstance(upgrade_table, str):
            upgrade_table = upgrade_tables[upgrade_table]
        elif upgrade_table is None:
            upgrade_table = UpgradeTable()
        elif not isinstance(upgrade_table, UpgradeTable):
            raise ValueError(f"Can't use {type(upgrade_table)} as the upgrade table")
        return impl(url, db_args=db_args, upgrade_table=upgrade_table, log=log)

    def override_pool(self, db: Database) -> None:
        pass

    async def start(self) -> None:
        try:
            await self.upgrade_table.upgrade(self)
        except Exception:
            self.log.critical("Failed to upgrade database", exc_info=True)
            sys.exit(25)

    @abstractmethod
    async def stop(self) -> None:
        pass

    @abstractmethod
    def acquire(self) -> AsyncContextManager[LoggingConnection]:
        pass

    async def execute(self, query: str, *args: Any, timeout: float | None = None) -> str:
        async with self.acquire() as conn:
            return await conn.execute(query, *args, timeout=timeout)

    async def executemany(self, query: str, *args: Any, timeout: float | None = None) -> str:
        async with self.acquire() as conn:
            return await conn.executemany(query, *args, timeout=timeout)

    async def fetch(self, query: str, *args: Any, timeout: float | None = None) -> list[Record]:
        async with self.acquire() as conn:
            return await conn.fetch(query, *args, timeout=timeout)

    async def fetchval(
        self, query: str, *args: Any, column: int = 0, timeout: float | None = None
    ) -> Any:
        async with self.acquire() as conn:
            return await conn.fetchval(query, *args, column=column, timeout=timeout)

    async def fetchrow(self, query: str, *args: Any, timeout: float | None = None) -> Record:
        async with self.acquire() as conn:
            return await conn.fetchrow(query, *args, timeout=timeout)
