import subprocess
from com.dtmilano.android.viewclient import ViewClient
import time

def installApp(path, device, serialno):
    viewClientObject = ViewClient(device, serialno)
    return subprocess.check_call([viewClientObject.adb,
                                   "install", "-r",
                                   path], shell=False)


def getPackageFromApk(path):
    package = subprocess.check_output("aapt dump badging " +
                                      path + "| grep package",
                                      shell=True)
    package = package.split()[1]
    package = package.replace("name=", "").replace("'", "")
    return package


def getLaunchableActivityFromApk(path):
    activity = subprocess.check_output("aapt dump badging " +
                                       path + "| grep launchable-activity",
                                       shell=True)
    activity = activity.split()[1]
    activity = activity.replace("name=", "").replace("'", "")
    return activity


def appIsInstalled(path, device, serialno):
    viewClientObject = ViewClient(device, serialno)
    package = getPackageFromApk(path)
    return len(subprocess.check_output([viewClientObject.adb,
                                       "shell", "pm", "list",
                                       "packages", package],
                                       shell=False)) > 0

def uninstallApp(path, device, serialno):
    if(appIsInstalled(path, device, serialno)):
        viewClientObject = ViewClient(device, serialno)
        package = getPackageFromApk(path)
        return subprocess.check_call([viewClientObject.adb,
                                     "uninstall",
                                      package], shell=False)
    else:
        return "App already uninstalled"


def takeScreenshot(device, filename): 
    try: 
        device.takeSnapshot(reconnect=True).save("screenshots/" + filename + '.png', 'PNG')
        return 0
    except: 
        return 1


def runInstalledApp(path, device, serialno):
    if(appIsInstalled(path, device, serialno)):
        viewClientObject = ViewClient(device, serialno)
        package = getPackageFromApk(path) 
        activity = getLaunchableActivityFromApk(path) 
        return subprocess.check_call([viewClientObject.adb,
                                      "shell", "am", "start",
                                      "-n", package+"/"+activity],
                                      shell=False)
    else: 
        return 1


"""
if __name__ == "__main__":
    app_path = "apps/speedtest.apk"
    device, serialno = ViewClient.connectToDeviceOrExit(verbose=True)
    uninstallApp(app_path, device, serialno)
    installApp(app_path, device, serialno)
    runInstalledApp(app_path, device, serialno)
    time.sleep(5)
    takeScreenshot(device, "first screenshot")
"""