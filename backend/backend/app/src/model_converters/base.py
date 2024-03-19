import abc
import functools
import inspect
import typing as t


# TODO: consider creating pydantic instances instead of dicts, check speed
class ModelConverter[H, L](abc.ABC):
    @classmethod
    @abc.abstractmethod
    def get_higher_model_base_class(cls) -> type[H]:
        pass

    @classmethod
    @abc.abstractmethod
    def get_lower_model_base_class(cls) -> type[L]:
        pass

    @classmethod
    @functools.cache  # TODO: check performance with logging
    def get_higher_to_lower_model_class_map(cls) -> dict[type[H], type[L]]:
        higher_class = cls.get_higher_model_base_class()
        lower_class = cls.get_lower_model_base_class()
        higher_module = inspect.getmodule(higher_class)
        lower_module = inspect.getmodule(lower_class)
        class_map = dict()

        for higher_attr_name, higher_attr in vars(higher_module).items():
            if inspect.isclass(higher_attr) and issubclass(higher_attr, higher_class) and higher_attr != higher_class:
                lower_attr = getattr(lower_module, higher_attr_name)
                if issubclass(lower_attr, lower_class):
                    class_map[higher_attr] = lower_attr

        return class_map


    @classmethod
    @functools.cache
    def get_lower_to_higher_model_class_map(cls) -> dict[type[L], type[H]]:
        return {v: k for k, v in cls.get_higher_to_lower_model_class_map().items()}

    def get_lower_model_class(self, higher_model_class: type[H]) -> type[L]:
        return self.get_higher_to_lower_model_class_map()[higher_model_class]

    def get_higher_model_class(self, lower_model_class: type[L]) -> type[H]:
        return self.get_lower_to_higher_model_class_map()[lower_model_class]

    def convert_to_lower_model(self, higher_model: H, **kwargs) -> L:
        return self._convert_from_target_model_dict(
            higher_model,
            self._convert_to_lower_model_dict(higher_model),
            self.get_lower_model_class
        )

    def convert_to_higher_model(self, lower_model: L, **kwargs) -> H:
        return self._convert_from_target_model_dict(
            lower_model,
            self._convert_to_higher_model_dict(lower_model, **kwargs),
            self.get_higher_model_class
        )

    # TODO: check if there is a way to make the same annotation for these funcs without overload

    @staticmethod
    @t.overload
    def _convert_from_target_model_dict(
            source_model: H,
            target_model_dict: dict[str, t.Any],
            get_target_model_class: t.Callable[[type[H]], type[L]]
    ) -> L: ...

    @staticmethod
    @t.overload
    def _convert_from_target_model_dict(
            source_model: L,
            target_model_dict: dict[str, t.Any],
            get_target_model_class: t.Callable[[type[L]], type[H]]
    ) -> H: ...

    @staticmethod
    def _convert_from_target_model_dict(
            source_model: [H | L],
            target_model_dict: dict[str, t.Any],
            get_target_model_class: t.Callable[[type[H] | type[L]], type[H] | type[L]]
    ) -> H | L:
        target_model_class = get_target_model_class(type(source_model))
        return target_model_class(**target_model_dict)

    def _convert_to_lower_model_dict(self, higher_model: H, **kwargs) -> dict[str, t.Any]:
        raise NotImplementedError

    def _convert_to_higher_model_dict(self, lower_model: L, **kwargs) -> dict[str, t.Any]:
        raise NotImplementedError

    @staticmethod
    @t.overload
    def _get_pydantic_model_attr_conversion_iterator(
            source_model: L,
            target_model_dict: dict[str, t.Any],
            check_model_class: type[L],
            convert_model: t.Callable[[L], t.Any]  # TODO: annotation for kwargs
    ) -> t.Iterator[tuple[str, t.Any, bool]]: ...

    @staticmethod
    @t.overload
    def _get_pydantic_model_attr_conversion_iterator(
            source_model: H,
            target_model_dict: dict[str, t.Any],
            check_model_class: type[H],
            convert_model: t.Callable[[H], t.Any]  # TODO: annotation for kwargs
    ) -> t.Iterator[tuple[str, t.Any, bool]]: ...

    @staticmethod
    def _get_pydantic_model_attr_conversion_iterator(
            source_model: H | L,
            target_model_dict: dict[str, t.Any],
            check_model_class: type[H | L],
            convert_model: t.Callable[[H | L], t.Any]  # TODO: annotation for kwargs
    ) -> t.Iterator[tuple[str, t.Any, bool]]:

        for key in source_model.model_fields:
            value = getattr(source_model, key)
            is_conditions_met = False
            target_model_dict[key] = value

            if isinstance(value, check_model_class):
                is_conditions_met = True
                target_model_dict[key] = convert_model(value)

            elif isinstance(value, list):
                is_conditions_met = True
                result_value = []
                for item in value:
                    if isinstance(item, check_model_class):
                        item_value = convert_model(item)
                    else:
                        item_value = value
                    result_value.append(item_value)
                target_model_dict[key] = result_value

            yield key, value, is_conditions_met
