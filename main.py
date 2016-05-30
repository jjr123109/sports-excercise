#!/usr/bin/env python
#
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

import json
import re
from google.appengine.api import images
import webapp2

class MainHandler(webapp2.RequestHandler):
    def get(self):
        # Not required for the exercise.
        pass
         
    def post(self):
        try:
            # json lib doesn't like trailing comma
            request = json.loads(re.sub(',[ \t\r\n]*\]', ']', self.request.body))
            inputs, heights, widths = [], [], []
            for element in request:
                # open file if fails then bad file
                image = images.Image(image_data=(open("img/"+element['filename'], "rb").read()))
            
                # check positive
                x = int(element['x'])
                if (x < 0):
                    raise ValueError('X Offset is invalid: ' + str(x))
                  
                y = int(element['y'])
                if (y < 0):
                    raise ValueError('Y Offset is invalid: ' + str(y))
            
                widths.append(image.width + x)
                heights.append(image.height + y)            
                inputs.append((image, x, y, 1.0, images.TOP_LEFT))
            
            response = images.composite(inputs, max(widths), max(heights))

        except IOError as err:
            self.response.headers['Content-Type'] = 'text/html'
            self.response.out.write("Image error: {0}".format(err))
        except ValueError as err:
            self.response.headers['Content-Type'] = 'text/html'
            self.response.out.write("Request error: {0}".format(err) + " : " + request_json)
        else:
            self.response.headers['Content-Type'] = "image/png"
            self.response.out.write(response)

app = webapp2.WSGIApplication([
    ('/', MainHandler)
], debug=True)
