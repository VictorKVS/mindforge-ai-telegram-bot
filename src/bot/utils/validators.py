"""
validators.py

Комплексная система валидации ввода с поддержкой различных типов данных,
правил валидации, пользовательских валидаторов и расширенной отчетности.

Структурированную систему валидации с классами для ошибок, результатов и правил

Поддержку различных типов данных: строки, числа, даты, email, телефоны и т.д.

Гибкие правила валидации с параметризацией

Валидацию схем данных (словарей/JSON)

Декораторы для валидации аргументов и возвращаемых значений функций

Утилитарные функции для быстрой валидации

Подробную отчетность с поддержкой ошибок и предупреждений

Экспорт в JSON для результатов валидации

Обратную совместимость с оригинальной функцией is_valid_input()

Полные примеры использования и тестирования
"""

import re
import json
from typing import Union, Optional, List, Dict, Any, Callable, Type, Tuple
from datetime import datetime, date
from decimal import Decimal, InvalidOperation
from email_validator import validate_email as validate_email_package, EmailNotValidError
import logging
from dataclasses import dataclass, field
from enum import Enum
import inspect

# Настройка логирования
logger = logging.getLogger(__name__)


class ValidationSeverity(Enum):
    """Уровень серьезности ошибки валидации"""
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class ValidationRuleType(Enum):
    """Типы правил валидации"""
    REQUIRED = "required"
    TYPE = "type"
    PATTERN = "pattern"
    LENGTH = "length"
    RANGE = "range"
    ENUM = "enum"
    CUSTOM = "custom"
    COMPOSITE = "composite"


@dataclass
class ValidationError:
    """Детализированная информация об ошибке валидации"""
    field: str
    message: str
    value: Any
    rule: str
    severity: ValidationSeverity = ValidationSeverity.ERROR
    code: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        """Конвертировать в словарь"""
        return {
            "field": self.field,
            "message": self.message,
            "value": self.value,
            "rule": self.rule,
            "severity": self.severity.value,
            "code": self.code,
            "metadata": self.metadata
        }


@dataclass
class ValidationResult:
    """Результат валидации с детальной информацией"""
    is_valid: bool
    errors: List[ValidationError] = field(default_factory=list)
    warnings: List[ValidationError] = field(default_factory=list)
    validated_data: Optional[Any] = None
    metadata: Dict[str, Any] = field(default_factory=dict)
    
    def __bool__(self) -> bool:
        """Булевое представление - только ошибки, предупреждения игнорируются"""
        return self.is_valid and not any(e.severity == ValidationSeverity.ERROR for e in self.errors)
    
    def add_error(self, 
                  field: str, 
                  message: str, 
                  value: Any, 
                  rule: str,
                  severity: ValidationSeverity = ValidationSeverity.ERROR,
                  code: Optional[str] = None,
                  **metadata) -> None:
        """Добавить ошибку валидации"""
        error = ValidationError(
            field=field,
            message=message,
            value=value,
            rule=rule,
            severity=severity,
            code=code,
            metadata=metadata
        )
        self.errors.append(error)
        if severity in [ValidationSeverity.ERROR, ValidationSeverity.CRITICAL]:
            self.is_valid = False
    
    def add_warning(self, 
                    field: str, 
                    message: str, 
                    value: Any, 
                    rule: str,
                    code: Optional[str] = None,
                    **metadata) -> None:
        """Добавить предупреждение валидации"""
        warning = ValidationError(
            field=field,
            message=message,
            value=value,
            rule=rule,
            severity=ValidationSeverity.WARNING,
            code=code,
            metadata=metadata
        )
        self.warnings.append(warning)
    
    def merge(self, other: 'ValidationResult') -> 'ValidationResult':
        """Объединить с другим результатом валидации"""
        self.errors.extend(other.errors)
        self.warnings.extend(other.warnings)
        self.is_valid = self.is_valid and other.is_valid
        
        if other.validated_data is not None:
            self.validated_data = other.validated_data
            
        self.metadata.update(other.metadata)
        return self
    
    def to_dict(self) -> Dict[str, Any]:
        """Конвертировать в словарь"""
        return {
            "is_valid": self.is_valid,
            "errors": [e.to_dict() for e in self.errors],
            "warnings": [w.to_dict() for w in self.warnings],
            "validated_data": self.validated_data,
            "metadata": self.metadata
        }
    
    def to_json(self, indent: Optional[int] = 2) -> str:
        """Конвертировать в JSON"""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False, default=str)


class ValidationRule:
    """Правило валидации"""
    
    def __init__(self, 
                 rule_type: ValidationRuleType,
                 validator: Callable,
                 message: Optional[str] = None,
                 params: Dict[str, Any] = None,
                 code: Optional[str] = None):
        self.rule_type = rule_type
        self.validator = validator
        self.message = message
        self.params = params or {}
        self.code = code
    
    def validate(self, value: Any, field_name: str = "") -> ValidationResult:
        """Применить правило валидации"""
        result = ValidationResult(is_valid=True, validated_data=value)
        
        try:
            is_valid = self.validator(value, **self.params) if self.params else self.validator(value)
            
            if not is_valid:
                message = self.message or f"Поле '{field_name}' не прошло валидацию по правилу {self.rule_type.value}"
                result.add_error(
                    field=field_name,
                    message=message,
                    value=value,
                    rule=self.rule_type.value,
                    code=self.code,
                    **self.params
                )
        except Exception as e:
            logger.error(f"Ошибка при выполнении валидации: {e}")
            result.add_error(
                field=field_name,
                message=f"Ошибка валидации: {str(e)}",
                value=value,
                rule=self.rule_type.value,
                code="VALIDATOR_ERROR"
            )
        
        return result


class Validator:
    """Базовый класс валидатора"""
    
    # Регулярные выражения для общих паттернов
    PATTERNS = {
        'email': r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$',
        'phone': r'^\+?[1-9]\d{1,14}$',
        'phone_ru': r'^(\+7|8)[\s\-]?\(?\d{3}\)?[\s\-]?\d{3}[\s\-]?\d{2}[\s\-]?\d{2}$',
        'url': r'^https?://(?:www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b(?:[-a-zA-Z0-9()@:%_\+.~#?&//=]*)$',
        'username': r'^[a-zA-Z0-9_-]{3,20}$',
        'password': r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&#])[A-Za-z\d@$!%*?&#]{8,}$',
        'date_iso': r'^\d{4}-\d{2}-\d{2}$',
        'time_24h': r'^([01]?[0-9]|2[0-3]):[0-5][0-9](?::[0-5][0-9])?$',
        'integer': r'^-?\d+$',
        'float': r'^-?\d+(?:\.\d+)?$',
        'hex_color': r'^#([A-Fa-f0-9]{6}|[A-Fa-f0-9]{3})$',
        'uuid': r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$',
        'ipv4': r'^(\d{1,3}\.){3}\d{1,3}$',
        'domain': r'^(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]$',
    }
    
    def __init__(self):
        self.rules: List[ValidationRule] = []
        self.field_name: str = ""
        
    def add_rule(self, rule: ValidationRule) -> 'Validator':
        """Добавить правило валидации"""
        self.rules.append(rule)
        return self
    
    def validate(self, value: Any, field_name: str = "") -> ValidationResult:
        """Выполнить валидацию"""
        self.field_name = field_name or self.field_name
        result = ValidationResult(is_valid=True, validated_data=value)
        
        # Применяем все правила
        for rule in self.rules:
            rule_result = rule.validate(value, self.field_name)
            result.merge(rule_result)
            
            # Если есть критическая ошибка, можно прервать
            if any(e.severity == ValidationSeverity.CRITICAL for e in rule_result.errors):
                break
        
        return result
    
    # Фабричные методы для создания правил
    
    @classmethod
    def required(cls, message: Optional[str] = None) -> ValidationRule:
        """Правило обязательного поля"""
        def validator(value: Any) -> bool:
            if value is None:
                return False
            if isinstance(value, str):
                return len(value.strip()) > 0
            if isinstance(value, (list, dict, set, tuple)):
                return len(value) > 0
            return True
        
        return ValidationRule(
            rule_type=ValidationRuleType.REQUIRED,
            validator=validator,
            message=message or "Поле обязательно для заполнения",
            code="REQUIRED"
        )
    
    @classmethod
    def type_check(cls, expected_type: Type, message: Optional[str] = None) -> ValidationRule:
        """Проверка типа данных"""
        def validator(value: Any) -> bool:
            return isinstance(value, expected_type)
        
        type_name = expected_type.__name__
        return ValidationRule(
            rule_type=ValidationRuleType.TYPE,
            validator=validator,
            message=message or f"Значение должно быть типа {type_name}",
            params={"expected_type": type_name},
            code="TYPE_MISMATCH"
        )
    
    @classmethod
    def pattern(cls, pattern: str, message: Optional[str] = None) -> ValidationRule:
        """Проверка по регулярному выражению"""
        def validator(value: Any) -> bool:
            if not isinstance(value, str):
                return False
            return bool(re.match(pattern, value))
        
        return ValidationRule(
            rule_type=ValidationRuleType.PATTERN,
            validator=validator,
            message=message or "Значение не соответствует ожидаемому формату",
            params={"pattern": pattern},
            code="PATTERN_MISMATCH"
        )
    
    @classmethod
    def min_length(cls, min_len: int, message: Optional[str] = None) -> ValidationRule:
        """Минимальная длина"""
        def validator(value: Any) -> bool:
            if not isinstance(value, str):
                return False
            return len(value.strip()) >= min_len
        
        return ValidationRule(
            rule_type=ValidationRuleType.LENGTH,
            validator=validator,
            message=message or f"Минимальная длина: {min_len} символов",
            params={"min_length": min_len},
            code="MIN_LENGTH"
        )
    
    @classmethod
    def max_length(cls, max_len: int, message: Optional[str] = None) -> ValidationRule:
        """Максимальная длина"""
        def validator(value: Any) -> bool:
            if not isinstance(value, str):
                return False
            return len(value.strip()) <= max_len
        
        return ValidationRule(
            rule_type=ValidationRuleType.LENGTH,
            validator=validator,
            message=message or f"Максимальная длина: {max_len} символов",
            params={"max_length": max_len},
            code="MAX_LENGTH"
        )
    
    @classmethod
    def length(cls, exact_len: int, message: Optional[str] = None) -> ValidationRule:
        """Точная длина"""
        def validator(value: Any) -> bool:
            if not isinstance(value, str):
                return False
            return len(value.strip()) == exact_len
        
        return ValidationRule(
            rule_type=ValidationRuleType.LENGTH,
            validator=validator,
            message=message or f"Требуемая длина: {exact_len} символов",
            params={"exact_length": exact_len},
            code="EXACT_LENGTH"
        )
    
    @classmethod
    def min_value(cls, min_val: Union[int, float], message: Optional[str] = None) -> ValidationRule:
        """Минимальное значение"""
        def validator(value: Any) -> bool:
            try:
                num = float(value) if isinstance(value, str) else value
                return num >= min_val
            except (ValueError, TypeError):
                return False
        
        return ValidationRule(
            rule_type=ValidationRuleType.RANGE,
            validator=validator,
            message=message or f"Минимальное значение: {min_val}",
            params={"min_value": min_val},
            code="MIN_VALUE"
        )
    
    @classmethod
    def max_value(cls, max_val: Union[int, float], message: Optional[str] = None) -> ValidationRule:
        """Максимальное значение"""
        def validator(value: Any) -> bool:
            try:
                num = float(value) if isinstance(value, str) else value
                return num <= max_val
            except (ValueError, TypeError):
                return False
        
        return ValidationRule(
            rule_type=ValidationRuleType.RANGE,
            validator=validator,
            message=message or f"Максимальное значение: {max_val}",
            params={"max_value": max_val},
            code="MAX_VALUE"
        )
    
    @classmethod
    def range_value(cls, 
                   min_val: Union[int, float], 
                   max_val: Union[int, float], 
                   message: Optional[str] = None) -> ValidationRule:
        """Диапазон значений"""
        def validator(value: Any) -> bool:
            try:
                num = float(value) if isinstance(value, str) else value
                return min_val <= num <= max_val
            except (ValueError, TypeError):
                return False
        
        return ValidationRule(
            rule_type=ValidationRuleType.RANGE,
            validator=validator,
            message=message or f"Значение должно быть в диапазоне от {min_val} до {max_val}",
            params={"min_value": min_val, "max_value": max_val},
            code="RANGE"
        )
    
    @classmethod
    def enum(cls, allowed_values: List[Any], message: Optional[str] = None) -> ValidationRule:
        """Проверка на вхождение в список разрешенных значений"""
        def validator(value: Any) -> bool:
            return value in allowed_values
        
        return ValidationRule(
            rule_type=ValidationRuleType.ENUM,
            validator=validator,
            message=message or f"Значение должно быть одним из: {allowed_values}",
            params={"allowed_values": allowed_values},
            code="ENUM"
        )
    
    @classmethod
    def custom(cls, 
              validator_func: Callable[[Any], bool], 
              message: Optional[str] = None,
              code: Optional[str] = None) -> ValidationRule:
        """Пользовательская функция валидации"""
        return ValidationRule(
            rule_type=ValidationRuleType.CUSTOM,
            validator=validator_func,
            message=message or "Не пройдена пользовательская валидация",
            code=code or "CUSTOM"
        )


# Специализированные валидаторы для конкретных типов данных

class StringValidator(Validator):
    """Валидатор строк"""
    
    def __init__(self):
        super().__init__()
    
    @classmethod
    def email(cls, message: Optional[str] = None) -> ValidationRule:
        """Валидация email с использованием библиотеки email-validator"""
        def validator(value: Any) -> bool:
            if not isinstance(value, str):
                return False
            
            # Базовая проверка regex
            if not re.match(cls.PATTERNS['email'], value):
                return False
            
            # Расширенная проверка с библиотекой
            try:
                validate_email_package(value, check_deliverability=False)
                return True
            except EmailNotValidError:
                return False
        
        return ValidationRule(
            rule_type=ValidationRuleType.PATTERN,
            validator=validator,
            message=message or "Некорректный email адрес",
            code="INVALID_EMAIL"
        )
    
    @classmethod
    def phone(cls, country_code: str = "RU", message: Optional[str] = None) -> ValidationRule:
        """Валидация номера телефона"""
        def validator(value: Any) -> bool:
            if not isinstance(value, str):
                return False
            
            # Очистка номера
            cleaned = re.sub(r'[^\d+]', '', value)
            
            # Выбор паттерна в зависимости от страны
            if country_code == "RU":
                # Для российских номеров
                if value.startswith('+7') or value.startswith('8'):
                    return bool(re.match(cls.PATTERNS['phone_ru'], value))
            
            # Международный формат E.164
            return bool(re.match(cls.PATTERNS['phone'], cleaned))
        
        return ValidationRule(
            rule_type=ValidationRuleType.PATTERN,
            validator=validator,
            message=message or "Некорректный номер телефона",
            params={"country_code": country_code},
            code="INVALID_PHONE"
        )
    
    @classmethod
    def url(cls, message: Optional[str] = None) -> ValidationRule:
        """Валидация URL"""
        return cls.pattern(cls.PATTERNS['url'], message or "Некорректный URL")


class NumberValidator(Validator):
    """Валидатор чисел"""
    
    def __init__(self):
        super().__init__()
    
    @classmethod
    def integer(cls, message: Optional[str] = None) -> ValidationRule:
        """Валидация целого числа"""
        return cls.pattern(cls.PATTERNS['integer'], message or "Значение должно быть целым числом")
    
    @classmethod
    def float(cls, message: Optional[str] = None) -> ValidationRule:
        """Валидация числа с плавающей точкой"""
        return cls.pattern(cls.PATTERNS['float'], message or "Значение должно быть числом")
    
    @classmethod
    def positive(cls, message: Optional[str] = None) -> ValidationRule:
        """Проверка на положительное число"""
        def validator(value: Any) -> bool:
            try:
                num = float(value) if isinstance(value, str) else value
                return num > 0
            except (ValueError, TypeError):
                return False
        
        return ValidationRule(
            rule_type=ValidationRuleType.RANGE,
            validator=validator,
            message=message or "Значение должно быть положительным",
            code="POSITIVE"
        )
    
    @classmethod
    def negative(cls, message: Optional[str] = None) -> ValidationRule:
        """Проверка на отрицательное число"""
        def validator(value: Any) -> bool:
            try:
                num = float(value) if isinstance(value, str) else value
                return num < 0
            except (ValueError, TypeError):
                return False
        
        return ValidationRule(
            rule_type=ValidationRuleType.RANGE,
            validator=validator,
            message=message or "Значение должно быть отрицательным",
            code="NEGATIVE"
        )


class DateTimeValidator(Validator):
    """Валидатор дат и времени"""
    
    def __init__(self):
        super().__init__()
    
    @classmethod
    def date(cls, format: str = "%Y-%m-%d", message: Optional[str] = None) -> ValidationRule:
        """Валидация даты"""
        def validator(value: Any) -> bool:
            if not isinstance(value, (str, date, datetime)):
                return False
            
            if isinstance(value, (date, datetime)):
                return True
            
            try:
                datetime.strptime(value, format)
                return True
            except ValueError:
                return False
        
        return ValidationRule(
            rule_type=ValidationRuleType.PATTERN,
            validator=validator,
            message=message or f"Дата должна быть в формате {format}",
            params={"format": format},
            code="INVALID_DATE"
        )
    
    @classmethod
    def datetime(cls, format: str = "%Y-%m-%d %H:%M:%S", message: Optional[str] = None) -> ValidationRule:
        """Валидация даты и времени"""
        return cls.date(format, message or f"Дата и время должны быть в формате {format}")
    
    @classmethod
    def future_date(cls, message: Optional[str] = None) -> ValidationRule:
        """Проверка что дата в будущем"""
        def validator(value: Any) -> bool:
            try:
                if isinstance(value, str):
                    dt = datetime.strptime(value, "%Y-%m-%d")
                elif isinstance(value, date):
                    dt = datetime.combine(value, datetime.min.time())
                elif isinstance(value, datetime):
                    dt = value
                else:
                    return False
                
                return dt > datetime.now()
            except (ValueError, TypeError):
                return False
        
        return ValidationRule(
            rule_type=ValidationRuleType.RANGE,
            validator=validator,
            message=message or "Дата должна быть в будущем",
            code="FUTURE_DATE"
        )
    
    @classmethod
    def past_date(cls, message: Optional[str] = None) -> ValidationRule:
        """Проверка что дата в прошлом"""
        def validator(value: Any) -> bool:
            try:
                if isinstance(value, str):
                    dt = datetime.strptime(value, "%Y-%m-%d")
                elif isinstance(value, date):
                    dt = datetime.combine(value, datetime.min.time())
                elif isinstance(value, datetime):
                    dt = value
                else:
                    return False
                
                return dt < datetime.now()
            except (ValueError, TypeError):
                return False
        
        return ValidationRule(
            rule_type=ValidationRuleType.RANGE,
            validator=validator,
            message=message or "Дата должна быть в прошлом",
            code="PAST_DATE"
        )


class SchemaValidator:
    """Валидатор схем данных (для словарей/JSON)"""
    
    def __init__(self, schema: Dict[str, Union[Validator, List[Validator]]]):
        self.schema = schema
    
    def validate(self, data: Dict[str, Any]) -> ValidationResult:
        """Валидация данных по схеме"""
        result = ValidationResult(is_valid=True, validated_data=data)
        
        for field_name, field_validators in self.schema.items():
            value = data.get(field_name)
            
            # Преобразуем одиночный валидатор в список
            validators = field_validators if isinstance(field_validators, list) else [field_validators]
            
            for validator in validators:
                if isinstance(validator, Validator):
                    field_result = validator.validate(value, field_name)
                    result.merge(field_result)
                elif callable(validator):
                    # Прямая функция валидации
                    try:
                        if not validator(value):
                            result.add_error(
                                field=field_name,
                                message=f"Поле '{field_name}' не прошло валидацию",
                                value=value,
                                rule="custom",
                                code="FIELD_VALIDATION"
                            )
                    except Exception as e:
                        result.add_error(
                            field=field_name,
                            message=f"Ошибка при валидации поля '{field_name}': {str(e)}",
                            value=value,
                            rule="custom",
                            code="VALIDATOR_EXCEPTION"
                        )
        
        # Проверка на лишние поля
        schema_fields = set(self.schema.keys())
        data_fields = set(data.keys())
        extra_fields = data_fields - schema_fields
        
        if extra_fields:
            result.add_warning(
                field="__extra__",
                message=f"Обнаружены лишние поля: {', '.join(extra_fields)}",
                value=list(extra_fields),
                rule="schema",
                code="EXTRA_FIELDS"
            )
        
        return result


# Утилитарные функции для быстрой валидации

def validate_string(
    value: Any,
    min_length: Optional[int] = None,
    max_length: Optional[int] = None,
    pattern: Optional[str] = None,
    required: bool = True
) -> ValidationResult:
    """Быстрая валидация строки"""
    validator = Validator()
    
    if required:
        validator.add_rule(Validator.required())
    
    validator.add_rule(Validator.type_check(str))
    
    if min_length is not None:
        validator.add_rule(Validator.min_length(min_length))
    
    if max_length is not None:
        validator.add_rule(Validator.max_length(max_length))
    
    if pattern is not None:
        validator.add_rule(Validator.pattern(pattern))
    
    return validator.validate(value)


def validate_email(value: Any, required: bool = True) -> ValidationResult:
    """Быстрая валидация email"""
    validator = StringValidator()
    
    if required:
        validator.add_rule(Validator.required())
    
    validator.add_rule(StringValidator.email())
    
    return validator.validate(value)


def validate_phone(value: Any, country_code: str = "RU", required: bool = True) -> ValidationResult:
    """Быстрая валидация телефона"""
    validator = StringValidator()
    
    if required:
        validator.add_rule(Validator.required())
    
    validator.add_rule(StringValidator.phone(country_code))
    
    return validator.validate(value)


def validate_number(
    value: Any,
    min_value: Optional[Union[int, float]] = None,
    max_value: Optional[Union[int, float]] = None,
    required: bool = True
) -> ValidationResult:
    """Быстрая валидация числа"""
    validator = NumberValidator()
    
    if required:
        validator.add_rule(Validator.required())
    
    # Проверка что это число
    def is_number(val: Any) -> bool:
        try:
            float(val)
            return True
        except (ValueError, TypeError):
            return False
    
    validator.add_rule(Validator.custom(is_number, "Значение должно быть числом"))
    
    if min_value is not None:
        validator.add_rule(Validator.min_value(min_value))
    
    if max_value is not None:
        validator.add_rule(Validator.max_value(max_value))
    
    return validator.validate(value)


# Декораторы для валидации функций

def validate_args(*validators, **kw_validators):
    """
    Декоратор для валидации аргументов функции
    """
    def decorator(func):
        sig = inspect.signature(func)
        param_names = list(sig.parameters.keys())
        
        def wrapper(*args, **kwargs):
            # Собираем все аргументы
            bound_args = sig.bind(*args, **kwargs)
            bound_args.apply_defaults()
            
            all_args = bound_args.arguments
            
            # Валидируем позиционные аргументы
            for i, validator in enumerate(validators):
                if i < len(param_names):
                    param_name = param_names[i]
                    value = all_args[param_name]
                    
                    if isinstance(validator, Validator):
                        result = validator.validate(value, param_name)
                        if not result:
                            raise ValueError(
                                f"Невалидный аргумент '{param_name}': {result.errors[0].message}"
                            )
            
            # Валидируем именованные аргументы
            for param_name, validator in kw_validators.items():
                if param_name in all_args:
                    value = all_args[param_name]
                    
                    if isinstance(validator, Validator):
                        result = validator.validate(value, param_name)
                        if not result:
                            raise ValueError(
                                f"Невалидный аргумент '{param_name}': {result.errors[0].message}"
                            )
            
            return func(*args, **kwargs)
        
        return wrapper
    return decorator


def validate_output(validator: Validator):
    """
    Декоратор для валидации возвращаемого значения функции
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            validation_result = validator.validate(result, "return_value")
            
            if not validation_result:
                raise ValueError(
                    f"Невалидный результат функции: {validation_result.errors[0].message}"
                )
            
            return result
        return wrapper
    return decorator


# Оригинальная функция для обратной совместимости

def is_valid_input(text: str) -> bool:
    """
    Базовая валидация ввода (обратная совместимость)
    
    Args:
        text: Текст для валидации
        
    Returns:
        bool: True если текст валиден
    """
    return isinstance(text, str) and len(text.strip()) > 0


# Пример использования
if __name__ == "__main__":
    print("=" * 60)
    print("Тестирование системы валидации")
    print("=" * 60)
    
    # Тест базовой функции
    print("\n1. Тест базовой функции is_valid_input:")
    print(f"  Пустая строка: {is_valid_input('')}")
    print(f"  Только пробелы: {is_valid_input('   ')}")
    print(f"  Нормальный текст: {is_valid_input('Hello')}")
    
    # Тест валидатора строк
    print("\n2. Тест StringValidator:")
    email_validator = StringValidator()
    email_validator.add_rule(Validator.required())
    email_validator.add_rule(StringValidator.email())
    
    email_result = email_validator.validate("test@example.com", "email")
    print(f"  Валидный email: {email_result.is_valid}")
    
    bad_email_result = email_validator.validate("invalid-email", "email")
    print(f"  Невалидный email: {bad_email_result.is_valid}")
    if bad_email_result.errors:
        print(f"  Ошибка: {bad_email_result.errors[0].message}")
    
    # Тест быстрой валидации
    print("\n3. Тест быстрой валидации:")
    quick_result = validate_email("user@domain.com")
    print(f"  Быстрая валидация email: {quick_result.is_valid}")
    
    # Тест валидации схемы
    print("\n4. Тест SchemaValidator:")
    
    user_schema = SchemaValidator({
        "name": [
            Validator().add_rule(Validator.required())
                       .add_rule(Validator.min_length(2))
                       .add_rule(Validator.max_length(50)),
        ],
        "email": StringValidator()
            .add_rule(Validator.required())
            .add_rule(StringValidator.email()),
        "age": NumberValidator()
            .add_rule(Validator.required())
            .add_rule(Validator.min_value(18))
            .add_rule(Validator.max_value(120)),
    })
    
    user_data = {
        "name": "John",
        "email": "john@example.com",
        "age": 25,
        "extra_field": "should trigger warning"
    }
    
    schema_result = user_schema.validate(user_data)
    print(f"  Валидация схемы: {schema_result.is_valid}")
    print(f"  Ошибки: {len(schema_result.errors)}")
    print(f"  Предупреждения: {len(schema_result.warnings)}")
    
    # Тест декоратора
    print("\n5. Тест декоратора валидации:")
    
    @validate_args(
        Validator().add_rule(Validator.required()).add_rule(Validator.min_length(3)),
        NumberValidator().add_rule(Validator.required()).add_rule(Validator.min_value(0))
    )
    @validate_output(NumberValidator().add_rule(Validator.min_value(0)))
    def calculate_price(name: str, quantity: int) -> float:
        """Пример функции с валидацией"""
        return len(name) * quantity * 10.5
    
    try:
        price = calculate_price("Product", 5)
        print(f"  Расчет цены: {price}")
        
        # Это вызовет ошибку валидации
        # price = calculate_price("Pr", -5)
    except ValueError as e:
        print(f"  Ошибка валидации: {e}")
    
    print("\n" + "=" * 60)
    print("Все тесты завершены!")
    print("=" * 60)