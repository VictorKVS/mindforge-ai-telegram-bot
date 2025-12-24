 self.env_prefix
                    else f'{arg_prefix.replace(subcommand_prefix, "", 1)}{name}'
                )
                kwargs: dict[str, Any] = {}
                kwargs['default'] = CLI_SUPPRESS
                kwargs['help'] = 'pydantic alias path'
                kwargs['action'] = 'append'
                kwargs['metavar'] = 'list'
                if index is None:
                    kwargs['metavar'] = 'dict'
                    self._cli_dict_args[arg_name] = dict
                args = [f'{self._cli_flag_prefix}{arg_name}']
                for key, arg in self._parser_map[arg_name].items():
                    arg.args, arg.kwargs = args, kwargs
                self._add_argument(context, *args, **kwargs)
                added_args.append(arg_name)

    def _get_modified_args(self, obj: Any) -> tuple[str, ...]:
        if not self.cli_hide_none_type:
            return get_args(obj)
        else:
            return tuple([type_ for type_ in get_args(obj) if type_ is not type(None)])

    def _metavar_format_choices(self, args: list[str], obj_qualname: str | None = None) -> str:
        if 'JSON' in args:
            args = args[: args.index('JSON') + 1] + [arg for arg in args[args.index('JSON') + 1 :] if arg != 'JSON']
        metavar = ','.join(args)
        if obj_qualname:
            return f'{obj_qualname}[{metavar}]'
        else:
            return metavar if len(args) == 1 else f'{{{metavar}}}'

    def _metavar_format_recurse(self, obj: Any) -> str:
        """Pretty metavar representation of a type. Adapts logic from `pydantic._repr.display_as_type`."""
        obj = _strip_annotated(obj)
        if _is_function(obj):
            # If function is locally defined use __name__ instead of __qualname__
            return obj.__name__ if '<locals>' in obj.__qualname__ else obj.__qualname__
        elif obj is ...:
            return '...'
        elif isinstance(obj, Representation):
            return repr(obj)
        elif typing_objects.is_typealiastype(obj):
            return str(obj)

        origin = get_origin(obj)
        if origin is None and not isinstance(obj, (type, typing.ForwardRef, typing_extensions