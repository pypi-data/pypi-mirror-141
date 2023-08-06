class BaseSolution:
    """ Base class for all solutions with the name property
    """

    @property
    def name(self) -> str:
        """Name of the model used as default for plotting label

        :setter: set the name for the model
        :getter: returns the name of the model
        """
        return self._name

    @name.setter
    def name(self, name: str) -> None:
        self._name = name
