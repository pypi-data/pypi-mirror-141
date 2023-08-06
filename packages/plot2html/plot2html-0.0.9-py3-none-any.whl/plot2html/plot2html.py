from datetime import datetime
from pandas import isna
from pandas.api.types import is_datetime64_any_dtype, is_numeric_dtype

class CreateReport:
    "Creates a static .html file with charts using Google Charts API"
    
    def __init__(self,title):
        self.title = title
        self.html_string = ""
        self.partitionsFilled = 0.0
        self.chartCount=0
        self.partition=1.0
    
    def setupNewChart(self,width):
        #insert data input validation in list
        if (width=="full"): self.partition = 1.0
        if (width=="half"): self.partition = 2.0
        if (width=="third"): self.partition = 3.0
        if (width=="2-thirds"): self.partition = 3.0/2.0
        if (width=="quarter"): self.partition = 4.0
        if (round(self.partitionsFilled + 1.0/self.partition,2) > 1):
            self.html_string += "</div>\n"
            self.partitionsFilled = 0
        if (self.partitionsFilled==0):
            self.html_string += "<div class='flex-container'>\n"
        self.partitionsFilled += 1.0/self.partition
        self.chartCount+=1
    
    def text(self,html_text,width="full"):
        self.setupNewChart(width);
        self.html_string += "<div style='width:" + "{:.2%}".format(1.0/self.partition) + ";'><p>" + html_text + "</p></div>\n"
        
    def plot(self,data,x,y,type="line",width="full",height=400,options={}):
        self.setupNewChart(width);
        self.html_string += '''
<div id="chart_div''' + str(self.chartCount) + '''" style="width:''' + "{:.2%}".format(1.0/self.partition) + ''';height:''' + str(height) + '''px;"></div>
<script type="text/javascript">
google.charts.load('current', {packages: ['corechart']});
google.charts.setOnLoadCallback(drawChart''' + str(self.chartCount) + ''');

function drawChart''' + str(self.chartCount) + '''() {
      var data = new google.visualization.DataTable();\n''';
        if (is_datetime64_any_dtype(data[x])): self.html_string += "data.addColumn('date', '" + x + "');\n";
        elif (is_numeric_dtype(data[x])):  self.html_string += "data.addColumn('number', '" + x + "');\n";
        else:  self.html_string += "data.addColumn('string', '" + x + "');\n";
        for a in y:
            if (is_numeric_dtype(data[a])):  self.html_string += "data.addColumn('number', '" + a + "');\n";
            else:  self.html_string += "data.addColumn('string', '" + a + "');\n";
        self.html_string += "data.addRows([\n";
        for index, row in data.iterrows():
            if (is_datetime64_any_dtype(data[x])): self.html_string+="[new Date("+str(row[x].year)+","+str(row[x].month-1)+","+str(row[x].day)+"),";
            else: self.html_string += "[" + str(row[x]) + ",";
            for a in y:
                if (isna(row[a])): self.html_string += "null,";
                else: self.html_string += str(row[a]) + ",";
            self.html_string += "],\n"
        self.html_string += "]);\n";
        self.html_string += " var options = " + str(options) + ";\n"
        types={'line':'LineChart','column':'ColumnChart'}
        self.html_string += "var chart = new google.visualization.{}".format(types[type]);
        self.html_string += "(document.getElementById('chart_div" + str(self.chartCount) + ''''));
      chart.draw(data, options);}
</script>
        '''
        
    def exporthtml(self,full_path):
        f = open(full_path, "w")
        html_string_full = '''
<!DOCTYPE html>
<!-- This .html file was created using Python Library plot2html -->
<head>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
body {
  margin: 0;
  padding-top: 80px; /* is overwriten by javascript */
  font-family: Arial, Helvetica, sans-serif;
  color: #444444;
}
.fixed-header {
  width: 100%;
  margin: 0 ;
  padding: 0;
  display: flex;
  justify-content: space-between;
  position: fixed;
  background: #DDDDDD;
  border-bottom: 1px solid #666;
  box-shadow: 0px 1px 4px 1px #999;
  top: 0;
  font-weight: bold;
  font-size: 24px;
}
.fixed-header > div {
  text-align: center;
  padding: 20px 16px;
}
.content {
  padding: 10px 16px;
}
.flex-container {
  display: flex;
  flex-wrap: nowrap;
}

</style>
<script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
</head>
<body>
<div class="fixed-header" id="myHeader">
  <div>link</div>
  <div>''' + self.title + '''</div>
  <div>''' + datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S") + ''' UTC</div>
</div>
<script type="text/javascript">
  function adjustHeaderHeight(){
    document.body.style.paddingTop = document.getElementById('myHeader').clientHeight + "px";
  }
window.addEventListener("resize", adjustHeaderHeight);
adjustHeaderHeight();
</script>
<div class="content">
''' + self.html_string
        if (self.partitionsFilled > 0):
            html_string_full += "</div>\n"
        html_string_full += "</div></body></html>"
        f.write(html_string_full)
        f.close()
        print("File exported to "+full_path);