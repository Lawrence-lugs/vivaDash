# ViVA Exported CSV AutoPlotter

Simple web GUI for plotting transient CSVs exported from Cadence ViVA

Uses plotly/dash and pandas

## How to use

`$ git clone https://github.com/Lawrence-lugs/vivaDash.git`

`$ pip install pandas`

`$ pip install dash`

`$ python vivaDash.py`

Next, export your waveforms as CSV from ViVA:
1. CTRL + SHIFT + A
2. Right Click -> Send to -> Export -> Change filetype to CSV
3. Export to vivaDash/waveforms/yourFile.csv

Dash should open the website at `http://127.0.0.1:8050/`
If not at port 8050, it should print whichever port it's working at in the terminal.

New customizations to the plot can be added by changing the fig plotly express calls in `vivaDash.py`

```Python
fig = px.line(df,y='value',x='time',facet_row='family',color='variable')
```

Please raise a github issue if it's not working.