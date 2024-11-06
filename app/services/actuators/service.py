from typing import Generic, List, TypeVar
from fastapi import HTTPException

from app.models.actuators import (
    Actuator,
    ActuatorRepository,
)
from app.models.errors import ValidationError

T = TypeVar("T", bound=Actuator)


class ActuatorService(Generic[T]):
    """
    A service class for managing actuators.

    This class provides methods to interact with actuator repositories.
    It is generic over a type T which must be a subclass of Actuator.

    Args:
        actuator (ActuatorRepository[T]): The repository for the actuator.
        item_type (T): The specific type of actuator.
    """

    def __init__(self, actuator: ActuatorRepository[T], item_type: T) -> None:
        self.actuator = actuator
        self.item_type = item_type

    def get_all(self) -> List[T]:
        """
        Retrieve all actuators.

        Returns:
            List[T]: A list of actuators.
        """
        return self.actuator.get_all()

    def get_by_id(self, actuator_id: int) -> T:
        """
        Retrieve an actuator by its ID.

        Args:
            actuator_id (int): The ID of the actuator.

        Returns:
            T: The actuator with the specified ID.
        """
        return self.actuator.get_by_id(actuator_id)

    def set_state(self, actuator: T) -> T:
        """
        Set the state of an actuator.

        Args:
            actuator (T): The actuator to update.

        Returns:
            T: The updated actuator.
        """
        self.validate_actuator_id(actuator)
        return self.actuator.set_state(actuator)

    def validate_actuator_id(self, actuator: T):
        """
        Validate the actuator ID.

        Args:
            actuator (T): The actuator to validate.

        Raises:
            HTTPException: If the actuator ID is invalid.
        """
        if actuator.id >= self.actuator.count:
            raise HTTPException(
                status_code=422,
                detail=[
                    ValidationError(
                        loc=["body", "id"],
                        msg=f"Input must be lower than {self.actuator.count}",
                        type="lower_than",
                        input=actuator.id,
                    ).model_dump()
                ],
            )
