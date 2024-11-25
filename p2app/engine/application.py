import p2app.events.database as db
import p2app.events.app as app
import p2app.engine.query as query


def quit_app() -> app.EndApplicationEvent:
    """
    Returns an EndApplicationEvent
    """
    obj = app.EndApplicationEvent()
    return obj

def open_db_file(path) -> db.DatabaseOpenedEvent:
    """
    Returns a DatabaseOpenedEvent
    """
    obj = db.DatabaseOpenedEvent(path)
    return obj

def open_db_file_fail() -> db.DatabaseOpenFailedEvent:
    """
    Returns a DatabaseOpenFailedEvent when a non .db file is selected
    """
    obj = db.DatabaseOpenFailedEvent('The file failed to open!')
    return obj

def close_db_file() -> db.DatabaseClosedEvent:
    """
    Returns a DatabaseClosedEvent
    """
    obj = db.DatabaseClosedEvent()
    return obj


def application_events(path, event):
    """
    Processes all the application level events
    """
    if 'QuitInitiatedEvent' in event.__repr__():
        return quit_app()

    elif 'OpenDatabaseEvent' in event.__repr__():
        path = event.path()
        if '.db' in str(path) and query.check_for_tables(path):
            return open_db_file(path)
        else:
            return open_db_file_fail()

    elif 'CloseDatabaseEvent' in event.__repr__():
        return close_db_file()
