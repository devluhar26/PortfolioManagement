import os
import random
import sqlite3
from datetime import datetime

from nicegui import ui

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


with ui.tabs().classes('w-full') as tabs:
    one = ui.tab('Overview')
    two = ui.tab('export data')

with ui.tab_panels(tabs, value=one).classes('w-full'):
    with ui.tab_panel(one):
        ui.label('First tab')
        label = ui.label()
        ui.timer(0.001, lambda: label.set_text(f'{datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}'))
    columns = [
        {'name': 'name', 'label': 'Name', 'field': 'name'},
        {'name': 'age', 'label': 'Age', 'field': 'age'},
    ]
    rows = [
        {'name': 'Alice', 'age': 18},
        {'name': 'Bob', 'age': 21},
        {'name': 'Carol'},
    ]

    table = ui.table(columns=columns, rows=rows, row_key='name').classes('w-72')
    table.add_slot('header', r'''
        <q-tr :props="props">
            <q-th auto-width />
            <q-th v-for="col in props.cols" :key="col.name" :props="props">
                {{ col.label }}
            </q-th>
        </q-tr>
    ''')
    table.add_slot('body', r'''
        <q-tr :props="props">
            <q-td auto-width>
                <q-btn size="sm" color="accent" round dense
                    @click="props.expand = !props.expand"
                    :icon="props.expand ? 'remove' : 'add'" />
            </q-td>
            <q-td v-for="col in props.cols" :key="col.name" :props="props">
                {{ col.value }}
            </q-td>
        </q-tr>
        <q-tr v-show="props.expand" :props="props">
            <q-td colspan="100%">
                <div class="text-left">This is {{ props.row.name }}.</div>
            </q-td>
        </q-tr>
    ''')

    with ui.tab_panel(two):
        ui.label('Second tab')


ui.run()

# Run NiceGUI on a different port
if __name__ in {"__main__", "__mp_main__"}:

    ui.run(host='0.0.0.0', port=8080)
