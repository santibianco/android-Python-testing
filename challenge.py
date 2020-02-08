from flask import Flask
from os import listdir
from flask_restful import reqparse, Api, Resource
from com.dtmilano.android.viewclient import ViewClient
from android_utils import uninstallApp, installApp, \
                          runInstalledApp, takeScreenshot
import time

app = Flask(__name__)
api = Api(app)


class List(Resource):
  def get(self):
    return {
      "url_to_run_apk": "localhost/run?name=<apk_name>",
      "available_apks": [apk for apk in listdir("apps")]
      }, 200


class Run(Resource):
  parser = reqparse.RequestParser()
  parser.add_argument("name", type=str, 
                      required=True,
                      help='apk name is required.')
  def get(self):
    return_dict = {}
    apk = self.parser.parse_args()['name']
    app_path = "apps/" + apk
    return_dict['apk_used'] = app_path
    device, serialno = ViewClient.connectToDeviceOrExit(verbose=True)
    uninstallApp(app_path, device, serialno)
    install_error = installApp(app_path, device, serialno)
    running_error = runInstalledApp(app_path, device, serialno)
    time.sleep(5)
    screenshot_name = apk+"_"+str(time.time())
    screenshot_error = takeScreenshot(device, screenshot_name)
    if(not screenshot_error):
      return_dict['screenshot_status'] = "Screenshot taken and saved as " + screenshot_name
    else:
      return_dict['screenshot_status'] = "Error while taking screenshot"
    return_dict['installation_status'] = "Success" if not install_error else "Error"
    return_dict['running_status'] = "Success" if not running_error else "Error"
    return return_dict, 200


# Setup the Api resource routing here
RESOURCES = [
  (List, '/'),
  (Run, '/run'),
]


for resource, endpoint in RESOURCES:
  api.add_resource(resource, endpoint)


if __name__ == '__main__':
  app.run(host="127.0.0.1", port=8000)
