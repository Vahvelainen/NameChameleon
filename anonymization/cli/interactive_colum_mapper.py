from typing import Dict
from prompt_toolkit import Application
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.layout import Layout, HSplit, Window
from prompt_toolkit.layout.controls import FormattedTextControl
from prompt_toolkit.formatted_text import FormattedText


COLUMN_TYPES = ['first_name', 'last_name', 'full_name', 'full_name_inverted', 'email', 'id', 'misc', 'skip']


class ColumnMappingUI:
    
    def __init__(self, columns: list[str]):
        self.columns = columns
        self.selected_types = {col: 'skip' for col in columns}
        self.current_row = 0
        self.cancelled = False
    
    def run(self) -> Dict[str, str]:
        print("\n📋 Column Mapping Configuration")
        print("Use ↑↓ to navigate, ←→ to change type, Enter to save, Ctrl+C to cancel\n")
        
        kb = self._create_key_bindings()
        layout = self._create_layout()
        
        app = Application(
            layout=layout,
            key_bindings=kb,
            full_screen=False,
            mouse_support=False
        )
        
        app.run()
        
        return self._get_result()
    
    def _create_key_bindings(self) -> KeyBindings:
        kb = KeyBindings()
        
        @kb.add('up')
        def move_up(event):
            self.current_row = max(0, self.current_row - 1)
        
        @kb.add('down')
        def move_down(event):
            self.current_row = min(len(self.columns) - 1, self.current_row + 1)
        
        @kb.add('left')
        def cycle_type_left(event):
            self._cycle_type(-1)
        
        @kb.add('right')
        def cycle_type_right(event):
            self._cycle_type(1)
        
        @kb.add('enter')
        def save(event):
            event.app.exit()
        
        @kb.add('c-c')
        def cancel(event):
            self.cancelled = True
            event.app.exit()
        
        return kb
    
    def _cycle_type(self, direction: int) -> None:
        column = self.columns[self.current_row]
        current_type = self.selected_types[column]
        current_idx = COLUMN_TYPES.index(current_type)
        new_idx = (current_idx + direction) % len(COLUMN_TYPES)
        self.selected_types[column] = COLUMN_TYPES[new_idx]
    
    def _create_layout(self) -> Layout:
        return Layout(
            HSplit([
                Window(
                    content=FormattedTextControl(self._get_formatted_text),
                    wrap_lines=False
                )
            ])
        )
    
    def _get_formatted_text(self):
        lines = [('', '  Column Name                          Type\n')]
        lines.append(('', '  ' + '─' * 50 + '\n'))
        
        for i, column in enumerate(self.columns):
            col_type = self.selected_types[column]
            
            if i == self.current_row:
                prefix = '❯ '
                style = 'bg:#0066cc #ffffff bold'
            else:
                prefix = '  '
                style = ''
            
            col_display = column[:30].ljust(30)
            type_display = f"← {col_type} →".center(18)
            
            lines.append((style, f"{prefix}{col_display} {type_display}\n"))
        
        lines.append(('', '\n'))
        lines.append(('', '  ↑↓: Navigate  ←→: Change type  Enter: Save  Ctrl+C: Cancel\n'))
        
        return FormattedText(lines)
    
    def _get_result(self) -> Dict[str, str]:
        if self.cancelled:
            print("\n❌ Configuration cancelled")
            raise KeyboardInterrupt()
        
        column_config = {col: typ for col, typ in self.selected_types.items() if typ != 'skip'}
        
        if column_config:
            print("\n✓ Configuration saved!")
        else:
            print("\n⚠ No columns configured")
        
        return column_config

