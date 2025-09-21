"""
Neo4j database connection and session management.
"""
import logging
from typing import Optional, Dict, Any, List, cast, TYPE_CHECKING

if TYPE_CHECKING:
    from neo4j import Query
else:
    Query = str
from contextlib import asynccontextmanager

from neo4j import GraphDatabase, Driver
from neo4j.exceptions import ServiceUnavailable, AuthError

logger = logging.getLogger(__name__)


class Neo4jConnection:
    """
    Neo4j database connection manager with connection pooling.
    """

    def __init__(self):
        self._driver: Optional[Driver] = None
        self._uri: Optional[str] = None
        self._username: Optional[str] = None
        self._password: Optional[str] = None

    def configure(self, uri: str, username: str, password: str):
        """Configure connection parameters."""
        self._uri = uri
        self._username = username
        self._password = password

    async def connect(self):
        """Establish connection to Neo4j database."""
        if not all([self._uri, self._username, self._password]):
            raise ValueError(
                "Database connection not configured. Call configure() first."
            )

        try:
            self._driver = GraphDatabase.driver(
                self._uri,  # type: ignore
                auth=(self._username, self._password),  # type: ignore
                max_connection_lifetime=30 * 60,  # 30 minutes
                max_connection_pool_size=50,
                connection_acquisition_timeout=30,  # 30 seconds
            )

            # Test the connection
            await self.verify_connectivity()
            logger.info(f"Successfully connected to Neo4j at {self._uri}")

        except (ServiceUnavailable, AuthError) as e:
            logger.error(f"Failed to connect to Neo4j: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error connecting to Neo4j: {e}")
            raise

    async def disconnect(self):
        """Close the database connection."""
        if self._driver:
            self._driver.close()
            self._driver = None
            logger.info("Disconnected from Neo4j")

    async def verify_connectivity(self):
        """Verify that the connection to Neo4j is working."""
        if not self._driver:
            raise RuntimeError("No active connection to Neo4j")

        try:
            with self._driver.session() as session:
                result = session.run("RETURN 1 as test")
                record = result.single()
                if record and record["test"] != 1:
                    raise RuntimeError("Connectivity test failed")
                logger.debug("Neo4j connectivity verified")
        except Exception as e:
            logger.error(f"Neo4j connectivity check failed: {e}")
            raise

    @asynccontextmanager
    async def get_session(self):
        """Get a Neo4j session with automatic cleanup."""
        if not self._driver:
            raise RuntimeError("No active connection to Neo4j")

        session = self._driver.session()
        try:
            yield session
        finally:
            session.close()

    async def execute_query(
        self, query: str, parameters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Execute a Cypher query and return results."""
        if not self._driver:
            raise RuntimeError("No active connection to Neo4j")

        async with self.get_session() as session:
            try:
                result = session.run(query, parameters or {})  # type: ignore[arg-type]
                return [record.data() for record in result]
            except Exception as e:
                logger.error(f"Query execution failed: {e}")
                logger.error(f"Query: {query}")
                logger.error(f"Parameters: {parameters}")
                raise

    async def execute_write_query(
        self, query: str, parameters: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """Execute a write Cypher query in a transaction."""
        if not self._driver:
            raise RuntimeError("No active connection to Neo4j")

        def _run_query(tx, query_str, params):
            result = tx.run(query_str, params or {})
            return [record.data() for record in result]

        async with self.get_session() as session:
            try:
                return session.write_transaction(_run_query, query, parameters)
            except Exception as e:
                logger.error(f"Write query execution failed: {e}")
                logger.error(f"Query: {query}")
                logger.error(f"Parameters: {parameters}")
                raise

    @property
    def is_connected(self) -> bool:
        """Check if there's an active connection."""
        return self._driver is not None


# Global connection instance
neo4j_connection = Neo4jConnection()


async def get_neo4j_connection() -> Neo4jConnection:
    """Dependency injection for Neo4j connection."""
    if not neo4j_connection.is_connected:
        raise RuntimeError("Neo4j connection not established")
    return neo4j_connection
