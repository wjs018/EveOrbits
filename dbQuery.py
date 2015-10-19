import sqlite3


def SDEQuery(selectStr, fromStr, whereStr):
    """This will query the sqlite database for info.

    selectStr   This is a string that is the field for the SELECT 
                part of the sql query

    fromStr     This is a string that is the field for the FROM
                part of the sql query

    whereStr    This is a string that is the field from the WHERE
                part of the sql query

    Returns:

    rows        This is a list of tuples with each entry being a row
                from the database as a tuple.

    """

    # Connect to the database

    conn = sqlite3.connect('sqlite-latest.sqlite')
    c = conn.cursor()

    # Construct command to execute

    selectConstruct = 'SELECT ' + selectStr + ' '
    fromConstruct = 'FROM ' + fromStr + ' '
    whereConstruct = 'WHERE ' + whereStr

    finalQuery = selectConstruct + fromConstruct + whereConstruct

    # Execute command

    results = c.execute(finalQuery)

    rows = results.fetchall()

    return(rows)


def getGroupIDs(categoryID):
    """
    Returns a list of all groupIDs contained within a given categoryID.

    Returns a list with groupIDs
    """

    selectStr = 'groupID'
    fromStr = 'invGroups'
    whereStr = 'categoryID = ' + str(categoryID) + ' AND published = 1'

    result = SDEQuery(selectStr, fromStr, whereStr)

    for i in range(0, len(result)):

        result[i] = result[i][0]

    return result


def getTypeIDs(groupID):
    """
    Returns a list of all typeIDs contained within a given groupID.

    Returns a list with typeIDs
    """

    selectStr = 'typeID'
    fromStr = 'invTypes'
    whereStr = 'groupID = ' + str(groupID) + ' AND published = 1'

    result = SDEQuery(selectStr, fromStr, whereStr)

    for i in range(0, len(result)):

        result[i] = result[i][0]

    return result


def getGroupID(typeID):
    """ 
    Returns the groupID of an object based on the given typeid
    """

    # Figure out inputs to the SDEQuery

    selectStr = 'groupID'
    fromStr = 'invTypes'
    whereStr = 'typeID = ' + str(typeID) + ' AND published = 1'

    # Make the query

    result = SDEQuery(selectStr, fromStr, whereStr)

    return(result[0][0])


def getCategoryID(groupID):
    """
    Returns the categoryID of a given groupID
    """

    # Make inputs to the SDEQuery

    selectStr = 'categoryID'
    fromStr = 'invGroups'
    whereStr = 'groupID = ' + str(groupID) + ' AND published = 1'

    result = SDEQuery(selectStr, fromStr, whereStr)

    return(result[0][0])


def getMarketGroupID(typeID):
    """
    Returns the groupID of an object based on the given typeid
    """

    # Same as other functions

    selectStr = 'marketGroupID'
    fromStr = 'invTypes'
    whereStr = 'typeID = ' + str(typeID) + ' AND published = 1'

    result = SDEQuery(selectStr, fromStr, whereStr)

    return(result[0][0])


def getGroupNames(categoryID):
    """
    Returns a list of group names contained within a categoryID
    """

    selectStr = 'groupName'
    fromStr = 'invGroups'
    whereStr = 'categoryID = ' + str(categoryID) + ' AND published = 1'

    result = SDEQuery(selectStr, fromStr, whereStr)

    for i in range(0, len(result)):

        result[i] = result[i][0]

    return result


def getTypeNames(groupID):
    """
    Returns a list of type names contained within a groupID
    """

    selectStr = 'typeName'
    fromStr = 'invTypes'
    whereStr = 'groupID = ' + str(groupID) + ' AND published = 1'

    result = SDEQuery(selectStr, fromStr, whereStr)

    for i in range(0, len(result)):

        result[i] = result[i][0]

    return result


def getGroupName(typeID):
    """
    Returns the groupName of a given typeid
    """

    selectStr = 'groupID'
    fromStr = 'invTypes'
    whereStr = 'typeID = ' + str(typeID) + ' AND published = 1'

    result = SDEQuery(selectStr, fromStr, whereStr)
    result = result[0][0]

    selectStr = 'groupName'
    fromStr = 'invGroups'
    whereStr = 'groupID = ' + str(result)

    result = SDEQuery(selectStr, fromStr, whereStr)
    result = result[0][0]

    return result


def getCategoryName(groupID):
    """
    Returns the categoryName of a given groupID
    """

    selectStr = 'categoryID'
    fromStr = 'invGroups'
    whereStr = 'groupID = ' + str(groupID) + ' AND published = 1'

    result = SDEQuery(selectStr, fromStr, whereStr)
    result = result[0][0]

    selectStr = 'categoryName'
    fromStr = 'invCategories'
    whereStr = 'categoryID = ' + str(result) + ' AND published = 1'

    result = SDEQuery(selectStr, fromStr, whereStr)
    result = result[0][0]

    return result


def getTypeName(typeID):
    """
    Returns the typeName of a given typeid
    """
    
    selectStr = 'typeName'
    fromStr = 'invTypes'
    whereStr = 'typeID = ' + str(typeID) + ' AND published = 1'
    
    result = SDEQuery(selectStr, fromStr, whereStr)
    result = result[0][0]
    
    return result
    
    
    
    
    