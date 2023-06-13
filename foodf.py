import pandas as pd
import PySimpleGUI as sg

# Read data from the Excel sheet
df = pd.read_excel("Demo.xlsx")

# Define the layout of the interface
layout = [
    [sg.Text('Enter your budget:'), sg.Input()],
    [sg.Button('Filter')],
    [sg.Text('Results:', font=('Arial', 12, 'bold'))],
    [sg.Listbox(values=[], size=(50, 6), font=('Arial', 12), key='LISTBOX')],
    [sg.Text('Should eat:', font=('Arial', 12, 'bold')), sg.Text('', key='SHOULD_EAT')],
    [sg.Text('Should not eat:', font=('Arial', 12, 'bold')), sg.Text('', key='SHOULD_NOT_EAT')],
    [sg.Text('Overall review:', font=('Arial', 12, 'bold')), sg.Text('', key='OVERALL_REVIEW')],
    [sg.Checkbox('Display friends reviews', default=False, key='DISPLAY_FRIENDS')],
    [sg.Text('Address:', font=('Arial', 12, 'bold')), sg.Text('', key='ADDRESS')],
    [sg.Button('Quit')]
]

# Create the window
window = sg.Window('Food Search', layout)

# Main event loop
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Quit':
        break
    if event == 'Filter':
        # Filter data based on the user's budget
        budget = float(values[0])
        filtered_df = df[df['Price'] <= budget][['Item name ', 'Review', 'who shouldnt eat', 'friends review', 'Shop name', 'Address']]
        items = filtered_df['Item name '].tolist()
        # Display filtered items in the list box
        window['SHOULD_EAT'].update('')
        window['SHOULD_NOT_EAT'].update('')
        window['OVERALL_REVIEW'].update('')
        window['ADDRESS'].update('')
        window['DISPLAY_FRIENDS'].update(False)
        window['LISTBOX'].update(values=items)
    if event == 'LISTBOX' and len(values['LISTBOX']) > 0:
        # Display information about the selected item
        item_name = values['LISTBOX'][0]
        item_row = filtered_df[filtered_df['Item name '] == item_name]
        should_eat = item_row.iloc[0]['Review']
        should_not_eat = item_row.iloc[0]['who shouldnt eat']
        overall_review = item_row.iloc[0]['Review']
        address = item_row.iloc[0]['Address']
        if values['DISPLAY_FRIENDS']:
            overall_review += '\n\nFriends review: ' + item_row.iloc[0]['friends review']
        window['SHOULD_EAT'].update(should_eat)
        window['SHOULD_NOT_EAT'].update(should_not_eat)
        window['OVERALL_REVIEW'].update(overall_review)
        window['ADDRESS'].update(address)
    elif event == 'LISTBOX' and len(values['LISTBOX']) == 0:
        window['SHOULD_EAT'].update('')
        window['SHOULD_NOT_EAT'].update('')
        window['OVERALL_REVIEW'].update('')
        window['ADDRESS'].update('')

# Close the window
window.close()