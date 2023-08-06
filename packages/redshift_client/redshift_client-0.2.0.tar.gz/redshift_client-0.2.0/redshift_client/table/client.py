from dataclasses import (
    dataclass,
)
from fa_purity.cmd import (
    Cmd,
)
from fa_purity.frozen import (
    FrozenDict,
)
from redshift_client.sql_client.core import (
    SqlClient,
)
from redshift_client.sql_client.query import (
    dynamic_query,
)
from redshift_client.table.core import (
    TableId,
)


@dataclass(frozen=True)
class ManifestId:
    uri: str


@dataclass(frozen=True)
class TableClient:
    _db_client: SqlClient

    def unload(
        self, table: TableId, prefix: str, role: str
    ) -> Cmd[ManifestId]:
        """
        prefix: a s3 uri prefix
        role: an aws role id-arn
        """
        stm = (
            "UNLOAD ('SELECT * FROM {schema}.{table}')"
            "TO %(prefix)s iam_role %(role)s MANIFEST"
        )
        return self._db_client.execute(
            dynamic_query(
                stm,
                FrozenDict({"schema": table.schema.name, "table": table.name}),
            ),
            FrozenDict({"prefix": prefix, "role": role}),
        ).map(lambda _: ManifestId(f"{prefix}manifest"))

    def load(
        self, table: TableId, manifest: ManifestId, role: str
    ) -> Cmd[None]:
        stm = (
            "COPY {schema}.{table} FROM %(manifest_file)s"
            "iam_role %(role)s MANIFEST"
        )
        return self._db_client.execute(
            dynamic_query(
                stm,
                FrozenDict({"schema": table.schema.name, "table": table.name}),
            ),
            FrozenDict({"manifest_file": manifest.uri, "role": role}),
        )
