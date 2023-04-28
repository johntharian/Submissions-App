from configparser import ConfigParser


def config(filename="database.ini", section="postgresql"):
    # create a parser to read the config file
    parser = ConfigParser()
    # read the specified config file
    parser.read(filename)

    # create an empty dictionary to store the database connection parameters
    db = {}
    # check if the specified section is present in the config file
    if parser.has_section(section):
        # get all the parameters for the specified section
        params = parser.items(section)
        # iterate over all the parameters and add them to the dictionary
        for param in params:
            db[param[0]] = param[1]
    else:
        raise Exception(
            "Section {0} not found in the {1} file".format(section, filename)
        )

    # return the dictionary containing the database connection parameters
    return db
