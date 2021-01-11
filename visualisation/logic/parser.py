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


def parseIV(system):
    # size of the data
    fields = system.initialvalues._meta.fields
    size = len(fields) - 2

    # prepare to store the data
    iv = [0.0 for i in range(size)]

    # get the data
    for i in range(size):
        field_name = f'x{i}'
        iv[i] = getattr(system.initialvalues, field_name)

    return iv


def parseTS(system):
    start = getattr(system.timespan, "start")
    end = getattr(system.timespan, "end")
    return start, end


def parseV(system):
    # size of the data
    fields = system.visible._meta.fields
    size = len(fields) - 2

    # prepare to store the data
    v = ()

    # get the data
    for i in range(size):
        field_name = f'x{i}'
        if (getattr(system.visible, field_name)):
            v += i,

    if len(v) < 2:
        v = (0,1)

    return v[0], v[1]


def parseIMS(system):
    return getattr(system.integrationmaxstep, "step")


