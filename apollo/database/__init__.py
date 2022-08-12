from dependency_injector import providers

from apollo.database.db import Database as _Database
from apollo.database.db import LibraryManager as _LibraryManager
from apollo.database.db import Connection, RecordSet
from apollo.database.db import DBStructureError, QueryBuildFailed, QueryExecutionFailed


Database = providers.Singleton(_Database)
LibraryManager = providers.Singleton(_LibraryManager)
