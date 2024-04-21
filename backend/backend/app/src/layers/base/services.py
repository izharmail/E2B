import typing as t

from app.src.layers.domain.models.cioms import CIOMS


class ServiceProtocol[T](t.Protocol):
    def list(self, model_class: type[T]) -> list[dict[str, t.Any]]: ...

    def read(self, model_class: type[T], pk: int) -> T: ...

    def create(self, model: T) -> tuple[T, bool]: ...

    def update(self, model: T, pk: int) -> tuple[T, bool]: ...

    def delete(self, model_class: type[T], pk: int) -> bool: ...


class BusinessServiceProtocol[T](ServiceProtocol[T], t.Protocol):
    def business_validate(self, model: T) -> tuple[T, bool]: ...


class CIOMSServiceProtocol(t.Protocol):
    def convert_icsr_to_cioms(self, pk: int) -> CIOMS: ...
