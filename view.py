#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
view.py
Enterprise Graphical User Interface (GUI) with Tabview layout and dynamic inputs.

(c) 2026 Your Name/Nickname <your_email@example.com>
Terms of Use: This code is licensed under CC BY-NC 4.0.
"""

import os
import sys
import threading
from tkinter import filedialog, messagebox
import customtkinter as ctk

# Imports from core
from core import PasswordGeneratorEngine, zero_memory_bytearray, PasswordConfig

if getattr(sys, 'frozen', False):
    BASE_DIR = os.path.dirname(sys.executable)
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

LOCALIZATION = {
    "RU": {
        "title": "Генератор Паролей Enterprise",
        "tab_params": "⚙️ Параметры",
        "tab_input": "📥 Входные данные",
        "tab_output": "📤 Выходные данные",
        "btn_input": "Выбрать файл ФИО",
        "btn_output": "Куда сохранить",
        "btn_start": "🚀 Запустить генерацию",
        "btn_copy": "📋 Копировать результат",
        "status_no_file": "Файл не выбран",
        "status_ready": "Готов к работе",
        "status_processing": "Обработка данных...",
        "status_success": "Готово! Пароли успешно сформированы.",
        "status_error": "Процесс прерван ошибкой",
        "err_select_files": "Пожалуйста, укажите пути к файлам или заполните поле ввода!",
        "err_security": "Запрещено выбирать файлы вне папки программы!",
        "err_empty": "Источник входных данных пуст!",
        "err_title": "Ошибка",
        "msg_success_title": "Успех",
        "msg_success_text": "Генерация паролей успешно завершена!",
        "dialog_input_title": "Выберите файл со списком ФИО",
        "dialog_output_title": "Укажите файл для сохранения результатов",
        "lbl_length": "Итоговая длина пароля:",
        "lbl_upper": "Заглавные (A-Z):",
        "lbl_lower": "Строчные (a-z):",
        "lbl_digits": "Цифры (0-9):",
        "lbl_specials": "Спецсимволы:",
        "chk_input_file": "Использовать текстовый файл",
        "chk_input_manual": "Ввести ФИО прямо в программе",
        "chk_output_file": "Сохранить в файл отчета",
        "chk_output_manual": "Вывести результат в окно ниже",
        "strength_weak": "Критически короткий / Опасно",
        "strength_medium": "Средний уровень защиты",
        "strength_strong": "Надежный пароль",
        "strength_excellent": "Высшая корпоративная безопасность"
    },
    "EN": {
        "title": "Enterprise Password Generator",
        "tab_params": "⚙️ Parameters",
        "tab_input": "📥 Input Data",
        "tab_output": "📤 Output Data",
        "btn_input": "Select Names File",
        "btn_output": "Save Result To",
        "btn_start": "🚀 Run Generation",
        "btn_copy": "📋 Copy Result",
        "status_no_file": "File not selected",
        "status_ready": "Ready to work",
        "status_processing": "Processing data...",
        "status_success": "Done! Passwords generated successfully.",
        "status_error": "Process interrupted by error",
        "err_select_files": "Please specify file paths or fill the input field!",
        "err_security": "Access denied: Selecting files outside the app directory is prohibited!",
        "err_empty": "Input data source is empty!",
        "err_title": "Error",
        "msg_success_title": "Success",
        "msg_success_text": "Password generation completed successfully!",
        "dialog_input_title": "Select file with full names list",
        "dialog_output_title": "Specify file to save results",
        "lbl_length": "Total Password Length:",
        "lbl_upper": "Uppercase (A-Z):",
        "lbl_lower": "Lowercase (a-z):",
        "lbl_digits": "Digits (0-9):",
        "lbl_specials": "Special Chars:",
        "chk_input_file": "Use source text file",
        "chk_input_manual": "Enter names directly in the app",
        "chk_output_file": "Save to report text file",
        "chk_output_manual": "Show result in the text box below",
        "strength_weak": "Critically short / Dangerous",
        "strength_medium": "Medium Security",
        "strength_strong": "Strong Password",
        "strength_excellent": "Excellent Corporate Security"
    }
}

class PasswordGeneratorApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()

        self.current_lang = "RU"
        self.config = PasswordConfig()
        self.engine = PasswordGeneratorEngine(config=self.config)

        self.title("Password Generation Utility")
        self.geometry("560x520")
        self.resizable(False, False)

        self.input_file_path = os.path.normpath(os.path.join(BASE_DIR, "FioLatinica.txt"))
        self.output_file_path = os.path.normpath(os.path.join(BASE_DIR, "PasswdFile.txt"))

        if not os.path.exists(self.input_file_path):
            try:
                with open(self.input_file_path, "w", encoding="utf-8") as f:
                    f.write("IvanovVL\nPetrovIA\nSidorovAK\n")
            except Exception:
                pass

        self.create_widgets()
        self.update_ui_language()
        self.recalculate_length()

    def create_widgets(self) -> None:
        # Верхняя панель (переключатель языка)
        self.frame_top = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_top.pack(fill="x", padx=30, pady=(10, 0))

        self.lang_switch = ctk.CTkSegmentedButton(
            self.frame_top, values=["RU", "EN"], command=self.change_language, width=70
        )
        self.lang_switch.pack(side="right")
        self.lang_switch.set(self.current_lang)

        # ==================================================================
        # СОЗДАНИЕ ВКЛАДОК (TABVIEW)
        # ==================================================================
        self.tabview = ctk.CTkTabview(self, width=500, height=340)
        self.tabview.pack(padx=20, pady=(5, 10), fill="both", expand=True)

        # Жестко фиксируем ID вкладок, чтобы контент не пропадал при смене языка
        self.tab_p = self.tabview.add("Parameters")
        self.tab_i = self.tabview.add("Input Data")
        self.tab_o = self.tabview.add("Output Data")

        # ------------------------------------------------------------------
        # ВКЛАДКА 1: ПАРАМЕТРЫ
        # ------------------------------------------------------------------
        self.row_length = ctk.CTkFrame(self.tab_p, fg_color="transparent")
        self.row_length.pack(fill="x", pady=(5, 2))
        
        self.lbl_l = ctk.CTkLabel(self.row_length, text="", font=ctk.CTkFont(size=13, weight="bold"))
        self.lbl_l.pack(side="left")
        self.val_lbl_l = ctk.CTkLabel(self.row_length, text="12", font=ctk.CTkFont(size=14, weight="bold"), text_color="#3498db")
        self.val_lbl_l.pack(side="left", padx=5)

        self.frame_strength = ctk.CTkFrame(self.tab_p, fg_color="transparent")
        self.frame_strength.pack(fill="x", pady=(0, 10))
        self.strength_bar = ctk.CTkProgressBar(self.frame_strength, height=5, width=440)
        self.strength_bar.pack(fill="x", expand=True)

        def build_slider_row(parent, start_val, from_, to, callback=None):
            row = ctk.CTkFrame(parent, fg_color="transparent")
            row.pack(fill="x", pady=3)
            lbl = ctk.CTkLabel(row, text="", width=140, anchor="w", font=ctk.CTkFont(size=12))
            lbl.pack(side="left")
            val_lbl = ctk.CTkLabel(row, text=str(start_val), width=30, font=ctk.CTkFont(size=12, weight="bold"))
            
            def on_slider_move(v):
                val_lbl.configure(text=str(int(v)))
                if callback: callback()

            slider = ctk.CTkSlider(row, from_=from_, to=to, number_of_steps=to-from_, height=16, command=on_slider_move)
            slider.set(start_val)
            slider.pack(side="left", fill="x", expand=True, padx=10)
            val_lbl.pack(side="left")
            return lbl, slider

        self.lbl_u, self.sld_upper = build_slider_row(self.tab_p, 3, 0, 10, self.recalculate_length)
        self.lbl_lo, self.sld_lower = build_slider_row(self.tab_p, 3, 0, 10, self.recalculate_length)
        self.lbl_d, self.sld_digits = build_slider_row(self.tab_p, 3, 0, 10, self.recalculate_length)
        self.lbl_s, self.sld_specials = build_slider_row(self.tab_p, 3, 0, 10, self.recalculate_length)

        # ------------------------------------------------------------------
        # ВКЛАДКА 2: ВХОДНЫЕ ДАННЫЕ
        # ------------------------------------------------------------------
        self.input_mode = ctk.StringVar(value="file")

        self.chk_in_file = ctk.CTkRadioButton(
            self.tab_i, text="", variable=self.input_mode, value="file", command=self.toggle_input_widgets
        )
        self.chk_in_file.pack(anchor="w", padx=10, pady=5)

        self.frame_in_file_actions = ctk.CTkFrame(self.tab_i, fg_color="transparent")
        self.frame_in_file_actions.pack(fill="x", padx=30, pady=2)
        self.btn_select_input = ctk.CTkButton(self.frame_in_file_actions, text="", command=self.select_input_file, width=150)
        self.btn_select_input.pack(side="left")
        self.lbl_input_status = ctk.CTkLabel(self.frame_in_file_actions, text="", font=ctk.CTkFont(size=12))
        self.lbl_input_status.pack(side="left", padx=15)

        self.chk_in_manual = ctk.CTkRadioButton(
            self.tab_i, text="", variable=self.input_mode, value="manual", command=self.toggle_input_widgets
        )
        self.chk_in_manual.pack(anchor="w", padx=10, pady=(10, 5))

        self.txt_input_manual = ctk.CTkTextbox(self.tab_i, height=130, font=ctk.CTkFont(size=12))
        self.txt_input_manual.pack(fill="both", expand=True, padx=30, pady=2)
        self.txt_input_manual.insert("0.0", "IvanovVL\nPetrovIA\nSidorovAK")

        # ------------------------------------------------------------------
        # ВКЛАДКА 3: ВЫХОДНЫЕ ДАННЫЕ
        # ------------------------------------------------------------------
        self.output_mode = ctk.StringVar(value="file")

        self.chk_out_file = ctk.CTkRadioButton(
            self.tab_o, text="", variable=self.output_mode, value="file", command=self.toggle_output_widgets
        )
        self.chk_out_file.pack(anchor="w", padx=10, pady=5)

        self.frame_out_file_actions = ctk.CTkFrame(self.tab_o, fg_color="transparent")
        self.frame_out_file_actions.pack(fill="x", padx=30, pady=2)
        self.btn_select_output = ctk.CTkButton(self.frame_out_file_actions, text="", command=self.select_output_file, width=150)
        self.btn_select_output.pack(side="left")
        self.lbl_output_status = ctk.CTkLabel(self.frame_out_file_actions, text="", font=ctk.CTkFont(size=12))
        self.lbl_output_status.pack(side="left", padx=15)

        self.chk_out_manual = ctk.CTkRadioButton(
            self.tab_o, text="", variable=self.output_mode, value="manual", command=self.toggle_output_widgets
        )
        self.chk_out_manual.pack(anchor="w", padx=10, pady=(10, 5))

        self.txt_output_manual = ctk.CTkTextbox(self.tab_o, height=100, font=ctk.CTkFont(size=12), state="disabled")
        self.txt_output_manual.pack(fill="both", expand=True, padx=30, pady=2)

        self.btn_copy_result = ctk.CTkButton(self.tab_o, text="", command=self.copy_to_clipboard, height=28, width=180)
        self.btn_copy_result.pack(pady=(5, 2))

        # ПОДВАЛ ПРОГРАММЫ
        self.lbl_process_status = ctk.CTkLabel(self, text="", font=ctk.CTkFont(size=13))
        self.lbl_process_status.pack(pady=(5, 2))

        self.progress_bar = ctk.CTkProgressBar(self, width=480, height=6)
        self.progress_bar.pack(pady=2)
        self.progress_bar.set(0)

        self.btn_start = ctk.CTkButton(
            self, text="", command=self.start_generation_thread, height=42, width=240,
            font=ctk.CTkFont(size=14, weight="bold"), corner_radius=8
        )
        self.btn_start.pack(pady=(8, 10))

        self.toggle_input_widgets()
        self.toggle_output_widgets()

    def toggle_input_widgets(self) -> None:
        if self.input_mode.get() == "file":
            self.btn_select_input.configure(state="normal")
            self.txt_input_manual.configure(state="disabled", fg_color=("#ebebeb", "#212121"))
        else:
            self.btn_select_input.configure(state="disabled")
            self.txt_input_manual.configure(state="normal", fg_color=("#ffffff", "#2d2d2d"))

    def toggle_output_widgets(self) -> None:
        if self.output_mode.get() == "file":
            self.btn_select_output.configure(state="normal")
            self.btn_copy_result.configure(state="disabled")
            self.txt_output_manual.configure(state="disabled", fg_color=("#ebebeb", "#212121"))
        else:
            self.btn_select_output.configure(state="disabled")
            self.btn_copy_result.configure(state="normal")
            self.txt_output_manual.configure(state="normal", fg_color=("#ffffff", "#2d2d2d"))

    def copy_to_clipboard(self) -> None:
        lang = LOCALIZATION[self.current_lang]
        text_to_copy = self.txt_output_manual.get("0.0", "end").strip()
        if text_to_copy:
            self.clipboard_clear()
            self.clipboard_append(text_to_copy)
            messagebox.showinfo(lang["msg_success_title"], "Результат успешно скопирован!" if self.current_lang == "RU" else "Result copied to clipboard!")
        else:
            messagebox.showwarning(lang["err_title"], lang["err_empty"])

    def change_language(self, selected_lang: str) -> None:
        self.current_lang = selected_lang
        self.update_ui_language()
        self.recalculate_length()

    def update_ui_language(self) -> None:
        lang = LOCALIZATION[self.current_lang]
        
        self.btn_select_input.configure(text=lang["btn_input"])
        self.btn_select_output.configure(text=lang["btn_output"])
        self.btn_start.configure(text=lang["btn_start"])
        self.btn_copy_result.configure(text=lang["btn_copy"])
       
        self.chk_in_file.configure(text=lang["chk_input_file"])
        self.chk_in_manual.configure(text=lang["chk_input_manual"])
        self.chk_out_file.configure(text=lang["chk_output_file"])
        self.chk_out_manual.configure(text=lang["chk_output_manual"])

        self.lbl_l.configure(text=lang["lbl_length"])
        self.lbl_u.configure(text=lang["lbl_upper"])
        self.lbl_lo.configure(text=lang["lbl_lower"])
        self.lbl_d.configure(text=lang["lbl_digits"])
        self.lbl_s.configure(text=lang["lbl_specials"])
        
        if not self.input_file_path:
            self.lbl_input_status.configure(text=lang["status_no_file"], text_color="#8a8a8a")
        if not self.output_file_path:
            self.lbl_output_status.configure(text=lang["status_no_file"], text_color="#8a8a8a")
            
        if self.btn_start.cget("state") == "normal" and self.progress_bar.get() == 0:
            self.lbl_process_status.configure(text=lang["status_ready"], text_color=("#2b2b2b", "#dbdbdb"))

    def recalculate_length(self) -> None:
        lang = LOCALIZATION[self.current_lang]
        required_sum = (
            int(self.sld_upper.get()) + int(self.sld_lower.get()) +
            int(self.sld_digits.get()) + int(self.sld_specials.get())
        )
        self.val_lbl_l.configure(text=str(required_sum))

        if required_sum == 0:
            self.strength_bar.set(0)
            self.lbl_process_status.configure(text=lang["status_ready"], text_color=("#2b2b2b", "#dbdbdb"))
        elif required_sum < 8:
            self.strength_bar.set(required_sum / 24.0)
            self.strength_bar.configure(progress_color="#e74c3c")
            self.lbl_process_status.configure(text=lang["strength_weak"], text_color="#e74c3c")
        elif required_sum < 12:
            self.strength_bar.set(required_sum / 24.0)
            self.strength_bar.configure(progress_color="#e67e22")
            self.lbl_process_status.configure(text=lang["strength_medium"], text_color="#e67e22")
        elif required_sum < 16:
            self.strength_bar.set(required_sum / 24.0)
            self.strength_bar.configure(progress_color="#2ecc71")
            self.lbl_process_status.configure(text=lang["strength_strong"], text_color="#2ecc71")
        else:
            self.strength_bar.set(min(required_sum / 24.0, 1.0))
            self.strength_bar.configure(progress_color="#1abc9c")
            self.lbl_process_status.configure(text=lang["strength_excellent"], text_color="#1abc9c")

    def is_path_forbidden(self, target_path: str) -> bool:
        path_parts = os.path.normpath(target_path).split(os.sep)
        for part in path_parts:
            if part in [".venv", "__pycache__"] or part.startswith('.'):
                return True
        return False

    def select_input_file(self) -> None:
        lang = LOCALIZATION[self.current_lang]
        file_path = filedialog.askopenfilename(
            initialdir=BASE_DIR, title=lang["dialog_input_title"],
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if file_path:
            norm_base = os.path.normpath(BASE_DIR)
            norm_file = os.path.normpath(file_path)
            if self.is_path_forbidden(norm_file):
                messagebox.showerror(lang["err_title"], "Выбор файлов из системных или скрытых папок (.venv, __pycache__) ЗАПРЕЩЕН!")
                return
            if os.path.commonpath([norm_base]) != os.path.commonpath([norm_base, norm_file]):
                messagebox.showerror(lang["err_title"], lang["err_security"])
                return
            self.input_file_path = norm_file
            self.lbl_input_status.configure(text=os.path.basename(norm_file), text_color="#2ecc71")

    def select_output_file(self) -> None:
        lang = LOCALIZATION[self.current_lang]
        file_path = filedialog.asksaveasfilename(
            initialdir=BASE_DIR, title=lang["dialog_output_title"],
            defaultextension=".txt", filetypes=[("Text Files", "*.txt")]
        )
        if file_path:
            norm_base = os.path.normpath(BASE_DIR)
            norm_file = os.path.normpath(file_path)
            if self.is_path_forbidden(norm_file):
                messagebox.showerror(lang["err_title"], "Сохранение файлов в системные или скрытых папки (.venv, __pycache__) ЗАПРЕЩЕНО!")
                return
            if os.path.commonpath([norm_base]) != os.path.commonpath([norm_base, norm_file]):
                messagebox.showerror(lang["err_title"], lang["err_security"])
                return
            self.output_file_path = norm_file
            self.lbl_output_status.configure(text=os.path.basename(norm_file), text_color="#2ecc71")

    def start_generation_thread(self) -> None:
        lang = LOCALIZATION[self.current_lang]
        if self.input_mode.get() == "file" and not self.input_file_path:
            messagebox.showwarning(lang["err_title"], lang["err_select_files"])
            return
        if self.output_mode.get() == "file" and not self.output_file_path:
            messagebox.showwarning(lang["err_title"], lang["err_select_files"])
            return

        l_val = int(self.val_lbl_l.cget("text"))
        if l_val == 0:
            messagebox.showwarning(lang["err_title"], "Длина пароля не может быть равна 0!" if self.current_lang == "RU" else "Password length cannot be 0!")
            return

        self.config.length = l_val
        self.config.upper_count = int(self.sld_upper.get())
        self.config.lower_count = int(self.sld_lower.get())
        self.config.digits_count = int(self.sld_digits.get())
        self.config.special_count = int(self.sld_specials.get())

        self.btn_start.configure(state="disabled")
        self.lbl_process_status.configure(text=lang["status_processing"], text_color="#e67e22")
        self.progress_bar.start()

        threading.Thread(target=self.process_files, daemon=True).start()

    def process_files(self) -> None:
        """Универсальный процессинг для файлов и окон прямого ввода"""
        lang = LOCALIZATION[self.current_lang]
        try:
            if self.input_mode.get() == "file":
                with open(self.input_file_path, "r", encoding="utf-8") as f_in:
                    lines = [line.strip() for line in f_in if line.strip()]
            else:
                raw_text = self.txt_input_manual.get("0.0", "end")
                lines = [line.strip() for line in raw_text.split("\n") if line.strip()]

            if not lines:
                self.after(0, self.reset_ui_after_error, lang["err_empty"])
                return

            output_buffer = []
            for line in lines:
                pwd_bytes = self.engine.generate_password_bytes()
                formatted_line = f"{line}   |   {pwd_bytes.decode('ascii')}\n==========================================\n"
                output_buffer.append((formatted_line, pwd_bytes))

            if self.output_mode.get() == "file":
                with open(self.output_file_path, "w", encoding="utf-8") as f_out:
                    for fmt_line, _ in output_buffer:
                        f_out.write(fmt_line)
            else:
                full_output_text = "".join([fmt_line for fmt_line, _ in output_buffer])
                self.after(0, lambda: self.txt_output_manual.configure(state="normal"))
                self.after(0, lambda: self.txt_output_manual.delete("0.0", "end"))
                self.after(0, lambda text=full_output_text: self.txt_output_manual.insert("0.0", text))

            for _, pwd_bytes in output_buffer:
                zero_memory_bytearray(pwd_bytes)

            self.after(0, self.on_generation_success)

        except Exception as e:
            self.after(0, self.reset_ui_after_error, f"{lang['status_error']}: {str(e)}")

    def on_generation_success(self) -> None:
        lang = LOCALIZATION[self.current_lang]
        self.progress_bar.stop()
        self.progress_bar.set(1)
        self.btn_start.configure(state="normal")
        self.lbl_process_status.configure(text=lang["status_success"], text_color="#2ecc71")
        
        if self.output_mode.get() == "manual":
            self.tabview.set("Output Data")
            
        messagebox.showinfo(lang["msg_success_title"], lang["msg_success_text"])

    def reset_ui_after_error(self, message: str) -> None:
        lang = LOCALIZATION[self.current_lang]
        self.progress_bar.stop()
        self.progress_bar.set(0)
        self.btn_start.configure(state="normal")
        self.lbl_process_status.configure(text=lang["status_error"], text_color="#e74c3c")
        messagebox.showerror(lang["err_title"], message)

