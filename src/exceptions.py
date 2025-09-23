"""
Custom exceptions for feature flag management.
"""


# ####################################################
# #### Repo custom exceptions ########################
# ####################################################
class FlagNotFoundError(Exception):
    pass


class RepoNotFoundError(Exception):
    pass


# ####################################################
# ### Service custom exceptions ######################
# ####################################################


class RepositoryConnError(Exception):
    pass


class FlagPersistenceError(Exception):
    pass
