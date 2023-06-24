from kivymd.theming import ThemableBehavior
from kivymd.uix.datatables.datatables import MDDataTable, TableHeader, TableData, TablePagination
from kivy.clock import Clock
from functools import partial

# https://stackoverflow.com/a/63476203/704681
class AppDataTable(MDDataTable):
        def __init__(self, **kwargs):
            # skip the MDDataTable.__init__() and call its superclass __init__()
            super(ThemableBehavior, self).__init__(**kwargs)
    
            # schedule call to MDDataTable.__init__() contents after ids are populated
            Clock.schedule_once(partial(self.delayed_init, **kwargs))
    
        def delayed_init(self, dt, **kwargs):
            # this is copied from MDDataTable.__init__() with super() call deleted
            self.header = TableHeader(
                column_data=self.column_data,
                sorted_on=self.sorted_on,
                sorted_order=self.sorted_order,
            )
            self.table_data = TableData(
                self.header,
                row_data=self.row_data,
                check=self.check,
                rows_num=self.rows_num,
                _parent=self,
            )
            self.register_event_type("on_row_press")
            self.register_event_type("on_check_press")
            self.pagination = TablePagination(table_data=self.table_data)
            self.table_data.pagination = self.pagination
            self.header.table_data = self.table_data
            self.table_data.fbind("scroll_x", self._scroll_with_header)
            self.ids.container.add_widget(self.header)
            self.ids.container.add_widget(self.table_data)
            if self.use_pagination:
                self.ids.container.add_widget(self.pagination)
            Clock.schedule_once(self.create_pagination_menu, 0.5)
            self.bind(row_data=self.update_row_data)
