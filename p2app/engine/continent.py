import sqlite3
import p2app.events.continents as continents
import p2app.engine.query as query
import p2app.events.app as app


def continent_search_data(event: continents.StartContinentSearchEvent) -> tuple:
    """
    Retrieves user entered data when searching for a continent.
    The data is returned in the form of a tuple, (continent code, name)
    """
    return event.continent_code(), event.name()


def continent_search_result(path: str, data: tuple) -> list[continents.ContinentSearchResultEvent]:
    """
    Returns a list of ContinentSearchResultEvent for each continent found in the search
    """
    search_result = query.continent_search(path, data[0], data[1])
    search_result_list = []

    for continent in search_result:
        search_result_list.append(continents.ContinentSearchResultEvent(continent))

    return search_result_list


def load_continent(path: str, event: continents.LoadContinentEvent) -> (continents.ContinentLoadedEvent |
                                                                        app.ErrorEvent):
    """
    Returns a ContinentLoadedEvent using the data from the given event in a query
    """
    try:
        continent_id = event.continent_id()
        continent_data = query.load_continent(path, continent_id)
        return continents.ContinentLoadedEvent(continents.Continent(continent_data[0],
                                                                    continent_data[1],
                                                                    continent_data[2]))
    except:
        return app.ErrorEvent('Loading the continent failed!')


def save_continent(path: str, event: continents.SaveContinentEvent) -> (continents.ContinentSavedEvent |
                                                                        continents.SaveContinentFailedEvent):
    """
    Given the data from the event (continent_id, continent_code, name), update
    the data using a query and return a ContinentSavedEvent
    """
    try:
        continent_update_data = event.continent()
        query.save_continent(path, continent_update_data)

        return continents.ContinentSavedEvent(continents.Continent(continent_update_data[0],
                                                                   continent_update_data[1],
                                                                   continent_update_data[2]))
    except sqlite3.IntegrityError:
        return save_new_continent_fail()


def save_new_continent(path: str, event: continents.SaveNewContinentEvent) -> (continents.ContinentSavedEvent |
                                                                               continents.SaveContinentFailedEvent):
    """"
    Given the data from the event (continent_id, continent_code, name),
    inserts the data using a query and return a ContinentSavedEvent
    """
    try:
        continent_update_data = event.continent()
        returned_id = query.save_new_continent(path, continent_update_data)

        return continents.ContinentSavedEvent(continents.Continent(returned_id,
                                                                   continent_update_data[1],
                                                                   continent_update_data[2]))
    except sqlite3.IntegrityError:
        return save_new_continent_fail()


def save_new_continent_fail() -> continents.SaveContinentFailedEvent:
    """
    Returns a SaveContinentFailedEvent
    """
    return continents.SaveContinentFailedEvent("Saving the continent failed!")


def continent_events(path, event):
    """
    Processes all continent related events
    """
    if isinstance(event, continents.StartContinentSearchEvent):
        data = continent_search_data(event)
        search_result_list = continent_search_result(path, data)
        return search_result_list

    elif isinstance(event, continents.LoadContinentEvent):
        return load_continent(path, event)

    elif isinstance(event, continents.SaveNewContinentEvent):
        return save_new_continent(path, event)

    elif isinstance(event, continents.SaveContinentEvent):
        return save_continent(path, event)

