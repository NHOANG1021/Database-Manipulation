import sqlite3
import p2app.events.continents as c
import p2app.events.countries as cc
import p2app.events.regions as r

def continent_search(path, continent_code, name):
    """
    Returns the continents resulting from a user's search
    """
    connection = sqlite3.connect(path)
    connection.execute("PRAGMA foreign_keys = ON;")
    cursor = connection.cursor()
    continents = []

    if continent_code and name:
        query = """SELECT continent_id, continent_code, name
        FROM continent
        WHERE continent_code = ? AND name = ?;"""
        cursor.execute(query, (continent_code, name))
    elif continent_code:
        query = """SELECT continent_id, continent_code, name
        FROM continent
        WHERE continent_code = ?;"""
        cursor.execute(query, (continent_code,))
    else:
        query = """SELECT continent_id, continent_code, name
        FROM continent
        WHERE name = ?;"""
        cursor.execute(query, (name,))

    while True:
        rows = cursor.fetchone()
        if rows is None:
            cursor.close()
            break
        continents.append(c.Continent(rows[0], rows[1], rows[2]))


    connection.close()
    return continents

def load_continent(path, continent_id):
    """
    Returns the continents resulting from a user's search
    """
    connection = sqlite3.connect(path)
    connection.execute("PRAGMA foreign_keys = ON;")
    cursor = connection.cursor()

    query = """SELECT continent_id, continent_code, name
    FROM continent
    WHERE continent_id = ?;"""
    cursor.execute(query, (continent_id,))

    rows = cursor.fetchone()
    connection.close()

    return rows


def save_continent(path, continent_data):
    """
    Given continent data in a tuple (continent_id, continent_code, name),
    updates the continent in the database.
    """
    connection = sqlite3.connect(path)
    connection.execute("PRAGMA foreign_keys = ON;")
    cursor = connection.cursor()

    query = """UPDATE continent
    SET continent_code = ?,  name = ?
    WHERE continent_id = ?;"""
    cursor.execute(query, (continent_data[1], continent_data[2], continent_data[0]))

    connection.commit()
    connection.close()


def unique_continent_id(path):
    """
    This function will loop through the existing continent_id's and
    returns an integer, to be used as a valid continent_id for new continents.
    """
    connection = sqlite3.connect(path)
    connection.execute("PRAGMA foreign_keys = ON;")
    cursor = connection.cursor()

    query = """SELECT *
    FROM continent;
    """

    cursor.execute(query)

    rows = cursor.fetchall()
    connection.close()
    return rows


def save_new_continent(path, continent_data):
    """
    Given continent data in a tuple (continent_id, continent_code, name),
    adds the continent in the database.
    """
    continent_id = unique_continent_id(path)[-1][0] + 1
    connection = sqlite3.connect(path)
    connection.execute("PRAGMA foreign_keys = ON;")
    cursor = connection.cursor()

    query = """INSERT INTO continent (continent_id, continent_code, name)
    VALUES (?, ?, ?)"""

    cursor.execute(query, (continent_id, continent_data[1], continent_data[2]))

    connection.commit()
    connection.close()

    return continent_id

def country_search(path, country_code, name):
    """
    Returns the countries resulting from a user's search
    """
    connection = sqlite3.connect(path)
    connection.execute("PRAGMA foreign_keys = ON;")
    cursor = connection.cursor()
    countries = []

    if country_code and name:
        query = """SELECT country_id, country_code, name, continent_id, wikipedia_link, keywords
        FROM country
        WHERE country_code = ? AND name = ?;"""
        cursor.execute(query, (country_code, name))
    elif country_code:
        query = """SELECT country_id, country_code, name, continent_id, wikipedia_link, keywords
        FROM country
        WHERE country_code = ?;"""
        cursor.execute(query, (country_code,))
    else:
        query = """SELECT country_id, country_code, name, continent_id, wikipedia_link, keywords
        FROM country
        WHERE name = ?;"""
        cursor.execute(query, (name,))

    while True:
        rows = cursor.fetchone()
        if rows is None:
            cursor.close()
            break
        countries.append(cc.Country(rows[0], rows[1], rows[2], rows[3], rows[4], rows[5]))


    connection.close()
    return countries


def load_country(path, country_id):
    """
    Returns the countries resulting from a user's search
    """
    connection = sqlite3.connect(path)
    connection.execute("PRAGMA foreign_keys = ON;")
    cursor = connection.cursor()

    query = """SELECT country_id, country_code, name, continent_id, wikipedia_link, keywords
    FROM country
    WHERE country_id = ?;"""
    cursor.execute(query, (country_id,))

    rows = cursor.fetchone()
    connection.close()

    return rows


def save_country(path, country_data):
    """
    Given country data in a tuple ('country_id', 'country_code', 'name', 'continent_id', 'wikipedia_link', 'keywords'),
    updates the country in the database.
    """
    connection = sqlite3.connect(path)
    connection.execute("PRAGMA foreign_keys = ON;")
    cursor = connection.cursor()
    if country_data[5] == '':
        query = """UPDATE country
        SET country_code = ?, name = ?, continent_id = ?, wikipedia_link = ?, keywords = NULL
        WHERE country_id = ?;"""
        cursor.execute(query, (country_data[1], country_data[2], country_data[3],
                               country_data[4], country_data[0]))
    else:
        query = """UPDATE country
        SET country_code = ?, name = ?, continent_id = ?, wikipedia_link = ?, keywords = ?
        WHERE country_id = ?;"""
        cursor.execute(query, (country_data[1], country_data[2], country_data[3],
                               country_data[4], country_data[5], country_data[0]))


    connection.commit()
    connection.close()


def unique_country_id(path):
    """
    This function will loop through the existing country_id's and
    returns an integer, to be used as a valid country_id for new continents.
    """
    connection = sqlite3.connect(path)
    connection.execute("PRAGMA foreign_keys = ON;")
    cursor = connection.cursor()

    query = """SELECT *
    FROM country;
    """

    cursor.execute(query)

    rows = cursor.fetchall()
    return rows


def save_new_country(path, country_data):
    """
    Given country data in a tuple ('country_id', 'country_code', 'name', 'continent_id', 'wikipedia_link', 'keywords'),
    adds the country in the database.
    """
    country_id = unique_country_id(path)[-1][0] + 1
    connection = sqlite3.connect(path)
    connection.execute("PRAGMA foreign_keys = ON;")
    cursor = connection.cursor()

    if country_data[5] == '':
        query = """INSERT INTO country (country_id, country_code, name, continent_id, wikipedia_link, keywords)
        VALUES (?, ?, ?, ?, ?, NULL)"""

        cursor.execute(query, (country_id, country_data[1], country_data[2], country_data[3],
                               country_data[4]))
    else:
        query = """INSERT INTO country (country_id, country_code, name, continent_id, wikipedia_link, keywords)
        VALUES (?, ?, ?, ?, ?, ?)"""

        cursor.execute(query, (country_id, country_data[1], country_data[2], country_data[3],
                               country_data[4], country_data[5]))

    connection.commit()
    connection.close()

    return country_id


def region_search(path, region_code, local_code, name):
    """
    Returns the region resulting from a user's search
    """
    connection = sqlite3.connect(path)
    connection.execute("PRAGMA foreign_keys = ON;")
    cursor = connection.cursor()
    regions = []

    if region_code and local_code and name:
        query = """SELECT region_id, region_code, local_code, name, continent_id, country_id, wikipedia_link, keywords
        FROM region
        WHERE region_code = ? AND local_code = ? AND name = ?;"""
        cursor.execute(query, (region_code, local_code, name))

    elif region_code and local_code:
        query = """SELECT region_id, region_code, local_code, name, continent_id, country_id, wikipedia_link, keywords
        FROM region
        WHERE region_code = ? AND local_code = ?;"""
        cursor.execute(query, (region_code, local_code))

    elif region_code and name:
        query = """SELECT region_id, region_code, local_code, name, continent_id, country_id, wikipedia_link, keywords
        FROM region
        WHERE region_code = ? AND name = ?;"""
        cursor.execute(query, (region_code, name))

    elif local_code and name:
        query = """SELECT region_id, region_code, local_code, name, continent_id, country_id, wikipedia_link, keywords
        FROM region
        WHERE local_code = ? AND name = ?;"""
        cursor.execute(query, (local_code, name))

    elif region_code:
        query = """SELECT region_id, region_code, local_code, name, continent_id, country_id, wikipedia_link, keywords
        FROM region
        WHERE region_code = ?;"""
        cursor.execute(query, (region_code,))

    elif local_code:
        query = """SELECT region_id, region_code, local_code, name, continent_id, country_id, wikipedia_link, keywords
        FROM region
        WHERE local_code = ?"""
        cursor.execute(query, (local_code,))

    elif name:
        query = """SELECT region_id, region_code, local_code, name, continent_id, country_id, wikipedia_link, keywords
        FROM region
        WHERE name = ?;"""
        cursor.execute(query, (name,))

    while True:
        rows = cursor.fetchone()
        if rows is None:
            cursor.close()
            break
        regions.append(r.Region(rows[0], rows[1], rows[2], rows[3], rows[4], rows[5], rows[6], rows[7]))


    connection.close()
    return regions

def load_region(path, region_id):
    """
    Returns the regions resulting from a user's search
    """
    connection = sqlite3.connect(path)
    connection.execute("PRAGMA foreign_keys = ON;")
    cursor = connection.cursor()

    query = """SELECT region_id, region_code, local_code, name, continent_id, country_id, wikipedia_link, keywords
    FROM region
    WHERE region_id = ?;"""
    cursor.execute(query, (region_id,))

    rows = cursor.fetchone()
    connection.close()

    return rows



def save_region(path, region_data):
    """
    Given region data in a tuple ('region_id', 'region_code', 'local_code', 'name',
    'continent_id', 'country_id', 'wikipedia_link', 'keywords'),
    updates the region in the database.
    """
    connection = sqlite3.connect(path)
    connection.execute("PRAGMA foreign_keys = ON;")
    cursor = connection.cursor()
    if region_data[6] and region_data[7]:
        query = """UPDATE region
        SET region_code = ?, local_code = ?, name = ?, continent_id = ?, country_id = ?, wikipedia_link = ?, keywords = ?
        WHERE region_id = ?;"""
        cursor.execute(query, (region_data[1], region_data[2], region_data[3],
                               region_data[4], region_data[5], region_data[6], region_data[7],
                               region_data[0]))

    elif region_data[6] == '' and region_data[7] == '':
        query = """UPDATE region
        SET region_code = ?, local_code = ?, name = ?, continent_id = ?, country_id = ?, wikipedia_link = NULL, keywords = NULL
        WHERE region_id = ?;"""
        cursor.execute(query, (region_data[1], region_data[2], region_data[3],
                               region_data[4], region_data[5], region_data[0]))

    elif region_data[6] == '' and region_data[7]:
        query = """UPDATE region
        SET region_code = ?, local_code = ?, name = ?, continent_id = ?, country_id = ?, wikipedia_link = NULL, keywords = ?
        WHERE region_id = ?;"""
        cursor.execute(query, (region_data[1], region_data[2], region_data[3], region_data[4],
                               region_data[5], region_data[7], region_data[0]))

    elif region_data[6] and region_data[7] == '':
        query = """UPDATE region
        SET region_code = ?, local_code = ?, name = ?, continent_id = ?, country_id = ?, wikipedia_link = ?, keywords = NULL
        WHERE region_id = ?;"""
        cursor.execute(query, (region_data[1], region_data[2], region_data[3], region_data[4],
                               region_data[5], region_data[6], region_data[0]))


    connection.commit()
    connection.close()



def unique_region_id(path):
    """
    This function will loop through the existing region_id's and
    returns an integer, to be used as a valid region_id for new regions.
    """
    connection = sqlite3.connect(path)
    connection.execute("PRAGMA foreign_keys = ON;")
    cursor = connection.cursor()

    query = """SELECT *
    FROM region;
    """

    cursor.execute(query)

    rows = cursor.fetchall()
    connection.close()
    return rows


def save_new_region(path, region_data):
    """
    Given region data in a tuple ('region_id', 'region_code', 'local_code', 'name',
    'continent_id', 'country_id', 'wikipedia_link', 'keywords'),
    adds the region in the database.
    """
    region_id = unique_region_id(path)[-1][0] + 1
    connection = sqlite3.connect(path)
    connection.execute("PRAGMA foreign_keys = ON;")
    cursor = connection.cursor()

    if region_data[6] and region_data[7]:
        query = """INSERT INTO region (region_id, region_code, local_code, name, continent_id, country_id, wikipedia_link, keywords)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)"""
        cursor.execute(query, (region_id, region_data[1], region_data[2], region_data[3],
                               region_data[4], region_data[5], region_data[6], region_data[7]))

    elif region_data[6] == '' and region_data[7] == '':
        query = """INSERT INTO region (region_id, region_code, local_code, name, continent_id, country_id, wikipedia_link, keywords)
        VALUES (?, ?, ?, ?, ?, ?, NULL, NULL)"""
        cursor.execute(query, (
        region_id, region_data[1], region_data[2], region_data[3], region_data[4], region_data[5]))

    elif region_data[6] == '' and region_data[7]:
        query = """INSERT INTO region (region_id, region_code, local_code, name, continent_id, country_id, wikipedia_link, keywords)
        VALUES (?, ?, ?, ?, ?, ?, NULL, ?)"""
        cursor.execute(query, (
        region_id, region_data[1], region_data[2], region_data[3], region_data[4], region_data[5], region_data[7]))

    elif region_data[6] and region_data[7] == '':
        query = """INSERT INTO region (region_id, region_code, local_code, name, continent_id, country_id, wikipedia_link, keywords)
        VALUES (?, ?, ?, ?, ?, ?, ?, NULL)"""
        cursor.execute(query, (
        region_id, region_data[1], region_data[2], region_data[3], region_data[4], region_data[5], region_data[6]))

    connection.commit()
    connection.close()

    return region_id


def check_for_tables(path) -> bool:
    """
    Checks if the .db file has continent, country, and region tables
    Returns True if they all exist, else False
    """
    connection = sqlite3.connect(path)
    connection.execute("PRAGMA foreign_keys = ON;")
    cursor = connection.cursor()

    try:
        cursor.execute("""SELECT *
        FROM continent
        """)
        cursor.execute("""SELECT *
        FROM country
        """)
        cursor.execute("""SELECT *
        FROM region
        """)

        cursor.close()
        connection.close()
        return True

    except sqlite3.OperationalError:
        cursor.close()
        connection.close()
        return False
