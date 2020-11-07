import math

# ============================
# PARSING
# ============================
def parseA(system):
    """
    Parser for ParamA table in database.
    :return: Matrix of linear parameters.
    """

    # size of the data
    fields = system.parama._meta.fields
    number_of_parameters = len(fields) - 2
    square_size = int(math.sqrt(number_of_parameters))

    # prepare to store the data
    a = [[0.0 for i in range(square_size)] for i in range(square_size)]

    # get the data
    for i in range(square_size):
        for j in range(square_size):
            field_name = f'a{i}{j}'
            a[i][j] = getattr(system.parama, field_name)

    return a


def parseC(system):
    """
    Parser for ParamC table in database.
    :return: Matrix of constant parameters.
    """
    # size of the data
    fields = system.paramc._meta.fields
    size = len(fields) - 2

    # prepare to store the data
    c = [0.0 for i in range(size)]

    # get the data
    for i in range(size):
        field_name = f'c{i}'
        c[i] = getattr(system.paramc, field_name)

    return c