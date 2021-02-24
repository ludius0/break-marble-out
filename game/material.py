class Material():
    """
    Holds data (parameters) about entities or other stuffs. 
    It holds data for friction, bounce and mass in floats between 0 to 1.
    """
    def __init__(self, friction: float = 0.5, bounce: float = 0.5, mass: float = 1.) -> None:
        assert 0 < friction <= 1. and 0 < bounce <= 1. and 0 < mass <= 1.
        self._friction = friction    # 0 -> ice; 1. -> glue
        self._bounce = bounce        # 0 -> inelastic; 1. -> elastic
        self._mass = mass
    
    def __repr__(self) -> str:
        return f"Material(Friction: {self._friction}; Bounce: {self._bounce}; Mass: {self._mass})"
    
    def __getitem__(self, item: str or int) -> float:
        assert isinstance(item, (str, int))
        if item in ("friction", "f", 0):    return self.friction
        elif item in ("bounce", "b", 1):    return self.bounce
        elif item in ("mass", "m", 2):      return self.mass
        raise TypeError
    
    @property
    def totuple(self) -> tuple: 
        return (self._friction, self._bounce, self._mass)

    @property
    def todict(self) -> dict: 
        return {"friction": self.friction, "bounce": self.bounce, "mass": self.mass}
    
    ### Explicit parts of Material
    
    @property
    def friction(self) -> float:
        return self._friction
    
    @friction.setter
    def friction(self, value: float) -> None:
        assert 0 < value <= 1. 
        self._friction = value

    @property
    def bounce(self) -> float:
        return self._bounce
    
    @bounce.setter
    def bounce(self, value: float) -> None:
        assert 0 < value <= 1. 
        self._bounce = value

    @property
    def mass(self) -> float:
        return self._mass
    
    @mass.setter
    def mass(self, value: float) -> None:
        assert 0 < value <= 1. 
        self._mass = value