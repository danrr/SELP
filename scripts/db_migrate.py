#!env/bin/python
import imp

from migrate.versioning import api
from app import db
from app.config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO
from tests.test_config import SQLALCHEMY_DATABASE_URI as TEST_SQLALCHEMY_DATABASE_URI,\
    SQLALCHEMY_MIGRATE_REPO as TEST_SQLALCHEMY_MIGRATE_REPO


def migrate_db(db_uri, migrate_repo):
    v = api.db_version(db_uri, migrate_repo)
    migration = migrate_repo + ('/versions/%03d_migration.py' % (v+1))
    tmp_module = imp.new_module('old_model')
    old_model = api.create_model(db_uri, migrate_repo)

    exec(old_model, tmp_module.__dict__)

    script = api.make_update_script_for_model(db_uri, migrate_repo, tmp_module.meta, db.metadata)

    open(migration, "wt").write(script)

    api.upgrade(db_uri, migrate_repo)

    v = api.db_version(db_uri, migrate_repo)
    print('New migration saved as ' + migration)
    print('Current database version: ' + str(v))

#app db
migrate_db(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)

#test db
migrate_db(TEST_SQLALCHEMY_DATABASE_URI, TEST_SQLALCHEMY_MIGRATE_REPO)
