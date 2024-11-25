import sqlite3
import p2app.engine.application as application
import p2app.engine.continent as continent
import p2app.engine.country as country
import p2app.engine.region as region
from p2app.events import *
class Engine:
    """An object that represents the application's engine, whose main role is to
    process events sent to it by the user interface, then generate events that are
    sent back to the user interface in response, allowing the user interface to be
    unaware of any details of how the engine is implemented.
    """

    def __init__(self):
        """Initializes the engine"""
        self.connection = None
        self.path = None


    def process_event(self, event):
        """A generator function that processes one event sent from the user interface,
        yielding zero or more events in response."""
        if isinstance(event, QuitInitiatedEvent) or isinstance(event, OpenDatabaseEvent) or isinstance(event, CloseDatabaseEvent):
            if isinstance(event, OpenDatabaseEvent):
                self.connect_to_database(event)

            yield application.application_events(self.path, event)

        elif (isinstance(event, StartContinentSearchEvent) or isinstance(event, LoadContinentEvent) or
              isinstance(event, SaveNewContinentEvent) or isinstance(event, SaveContinentEvent)):
            if isinstance(event, StartContinentSearchEvent):
                for i in continent.continent_events(self.path, event):
                    yield i
            else:
                yield continent.continent_events(self.path, event)

        elif (isinstance(event, StartCountrySearchEvent) or isinstance(event, LoadCountryEvent) or
              isinstance(event, SaveNewCountryEvent) or isinstance(event, SaveCountryEvent)):
            if isinstance(event, StartCountrySearchEvent):
                for i in country.country_events(self.path, event):
                    yield i
            else:
                yield country.country_events(self.path, event)

        else:
            if isinstance(event, StartRegionSearchEvent):
                for i in region.region_events(self.path, event):
                    yield i
            else:
                yield region.region_events(self.path, event)

    def connect_to_database(self, event: OpenDatabaseEvent):
        """
        When an OpenDatabaseEvent occurs, initialize connection and path.
        Also execute the foreign key constraints
        """
        self.path = event.path()
        self.connection = sqlite3.connect(self.path)
        self.connection.execute("PRAGMA foreign_keys = ON;")