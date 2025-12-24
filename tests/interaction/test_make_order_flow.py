oups() if matched else ('', '')
            value: str | list[Any] | dict[str, Any] = (
                json.dumps(model_default) if isinstance(model_default, (dict, list, set)) else str(model_default)
            )

            if arg.is_alias_path_only:
                # For alias path only, we wont know the complete value until we've finished parsing the entire class. In
                # this case, insert value as a non-string reference pointing to the relevant alias_path_only_defaults
                # entry and convert into completed string value later.
                value = self._update_alias_path_only_default(arg_name, value, field_info, alias_path_only_defaults)

            if _CliPositionalArg in field_info.metadata:
                for value in model_default if isinstance(model_default, list) else [model_default]:
                    value = json.dumps(value) if isinstance(value, (dict, list, set)) else str(value)
                    positional_args.append(value)
                continue

            # Note: prepend 'no-' for boolean optional action flag if model_default value is False and flag is not a short option
            if arg.kwargs.ge