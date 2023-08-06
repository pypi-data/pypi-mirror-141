from Orange.widgets.widget import OWWidget
from Orange.data import Table, Domain, ContinuousVariable
from orangewidget.widget import Output, Input
from orangewidget import gui


class Case(OWWidget):
    name = 'Case'
    icon = 'icons/case.png'
    description = '''Switch-case statement for Orange3'''
    want_main_area = False

    input = None

    cases = ''
    results = ''
    default = ''

    def __init__(self):
        super().__init__()

        self.optionsBox = gui.widgetBox(self.controlArea, 'Logic')

        gui.lineEdit(self.optionsBox, self, 'cases', 'Enter a conditions. A list of objects comma separated. E.g. dog,cat,horse', callback=self.commit)
        gui.lineEdit(self.optionsBox, self, 'results', 'Enter the outputs. A list of objects comma separated. E.g. 10, 20, 30', callback=self.commit)

        gui.lineEdit(self.optionsBox, self, 'default', 'Default value if none of conditions exist above.', callback=self.commit)

    class Inputs:
        data = Input('Data', object, auto_summary=False)

    class Outputs:
        data = Output('Data', object, auto_summary=False)

    def commit(self):
        if self.input is None:
            return

        if not self.cases or not self.results:
            return

        cases = self.cases.split(',')
        results = self.results.split(',')

        if len(cases) != len(results):
            return

        domain = Domain([ContinuousVariable(name='Output')])

        for case, result in zip(cases, results):
            if case == self.input:
                self.Outputs.data.send(Table.from_list(domain, [[result]]))
                return

        self.Outputs.data.send(Table.from_list(domain, [[self.default]]))

    @Inputs.data
    def set_data(self, data):
        if type(data) == Table:
            if len(data) == 0 or len(data[0]) == 0:
                return

            self.input = data[0][0].value
        else:
            self.input = data

        self.commit()

if __name__ == '__main__':
    from Orange.widgets.utils.widgetpreview import WidgetPreview  # since Orange 3.20.0
    WidgetPreview(Case).run()
