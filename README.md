# ynab-currency-converter
This is a short script to convert values in a ynab budget to another currency.

## Instructions
Backup your .ynab4 file/folder into the same folder as ynab-converter.py. Then run using 'python ynab-converter.py <ynab4_file> <multiplier>'
The script will then copy the current budget and multiply all the amounts by the multiplier. There seems to be some issues with split transactions but otherwise it seems to work fine. Remember to change the currency when you open the converted budget in YNAB afterwards.