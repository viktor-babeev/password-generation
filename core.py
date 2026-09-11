#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
core.py
Enterprise-grade automated strong password generation engine.

(c) 2026 Your Name/Nickname <your_email@example.com>
Terms of Use: This code is licensed under CC BY-NC 4.0.
"""

import string
import secrets
from dataclasses import dataclass
from typing import List, Set

@dataclass
class PasswordConfig:
    """Конфигурация требований к паролю"""
    length: int = 12
    upper_count: int = 3
    lower_count: int = 3
    digits_count: int = 3
    special_count: int = 3
    forbidden_specials: Set[str] = ('`', '~', '|', "'")

def zero_memory_bytearray(b: bytearray) -> None:
    """
    Безопасно затирает массив байт нулями в памяти.
    Для изменяемых типов (bytearray) это работает стабильно и без сбоев.
    """
    if b:
        for i in range(len(b)):
            b[i] = 0

class PasswordGeneratorEngine:
    """Изолированное ядро генерации. Не зависит от интерфейса/GUI."""
    def __init__(self, config: PasswordConfig = PasswordConfig()):
        self.config = config
        self._allowed_specials: List[str] = [
            c for c in string.punctuation if c not in self.config.forbidden_specials
        ]
        self._validate_config_integrity()

    def _validate_config_integrity(self) -> None:
        """Проверка валидности конфигурации при инициализации"""
        total_required = (
            self.config.upper_count + 
            self.config.lower_count + 
            self.config.digits_count + 
            self.config.special_count
        )
        if total_required > self.config.length:
            raise ValueError("Сумма обязательных символов превышает общую длину пароля!")

    def generate_password_bytes(self) -> bytearray:
        """Криптографически безопасная генерация пароля в виде bytearray"""
        upper = [secrets.choice(string.ascii_uppercase) for _ in range(self.config.upper_count)]
        lower = [secrets.choice(string.ascii_lowercase) for _ in range(self.config.lower_count)]
        digits = [secrets.choice(string.digits) for _ in range(self.config.digits_count)]
        specials = [secrets.choice(self._allowed_specials) for _ in range(self.config.special_count)]

        password_list = upper + lower + digits + specials

        if len(set(password_list)) < self.config.length:
            return self.generate_password_bytes()

        secrets.SystemRandom().shuffle(password_list)
        
        # Переводим в изменяемый массив байт (ASCII кодировка)
        return bytearray("".join(password_list).encode('ascii'))
