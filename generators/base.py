from abc import ABC, abstractmethod


class MicroserviceGenerator(ABC):
    @abstractmethod
    def generate(self, output_dir: str):
        """Generate the code for the microservice into the given directory."""
        pass
