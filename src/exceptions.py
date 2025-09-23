"""
Custom exceptions for feature flag management.
"""


# ####################################################
# #### Repo custom exceptions ########################
# ####################################################
class RepositoryConnectionError(Exception):
    pass


class RepositoryNotFoundError(Exception):
    pass


# ####################################################
# ### Service custom exceptions ######################
# ####################################################


class FlagNotFoundError(Exception):
    pass


class FlagPersistenceError(Exception):
    pass
