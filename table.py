class Table:
    def __init__(self) -> None:
        self.header = []
        self.rows = []

    def set_header(self, *labels):
        self.header = labels

    def add_row(self, *values):
        self.rows.append(values)

    @staticmethod
    def render_row_string(*values) -> str:
        string = '<TR>'
        for val in values:
            string += f'<TD>{str(val)}</TD>'
        string += '</TR>'
        return string

    def render_table_string(self) -> str:
        string = '<<TABLE>'
        string += self.render_row_string(*self.header)
        for row in self.rows:
            string += self.render_row_string(*row)
        string += '</TABLE>>'
        return string

    def get_gv_html(self) -> str:
        return self.render_table_string()
