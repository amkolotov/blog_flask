from app import manager

from main_app.management.commands.fill_db_from_json import fill_db_from_json
from main_app.management.commands.fill_reviews import fill_reviews_from_file


@manager.command
def fill_db():
    fill_db_from_json()


@manager.command
def fill_reviews():
    fill_reviews_from_file()


if __name__ == '__main__':
    manager.run()
