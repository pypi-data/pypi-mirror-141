# plot2html
### Helping people publish beautiful automated reports that contribute to transparency, high quality monitoring and faster decision making

With this library, you can create static .html files with text and charts using Google Charts API.

On the command line:
```
pip install plot2html
```

Example data:
```python
import pandas as pd
temp = pd.read_csv('https://raw.githubusercontent.com/rafatro/plot2html/main/tests/Temperature_London_Rome.csv',parse_dates=[0])
```

Your python code:
```python
from plot2html import CreateReport
rep = CreateReport("Example of plot2html Report")
rep.text("<h2>Smart title you can create</h2>This is an example what what you can do with plot2html.")
options = {'title': 'Average temperature at London and Rome',
           'hAxis': {'title': 'Date'},
           'vAxis': {'title': 'Average Daily Temperature (Celsius)'},
           'colors': ['#a52714', '#097138']
          }
rep.plot(data=temp.pivot(index='date', columns='location', values='tavg').reset_index()
         ,x='date'
         ,y=['London','Rome']
         ,type='line'
         ,width='half'
         ,height=400
         ,options=options)
rep.text('''This text is an explanation about the chart to the left.<br>
The first chart above shows data from <a href='https://meteostat.net/'>Meteostat</a>, that provides open source data about meteorology.<br>
You can see Rome temperatures follow the same trend as London's, because both cities are in the northern hemisphere, but Rome is a bit hotter, especialy on the summer.
''',width="half")
rep.exporthtml("C:/Users/rafae/Desktop/plot2html/tests/index.html")
```

You will get this output:

![example screenshot](https://raw.githubusercontent.com/rafatro/plot2html/main/tests/example.jpg)

This is just the begining.
