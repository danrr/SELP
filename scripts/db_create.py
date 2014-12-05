#!env/bin/python
import os.path
from migrate.versioning import api
from app.config import SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO
from tests.test_config import SQLALCHEMY_DATABASE_URI as TEST_SQLALCHEMY_DATABASE_URI,\
    SQLALCHEMY_MIGRATE_REPO as TEST_SQLALCHEMY_MIGRATE_REPO
from app import db


def create_db_and_update(db_uri, migrate_repo):
    if not os.path.exists(migrate_repo):
        api.create(migrate_repo, 'database repository')
        api.version_control(db_uri, migrate_repo)
    else:
        api.version_control(db_uri,
                            migrate_repo,
                            api.version(migrate_repo))


def main():
    db.create_all()
    #app db
    create_db_and_update(SQLALCHEMY_DATABASE_URI, SQLALCHEMY_MIGRATE_REPO)

    #test db
    create_db_and_update(TEST_SQLALCHEMY_DATABASE_URI, TEST_SQLALCHEMY_MIGRATE_REPO)


if __name__ == "__main__":
    main()