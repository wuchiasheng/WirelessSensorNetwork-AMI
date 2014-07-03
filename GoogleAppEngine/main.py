#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import jinja2
import os
import datetime
from google.appengine.ext import ndb

MAIN_PAGE_HTML = """\
<html>
  <head>
    <script type='text/javascript' src='https://www.google.com/jsapi'></script>
    <script type='text/javascript'>
      google.load('visualization', '1', {packages:['table']});
      google.setOnLoadCallback(drawTable);
      function drawTable() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Sensor ID');
        data.addColumn('string', 'Sensor Name');
        data.addColumn('string', 'Value');

        {% for greeting in greetings %}
	data.addRow(['{{}}','TCA','28.06']);
	{% endfor %}	
		
		
        var table = new google.visualization.Table(document.getElementById('table_div'));
		
        table.draw(data, {showRowNumber: true});
		
      }
    </script>
  </head>

  <body>
    <div id='table_div'></div>
  </body>
</html>
"""
JINJA_ENVIRONMENT = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
    extensions=['jinja2.ext.autoescape'],
    autoescape=True)


class sensorParser(ndb.Model):
    sensorID = ndb.StringProperty()
    sensorName = ndb.StringProperty()
    sensorValue = ndb.StringProperty()
    dateTime = ndb.DateTimeProperty()

class MainHandler(webapp2.RequestHandler):
    def get(self):
        date = datetime.datetime.strptime('07/01/2014', '%m/%d/%Y')
        sensorQuery=sensorParser.query( ndb.AND(sensorParser.dateTime < date,sensorParser.sensorID =="A03",sensorParser.sensorName == "TCA"))
        sensorDatas = sensorQuery.fetch(12)
        #for sensorData in sensorDatas:
        #self.response.write(sensorData.sensorName)
        
        template_values = {
            'sensorDatas': sensorDatas,
        }
        
        template = JINJA_ENVIRONMENT.get_template('index.html')
        self.response.write(template.render(template_values))     
            
        #self.response.write(MAIN_PAGE_HTML)

class temperature(webapp2.RequestHandler):
    def get(self):
        date = datetime.datetime.strptime('07/01/2014', '%m/%d/%Y')
        sensorQuery=sensorParser.query( ndb.AND(sensorParser.dateTime < date,sensorParser.sensorID =="A03",sensorParser.sensorName == "TCA"))
        sensorDatas = sensorQuery.fetch(20)
        #for sensorData in sensorDatas:
        #self.response.write(sensorData.sensorName)
        
        template_values = {
            'sensorDatas': sensorDatas,
        }
        
        template = JINJA_ENVIRONMENT.get_template('line.html')
        self.response.write(template.render(template_values))     
            
        #self.response.write(MAIN_PAGE_HTML)

app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/temperature', temperature)
], debug=True)
