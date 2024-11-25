import sqlite3
import p2app.events.regions as regions
import p2app.engine.query as query
import p2app.events.app as app

def region_search_data(event: regions.StartRegionSearchEvent) -> tuple:
    """
    Retrieves user entered data when searching for a region.
    The data is returned in the form of a tuple, (region code, local code, name)
    """
    return event.region_code(), event.local_code(), event.name()


def region_search_result(path: str, data: tuple) -> list[regions.RegionSearchResultEvent]:
    """
    Returns a list of RegionSearchResultEvent for each region found in the search
    """
    search_result = query.region_search(path, data[0], data[1], data[2])
    search_result_list = []

    for region in search_result:
        search_result_list.append(regions.RegionSearchResultEvent(region))

    return search_result_list



def load_region(path: str, event: regions.LoadRegionEvent) -> regions.RegionLoadedEvent | app.ErrorEvent:
    """
    Returns a RegionLoadedEvent using the data from the given event in a query
    """
    try:
        region_id = event.region_id()
        region_data = query.load_region(path, region_id)
        return regions.RegionLoadedEvent(regions.Region(region_data[0], region_data[1], region_data[2],
                                                        region_data[3], region_data[4], region_data[5],
                                                        region_data[6], region_data[7]))
    except:
        return app.ErrorEvent('There was an error when loading the region!')


def save_region(path: str, event: regions.SaveRegionEvent) -> (regions.RegionSavedEvent |
                                                               regions.SaveRegionFailedEvent):
    """
    Given the data from the event ('region_id', 'region_code', 'local_code', 'name',
    'continent_id', 'country_id', 'wikipedia_link', 'keywords'),
    updates the data using a query and return a RegionSavedEvent
    """
    try:
        region_update_data = event.region()
        query.save_region(path, region_update_data)
        return regions.RegionSavedEvent(regions.Region(region_update_data[0], region_update_data[1],
                                                       region_update_data[2], region_update_data[3],
                                                       region_update_data[4], region_update_data[5],
                                                       region_update_data[6], region_update_data[7]))

    except sqlite3.IntegrityError:
        return save_new_region_fail()


def save_new_region(path: str, event: regions.SaveNewRegionEvent) -> (regions.RegionSavedEvent |
                                                                      regions.SaveRegionFailedEvent):
    """"
    Given the data from the event ('region_id', 'region_code', 'local_code', 'name',
    'continent_id', 'country_id', 'wikipedia_link', 'keywords'),
    insert the data using a query and return a RegionSavedEvent
    """
    try:
        region_update_data = event.region()
        returned_id = query.save_new_region(path, region_update_data)
        return regions.RegionSavedEvent(regions.Region(returned_id, region_update_data[1],
                                                       region_update_data[2],region_update_data[3],
                                                       region_update_data[4], region_update_data[5],
                                                       region_update_data[6], region_update_data[7]))

    except sqlite3.IntegrityError:
        return save_new_region_fail()

def save_new_region_fail() -> regions.SaveRegionFailedEvent:
    """
    Returns a RegionFailedEvent
    """
    return regions.SaveRegionFailedEvent("Saving the region failed!")


def region_events(path, event):
    """
    Processes all region related events
    """
    if isinstance(event, regions.StartRegionSearchEvent):
        data = region_search_data(event)
        search_result_list = region_search_result(path, data)
        return search_result_list

    elif isinstance(event, regions.LoadRegionEvent):
        return load_region(path, event)

    elif isinstance(event, regions.SaveNewRegionEvent):
        return save_new_region(path, event)

    elif isinstance(event, regions.SaveRegionEvent):
        return save_region(path, event)