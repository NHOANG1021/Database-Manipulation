import sqlite3
import p2app.events.countries as countries
import p2app.engine.query as query
import p2app.events.app as app

def country_search_data(event: countries.StartCountrySearchEvent) -> tuple:
    """
    Retrieves user entered data when searching for a country.
    The data is returned in the form of a tuple, (country code, name)
    """
    return event.country_code(), event.name()


def country_search_result(path: str, data: tuple) -> list[countries.CountrySearchResultEvent]:
    """
    Returns a list of CountrySearchResultEvent for each country found in the search
    """
    search_result = query.country_search(path, data[0], data[1])
    search_result_list = []

    for country in search_result:
        search_result_list.append(countries.CountrySearchResultEvent(country))

    return search_result_list


def load_country(path: str, event: countries.LoadCountryEvent) -> countries.CountryLoadedEvent | app.ErrorEvent:
    """
    Returns a CountryLoadedEvent using the data from the given event in a query
    """
    try:
        country_id = event.country_id()
        country_data = query.load_country(path, country_id)
        return countries.CountryLoadedEvent(countries.Country(country_data[0], country_data[1], country_data[2],
                                                              country_data[3], country_data[4], country_data[5]))
    except:
        return app.ErrorEvent('There was an error when loading the country!')

def save_country(path: str, event: countries.SaveCountryEvent) -> (countries.CountrySavedEvent |
                                                                   countries.SaveCountryFailedEvent):
    """
    Given the data from the event, ('country_id', 'country_code', 'name', 'continent_id', 'wikipedia_link', 'keywords'),
    updates the data using a query and return a CountrySavedEvent if successful
    """
    try:
        country_update_data = event.country()
        query.save_country(path, country_update_data)
        return countries.CountrySavedEvent(countries.Country(country_update_data[0], country_update_data[1],
                                                             country_update_data[2],country_update_data[3],
                                                             country_update_data[4], country_update_data[5]))

    except sqlite3.IntegrityError:
        return save_new_country_fail()

def save_new_country(path: str, event: countries.SaveNewCountryEvent)-> (countries.CountrySavedEvent |
                                                                         countries.SaveCountryFailedEvent):
    """"
    Given the data from the event ('country_id', 'country_code', 'name', 'continent_id', 'wikipedia_link', 'keywords'),
    inserts the data using a query and return a CountrySavedEvent if successful
    """
    try:
        country_update_data = event.country()
        returned_id = query.save_new_country(path, country_update_data)

        return countries.CountrySavedEvent(countries.Country(returned_id, country_update_data[1],
                                                             country_update_data[2],country_update_data[3],
                                                             country_update_data[4], country_update_data[5]))
    except sqlite3.IntegrityError:
        return save_new_country_fail()


def save_new_country_fail() -> countries.SaveCountryFailedEvent:
    """
    Returns a SaveCountryFailedEvent
    """
    return countries.SaveCountryFailedEvent("Saving the country failed!")

def country_events(path, event):
    """
    Processes all country related events
    """
    if isinstance(event, countries.StartCountrySearchEvent):
        data = country_search_data(event)
        search_result_list = country_search_result(path, data)
        return search_result_list

    elif isinstance(event, countries.LoadCountryEvent):
        return load_country(path, event)

    elif isinstance(event, countries.SaveNewCountryEvent):
        return save_new_country(path, event)

    elif isinstance(event, countries.SaveCountryEvent):
        return save_country(path, event)