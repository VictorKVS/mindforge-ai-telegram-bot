t in field_info.metadata:
                ifdef = 'ifdef: ' if model_default is None else ''
                _help += f' ({ifdef}required)' if _help else f'({ifdef}required)'
        else:
            default = f'(default: {self.cli_parse_none_str})'
            if is_model_class(type(model_default)) or is_pydantic_dataclass(type(model_default)):
                default = f'(default: {getattr(model_default, field_name)})'
            elif model_default not in (PydanticUndefined, None) and _is_function(model_default):
                default = f'(default factory: {self._metavar_format(model_default)})'
            elif field_info.default not in (PydanticUndefined, None):
                enum_name = _annotation_enum_val_to_name(field_info.annotation, field_info.default)
                default = f'(default: {field_info.default if enum_name is None else enum_name})'
            elif field_info.default_factory is not None:
                default = f'(default factory: {self._metavar_format(field_info.default_factory)})'
            _help += f' {default}' if _help else default
        return _help.replace('%', '%%') if issubclass(ty