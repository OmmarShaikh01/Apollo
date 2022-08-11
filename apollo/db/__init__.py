from dependency_injector import providers

from apollo.db.database import Database as _Database
from apollo.db.database import DBStructureError
from apollo.db.database import LibraryManager as _LibraryManager
from apollo.db.database import QueryBuildFailed, QueryExecutionFailed, RecordSet


Database = providers.Singleton(_Database)
LibraryManager = providers.Singleton(_LibraryManager)
