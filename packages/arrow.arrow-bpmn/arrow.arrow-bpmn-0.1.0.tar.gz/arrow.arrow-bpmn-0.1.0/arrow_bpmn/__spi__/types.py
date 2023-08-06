from typing import Callable

from arrow_bpmn.__spi__.execution.executable import Executable
from arrow_dmn.__spi__.dmn_engine import DmnEngine

ServiceFactory = Callable[[str], Executable]
BusinessRuleFactory = Callable[[str, str], DmnEngine]
