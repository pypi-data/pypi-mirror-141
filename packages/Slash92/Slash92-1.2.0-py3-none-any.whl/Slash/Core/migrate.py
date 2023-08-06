import hashlib
import json
import copy
import os

from migration_templates import (
    STANDART_JSON_CONFIG,
    MIGRATION_BLOCK
)
from ..types_ import (
    BasicTypes, TablesManager, TableMeta
)


class MigrationTableBlock:
    def __init__(self, name, columns, path):
        self.__name = name
        self.__columns = columns

    def get_table_block(self):
        return [
            {
                self.__name: list(
                    zip(
                        [c.name for c in self.__columns],
                        [BasicTypes.DB_TYPES_LIST[c.type] for c in self.__columns]
                    )
                )
            },
            "".join([c.name for c in self.__columns])
        ]

        return (self.__name, [c.name for c in self.__columns])


class MigrationCore:
    def __init__(self, path_) -> None:
        if not os.path.exists(path_):
            os.mkdir(path_)
            with open(path_+"/config.json", "w") as file_:
                json.dump(STANDART_JSON_CONFIG, file_, indent=4)
        self.__migrations_folder = path_

    @property
    def path(self):
        return self.__migrations_folder

    def make_migrations(self):
        if TableMeta.COUNT_OF_TABLE_OBJECTS == TableMeta.COUNT_OF_TABLE_TEMPLATES:
            config: dict = self._read_config_file()
            merged_table_blocks: dict = {}
            column_names: str = ""

            for table in TablesManager.tables.values():
                tables_block = MigrationTableBlock(
                        table.name, table.columns, self.path
                    ).get_table_block()

                merged_table_blocks.update(tables_block[0])
                column_names += tables_block[1]

            if config["count_of_blocks"] == 0:
                self._make_migration_block(config, merged_table_blocks, column_names)
                config["count_of_blocks"] += 1
            else:
                current_signature: set = set()
                last_signature: set = set()

                for key in merged_table_blocks.keys():
                    current_signature.add(key)
                    current_signature.add("".join([i[0] for i in merged_table_blocks[key]]))

                last_block: dict = config["blocks"][f"migration_{config['count_of_blocks']-1}"]
                for key in last_block["tables"].keys():
                    last_signature.add(key)
                    last_signature.add("".join([i[0] for i in last_block["tables"][key]]))

                if (current_signature != last_signature):
                    self._make_migration_block(config, merged_table_blocks, column_names, last_block["hash"])

                    config["count_of_blocks"] += 1
            self._write_config_file(config)

    def _make_migration_block(self, globla_config: dict, table_blocks: dict, columns_names: str, last_hash: str=""):
        new_migration: dict = copy.deepcopy(MIGRATION_BLOCK)
        new_migration["is_first"] = True if not last_hash else False
        new_migration["table_count"] = len(table_blocks)
        new_migration["tables"].update(table_blocks)

        new_migration["hash"] = hashlib.sha512(
            (
                last_hash + "".join([k for k in table_blocks.keys()]) + columns_names
            ).encode("utf-8")
        ).hexdigest()

        globla_config["blocks"].update(
            {
               "migration_"+str(globla_config["count_of_blocks"]): new_migration
           }
        )
        globla_config["last_hash"] = new_migration["hash"]

    def _read_config_file(self):
        if os.path.exists(self.__migrations_folder + "\\config.json"):
            with open(self.__migrations_folder + "\\config.json") as json_configs:
                return json.load(json_configs)
        else:
            raise FileExistsError(f"\n\tConfig file is not found...\n\t\t{self.__migrations_folder}\config.json")

    def _write_config_file(self, data):
        with open(self.__migrations_folder + "\\config.json", "w") as json_configs:
            json.dump(data, json_configs, indent=4)
