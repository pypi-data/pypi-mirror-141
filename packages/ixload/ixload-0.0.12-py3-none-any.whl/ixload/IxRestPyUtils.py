try:
    import requests
except:
    print("The 'requests' module could not be imported. Please make sure the 'requests' module is installed in your Python build.")
    exit(1)
try:
	#python 2.7
	from urlparse import urljoin
except:
	#python 3.5
	import urllib
	from urllib.parse import urljoin
import json, re, time, os, copy
from threading import RLock
from future.utils import iteritems
try:
    requests.packages.urllib3.disable_warnings()
except Exception:
    pass

kIp             = "localhost"
kPort           = 8443
kApiVersion     = "v0"
kHttpRedirect   = False
kConnection     = None

kActionStateFinished = 'finished'
kActionStatusSuccessful = 'Successful'
kActionStateSuccess = 'SUCCESS'
kActionStateError = 'EXCEPTION'
kActionStatusError = 'Error'
kTestStateUnconfigured = 'Unconfigured'

kOperationTimeoutParameter = "operationTimeout"

def setEnvironment(ip=None, port=None, apiVersion=None, httpRedirect=False):
    global kIp
    global kPort
    global kApiVersion
    global kHttpRedirect

    if ip != None:
        kIp = ip
    if port != None:
        kPort = port
    if apiVersion != None:
        kApiVersion = apiVersion
    if httpRedirect != None:
        kHttpRedirect = httpRedirect

def getConnection():
    global kConnection
    if kConnection is None:
        kConnection = Connection.getConnection(kIp, kPort, kHttpRedirect, kApiVersion)

    return kConnection

def stripApiAndVersionFromURL(url):
    # remove the slash (if any) at the beginning of the url
    if url[0] == '/':
        url = url[1:]
    urlElements = url.split('/')
    if 'api' in url:
        # strip the api/v0 part of the url
        urlElements = urlElements[2:]

    return '/'.join(urlElements)

def log(message):
    currentTime = time.strftime("%H:%M:%S")
    print("%s -> %s" % (currentTime, message))


class Connection(object):
    '''
        Class that executes the HTTP requests to the application instance.
        It handles creating the HTTP session and executing HTTP methods.
    '''
    kHeaderContentType = "content-type"
    kContentJson = "application/json"
    kApiKeyHeader = 'X-Api-Key'
    kApiKey = ''
    kDefaultErrorCodes = [400, 404, 500]

    @staticmethod
    def getConnection(server, port, httpRedirect=False, version="v0"):
        transportType = 'https' if not httpRedirect else 'http'
        connectionUrl = "%s://%s:%s/" % (transportType, server, port)
        conn = Connection(connectionUrl, version, httpRedirect)
        return conn

    def __init__(self, siteUrl, apiVersion, httpRedirect=False):
        '''
            Args:
            - siteUrl is the actual url to which the Connection instance will be made.
            - apiVersion is the actual version of the REST API that the Connection instance will use.

            The HTTP session will be created when the first http request is made.
        '''

        self.httpSession = None
        self.httpRedirect = httpRedirect
        self.poolManager = None
        self.poolManagerLock = RLock()
        #final url for the connection will have the format: "http://IP:PORT/api/versionNo"
        self.url = Connection.urljoin(siteUrl, "api")
        self.url = Connection.urljoin(self.url, apiVersion)

    @staticmethod
    def setApiKey(apiKey):
        Connection.kApiKey = apiKey

    def _getHttpSession(self):
        '''
            This is a lazy initializer for the HTTP session.
            It does not need to be active until it is required.
        '''
        if self.httpSession is None:
            self.httpSession = requests.Session()
            if not self.httpRedirect:
                from requests.adapters import HTTPAdapter
                try:
                    from requests.packages.urllib3.poolmanager import PoolManager
                    from requests.packages.urllib3.util.retry import Retry
                except ImportError:
                    try:
                        # This import is for older versions of requests
                        from urllib3.poolmanager import PoolManager
                        from urllib3.util.retry import Retry
                    except Exception:
                        raise Exception('Failed to import PoolManager from the requests module')
                import ssl
                retry = Retry(connect=5, backoff_factor=0.5)
                httpAdapter = HTTPAdapter(max_retries=retry)

                try:
                    httpAdapter.poolmanager = PoolManager(ssl_version=ssl.PROTOCOL_TLSv1_2)
                    self.poolManager = httpAdapter.poolmanager
                except Exception:
                    raise Exception("Failed to create PoolManager for TLS version 1.2. Please make sure you are using a Python executable that has support for TLS 1.2")
                self.httpSession.mount('https://', httpAdapter)
        return self.httpSession

    @classmethod
    def urljoin(cls, base, end):
        '''
            Join two URLs. If the second URL is absolute, the base is ignored.

            Use this instead of urlparse.urljoin directly so that we can customize its behavior if necessary.
            Currently differs in that it
                1. appends a / to base if not present.
                2. casts end to a str as a convenience
        '''
        if base and not base.endswith("/"):
            base = base + "/"
        return urljoin(base, str(end))

    def httpRequest(self, method, url="", data="", params={}, headers={}, stream=False, timeout=(80,80)):
        '''
            Args:
            - Method (mandatory) represents the HTTP method that will be executed.
            - url (optional) is the url that will be appended to the application url.
            - data (optional) is the data that needs to be sent along with the HTTP method as the JSON payload
            - params (optional) the payload python dict not necessary if data is used.
            - headers (optional) these are the HTTP headers that will be sent along with the request. If left blank will use default
            - stream (optional) specifies if the data to/from the client should be streamed
            - timeout (optional) specifies the read and connect timeout. If you wish to have different values for read and connect
            then specify timeout as a tuple e.g. timeout=(80, 100)

            Method for making a HTTP request. The method type (GET, POST, PATCH, DELETE) will be sent as a parameter.
            Along with the url and request data. The HTTP response is returned
        '''
        headers[Connection.kHeaderContentType] = Connection.kContentJson

        if Connection.kApiKey != '':
            headers[Connection.kApiKeyHeader] = Connection.kApiKey

        if not stream:
            if type(data) == dict:
                data = json.dumps(data)
            data = str(data)
        absUrl = Connection.urljoin(self.url, url)

        self.poolManagerLock.acquire()
        result = None
        try:
            if self.poolManager != None:
                self.poolManager.clear()
            result = self._getHttpSession().request(method, absUrl, data=data, params=params, headers=headers, verify=False, timeout=timeout, stream=stream)
        finally:
            self.poolManagerLock.release()
        return result

    def httpGet(self, url="", data="", params={}, headers={}, errorCodes = [], wrapResult=True):
        '''
            Method for calling HTTP GET. This will return a WebObject that has the fields returned
            in JSON format by the GET operation.
        '''
        reply = self.httpRequest("GET", url, data, params, headers)

        if errorCodes == []:
            errorCodes = Connection.kDefaultErrorCodes
        if reply.status_code in errorCodes:
            raise Exception("Error on executing GET request on url %s: %s" % (url, reply.text))

        if wrapResult:
            return _WebObject(reply.json(), url)
        else:
            return reply.json()

    def httpPost(self, url="", data="", params={}, headers={}):
        '''
            Method for calling HTTP POST. Will return the HTTP reply.
        '''
        return self.httpRequest("POST", url, data, params, headers)

    def httpPatch(self, url="", data="", params={}, headers={}):
        '''
            Method for calling HTTP PATCH. Will return the HTTP reply.
        '''
        return self.httpRequest("PATCH", url, data, params, headers)

    def httpDelete(self, url="", data="", params={}, headers={}):
        '''
            Method for calling HTTP DELETE. Will return the HTTP reply.
        '''
        return self.httpRequest("DELETE", url, data, params, headers)

    def refreshData(self, object):
        newObj = self.httpGet(object.getUrl())
        object.copyData(newObj)


def _WebObject(value, _url_ = None):
    '''
        Method used for creating a wrapper object corresponding to the JSON string received on a GET request.
    '''
    if isinstance(value, dict):
        value['_url_'] = _url_
        if _url_ and bool(re.search(r'[\w.-]+/ixload/stats/[\w().-]+/values', _url_)):
            #    pass#'values' resources only have name and value of the stats, don't need the url
            result = StatsWebObject(**value)
        else:
            result = WebObject(**value)
    elif isinstance(value, list):
        result = WebList(entries=value, _url_=_url_)
    else:
        result = value
    return result


class WebList(list):
    '''
        Using this class a JSON list will be transformed in a list of WebObject instances.
    '''

    def __init__(self, entries=[], _url_=None):
        '''
            Create a WebList from a list of items that are processed by the _WebObject function
        '''
        self._url_ = _url_

        url = _url_
        filterSyntax = "?filter=" #  we need to remove the query param syntax from all chindren of the list.
        if url and filterSyntax in url:
            url = url.split(filterSyntax)[0] # get everything on the left of the filter, removing the query param

        for item in entries:
            itemUrl = None
            if "objectID" in item:
                itemUrl = "%s/%s" % (url, item["objectID"])

            self.append(_WebObject(item, itemUrl))

    def copyData(self, newObj):
        self[:] = []

        for item in newObj:
            self.append(item)

    def isContainerObject(self):
        return True

    def getUrl(self):
        return self._url_

    def clear(self):
        connection = getConnection()
        data = json.dumps({})
        reply = connection.httpDelete(url=self.getUrl(), data=data)

        if not reply.ok:
            raise Exception(reply.text)

    def appendItem(self, **kwargs):
        data = json.dumps(kwargs)
        connection = getConnection()
        reply = connection.httpPost(url=self.getUrl(), data=data)

        if not reply.ok:
            raise Exception(reply.text)

        try:
            newObjPath = reply.headers['location']
        except:
            raise Exception("Location header is not present. Please check if the action was created successfully.")

        newObjID = newObjPath.split('/')[-1]
        newObjURL = "%s/%s" % (self.getUrl(), newObjID)

        listElement = connection.httpGet(newObjURL)
        self.append(listElement)

        return listElement

    def __setattr__(self, property, value):
        if not property in ["_url_", "jsonOptions", "operations"]:
            if len(self) > 0:
                item = self[0]
                for prop in item.jsonOptions:
                    if property.lower() == prop.lower():
                        connection = getConnection()

                        data = json.dumps({property:value})
                        reply = connection.httpPatch(url=self.getUrl(), data=data)
                        if not reply.ok:
                            raise Exception(reply.text)
                        return

        super(WebList, self).__setattr__(property, value)


class WebOperation(object):
    '''
       Using the WebOperation class to model an operation on an object.
    '''

    def __init__(self, parent, url, operationName, parameters):
        self.url = url
        self.operationName = operationName
        self.parameters = parameters
        self.parent = parent

    def waitForActionToFinish(self, replyObj, actionUrl, timeout=None):
        actionStatusSuccess = {"v0": lambda x: x.state == kActionStateFinished and x.status == kActionStatusSuccessful,
                               "v1": lambda x: x.state == kActionStateSuccess}
        actionStatusError = {"v0": lambda x: x.status == kActionStatusError,
                             "v1": lambda x: x.state == kActionStateError}
        messageError = {"v0": lambda x: x.error,
                        "v1": lambda x: x.message}

        connection = getConnection()
        apiVersion = kApiVersion

        initialTime = int(time.time())
        sleepPeriod = 1 #sleep for 1 second

        actionResultURL = replyObj.headers.get('location')
        if actionResultURL:
            actionResultURL = stripApiAndVersionFromURL(actionResultURL)
            actionFinished = False
            while not actionFinished:
                actionStatusObj = connection.httpGet(actionResultURL)
                if actionStatusSuccess[apiVersion](actionStatusObj):
                    actionFinished = True

                elif actionStatusError[apiVersion](actionStatusObj):
                    errorMsg = "Error while executing action '%s'." % actionResultURL
                    errorMsg += messageError[apiVersion](actionStatusObj)
                    raise Exception(errorMsg)
                else:
                    if timeout is not None and int(time.time())-initialTime >= timeout:
                        raise Exception("Operation %s exceeded timeout of %s seconds." % (actionResultURL, timeout))

                    time.sleep(sleepPeriod)
                    
    def __call__(self, **kwargs):
        log("Starting '%s' operation..." % (self.operationName))

        timeout=None
        if kOperationTimeoutParameter in kwargs:
            timeout = kwargs[kOperationTimeoutParameter]
            del kwargs[kOperationTimeoutParameter]

        connection = getConnection()
        data = json.dumps(kwargs)
        reply = connection.httpPost(url=self.url, data=data)
        if not reply.ok:
            raise Exception(reply.text)

        ## if no timeout was provided, the operation will not have a timeout period. 
        self.waitForActionToFinish(reply, self.url, timeout=timeout)

        # refreshing the data of the parent. for loading a config for example,
        # the data model can change after performing the operation
        self.parent.refreshData()

        log("%s operation completed." % (self.operationName))

        return reply


class WebObjectPromise(object):
    def __init__(self, url):
        self.url = url


class WebObject(object):
    '''
        A WebObject instance will have its fields set to correspond to the JSON format received on a GET request.
        for example: a response in the format: {"caption": "http"} will return an object that has obj.caption="http"
    '''

    def __init__(self, **entries):
        '''
            Create a WebObject instance by providing a dict having a property - value structure.
        '''
        connection = getConnection()
        self.jsonOptions = {}
        self.operations = {}
        for key, value in iteritems(entries):
            key = key.lower()# -> keep all urls case insensitive
            if key == "links":
                for link in value:
                    optionName = None
                    if kApiVersion == "v1":
                        if link["rel"] != "child":
                            continue
                        optionName = link["href"].split("/")[-1]
                    elif kApiVersion == "v0":
                        optionName = link["rel"]

                    if optionName == "docs":
                        continue

                    optionUrl = link["href"]
                    value = WebObjectPromise(optionUrl)
                    self.jsonOptions[optionName] = value

            else:
                webObj = _WebObject(value)
                self.jsonOptions[key] = webObj
                self.__dict__[key] = webObj

        if self.getUrl() and not "/operations/" in self.getUrl().lower():
            #if the web object that is being populated is an operation status url
            #such as /sessions/2/operations/start/2
            #no need to check operations for that url
            self.populateOperations()

    def getUrl(self):
        return self._url_

    def populateOperations(self):
        connection = getConnection()
        url = "%s/%s" % (self.getUrl(), "operations")
        operations = connection.httpGet(url, wrapResult=False)
        for (operationName, parameters) in iteritems(operations):
            operationName = operationName.lower()
            if operationName == "links":
                continue
            else:
                operationUrl = "%s/%s" % (url, operationName)
                operation = WebOperation(self, operationUrl, operationName, parameters)
                self.operations[operationName] = operation
                self.__dict__[operationName] = operation

    def copyData(self, newObj):
        self.jsonOptions = {}
        for key, obj in iteritems(newObj.jsonOptions):
            key = key.lower()# -> everything case insensitive
            self.jsonOptions[key] = obj
            if not isinstance(obj, WebObjectPromise):
                self.__dict__[key] = obj

    def isContainerObject(self):
        return False

    def getOptions(self):
        return self.jsonOptions

    def __str__(self):
        try:
            return self.restObjectType
        except:
            return super(WebObject, self).__str__()

    def __getattr__(self, property):
        #URL can be retrieved immediately, no handling needed
        if property in ["_url_", "jsonOptions", "operations"]:
            return self.__dict__[property]

        property = property.lower()# -> keep everything case insensitive
        self.refreshData()

        try:
            attr = self.__getattribute__(property)
        except Exception as e:
            attr = self.jsonOptions.get(property)
            if isinstance(attr, WebObjectPromise):
                connection = getConnection()
                attr = connection.httpGet(attr.url)

        return attr

    def __setattr__(self, property, value):
        if not property in ["_url_", "jsonOptions", "operations"]:
            log("Setting value %s on property %s" % (value, property))
            for prop in self.jsonOptions:
                if property.lower() == prop.lower():
                    connection = getConnection()

                    data = json.dumps({property:value})
                    reply = connection.httpPatch(url=self.getUrl(), data=data)
                    if not reply.ok:
                        raise Exception(reply.text)
                    return

        super(WebObject, self).__setattr__(property, value)

    ### API Available on WebObject that allows setting multiple parameters at once - will only make 1 PATCH request.
    def setOptions(self, **kwargs):
        data = {}
        for propTup in kwargs.items():
            property = propTup[0]
            value = propTup[1]
            if not property in ["_url_", "jsonOptions", "operations"]:
                log("Setting value %s on property %s" % (value, property))
                for prop in self.jsonOptions:
                    if property.lower() == prop.lower():
                        data[property] = value

        if len(data) > 0:
            connection = getConnection()

            data = json.dumps(data)
            reply = connection.httpPatch(url=self.getUrl(), data=data)
            if not reply.ok:
                raise Exception(reply.text)
            return

    def refreshData(self):
        connection = getConnection()
        connection.refreshData(self)


class StatsWebObject(object):
    '''
        Using StatsWebObject to encompass a stat source.
    '''
    def __init__(self, **entries):
        self.jsonOptions = entries
        if "_url_" in self.jsonOptions:
            if len(self.jsonOptions.keys()) == 1:
                return
            else:
                self.jsonOptions.pop("_url_")
        import collections
        self.forStat = {}

        self.jsonOptions = collections.OrderedDict(sorted(self.jsonOptions.items(), key=lambda t: int(t[0])))
        for key in self.jsonOptions:
            for el in self.jsonOptions[key].keys():
                if not el in self.forStat:
                    self.forStat[el] = collections.OrderedDict()
                self.forStat[el][key] = self.jsonOptions[key][el]

    def __str__(self):
        return str(self.jsonOptions)

    def keys(self):
        return self.jsonOptions.keys()

    def getStatNames(self):
        return self.forStat.keys()

    def __getitem__(self, key):
        return self.jsonOptions[key]


def closeAllSessions():
    sessions = getSessions()
    connection = getConnection()
    data = json.dumps({})
    reply = connection.httpDelete(url=sessions.getUrl(), data=data)

    if not reply.ok:
        raise Exception(reply.text)

def closeSession(session):
    connection = getConnection()
    data = json.dumps({})
    reply = connection.httpDelete(url=session.getUrl(), data=data)

    if not reply.ok:
        raise Exception(reply.text)

def getSessions():
    connection = getConnection()
    sessions = connection.httpGet("sessions")
    return sessions

def createSession(version=None):
    sessions = getSessions()
    if version is None:
        raise Exception("We don't support running without a version yet. Please send version")

    parameters = {"ixLoadVersion":version}
    if kApiVersion == "v1":
        parameters = {"applicationVersion":version}

    session = sessions.appendItem(**parameters)
    return session

def uploadFile(fileName, uploadPath, overwrite=True, timeout=80):
    '''
        This method is used to upload a file to the specified location.

        Args:
        - fileName is the name of the file to be uploaded (on the local machine)
        - uploadPath is the path where the file will be uploaded
        - overwrite is used to select if the existing file should be overwritten
        - timeout is the operation timeout
    '''
    connection = getConnection()
    url = Connection.urljoin(connection.url, "resources")
    uploadPath = os.path.join(getSharedFolder(), uploadPath)
    headers = {'Content-Type': 'multipart/form-data'}
    params = {"overwrite": overwrite, "uploadPath": uploadPath}
    log('Uploading to %s...' % (uploadPath))
    try:
        with open(fileName, 'rb') as f:
            resp = connection.httpRequest('POST', url, data=f, params=params, headers=headers, stream=True, timeout=timeout)
            if resp.ok is not True:
                raise Exception('POST operation failed with %s' %resp.text)
    except requests.exceptions.ConnectionError as e:
        raise Exception(
            'Upload file failed. Received connection error. One common cause for this error is the size of the file to be uploaded.'
            ' The web server sets a limit of 1GB for the uploaded file size. Received the following error: %s' % str(e)
        )
    except IOError as e:
        raise Exception('Upload file failed. Received IO error: %s' % str(e))
    except Exception as e:
        raise Exception('Upload file failed. Received the following error:\n %s' % str(e))
    else:
        log('Upload file finished.')
        log('Response status code %s' % (resp.status_code))
        log('Response text %s' % (resp.text))

def downloadResource(downloadFolder, localPath, zipName=None, timeout=80):
    '''
        This method is used to download an entire folder as an archive or any type of file without changing it's format.

        Args:
        - downloadFolder is the folder were the archive/file will be saved
        - localPath is the local path on the machine that holds the IxLoad instance
        - zipName is the name that archive will take, this parameter is mandatory only for folders, if you want to download a file this parameter is not used.
    '''
    connection = getConnection()
    url = Connection.urljoin(connection.url, "downloadResource")
    downloadFolder = downloadFolder.replace("\\\\", "\\")
    localPath = localPath.replace("\\", "/")
    parameters = { "localPath": localPath, "zipName": zipName }

    downloadResourceReply = connection.httpRequest('GET', url, params=parameters, stream=True, timeout=timeout)
    if not downloadResourceReply.ok:
        raise Exception("Error on executing GET request on url %s: %s" % (url, downloadResourceReply.text))

    if not zipName:
        zipName = localPath.split("/")[-1]
    elif zipName.split(".")[-1] != "zip":
        zipName  = zipName + ".zip"
    downloadFile = '/'.join([downloadFolder, zipName])
    log('Downloading resource to %s...' % (downloadFile))
    try:
        with open(downloadFile, 'wb') as fileHandle:
            for chunk in downloadResourceReply.iter_content(chunk_size=1024):
                fileHandle.write(chunk)
    except IOError as e:
        raise Exception('Download resource failed. Could not open or create file, please check path and/or permissions. Received IO error: %s' % str(e))
    except Exception as e:
        raise Exception('Download resource failed. Received the following error:\n %s' % str(e))
    else:
        log('Download resource finished.')

def retrieveCaptureFileForPort(session, communityPortIdTuple, captureFile):
    '''
        This method is used to retrieve the capture file for the port specified.

        Args:
        - communityPortIdTuple is the (communityObjectId, portId) tuple; eg: (0, '1.5.1')
        - captureFile is the save path for the capture file

        Error Codes:
        - 0 No error
        - 1 Invalid portId
        - 2 Cannot create/open captureFile
    '''
    communityObjectId, portId = communityPortIdTuple

    communityObject = None
    portObject = None
    communityList = session.ixload.test.activeTest.communityList
    for community in communityList:
        if community.objectId == communityObjectId:
            communityObject = community
            portList = community.network.portList
            for port in portList:
                if port.id == portId:
                    portObject = port
                    break
            break

    if not communityObject:
        log('Error: Community with id %s not found.' % (communityObjectId))
        return 1
    if not portObject:
        log('Error: Port with id %s not found.' % (portId))
        return 1

    connection = getConnection()
    captureFile = captureFile.replace("\\\\", "\\")
    captureUrl = '/'.join([portObject.getUrl(), 'restCaptureFile'])
    capturePayload = connection.httpRequest('GET', captureUrl, stream=True)

    log('Saving capture file %s...' % (captureFile))
    try:
        with open(captureFile, 'wb') as fileHandle:
            for chunk in capturePayload.iter_content(chunk_size=1024):
                fileHandle.write(chunk)
    except IOError as e:
        log('Error: Saving capture failed. Could not open or create file, please check path and/or permissions. Received IO error: %s' % (str(e)))
        return 2
    except Exception as e:
        log('Error: Saving capture failed. Received the following error:\n %s' % (str(e)))
        return 2
    else:
        log('Saving capture finished.')

    return 0

def retrieveCaptureFileForAssignedPorts(session, captureFolder):
    '''
        This method is used to retrieve capture files from a rest session which had portCapture set to True.

        Args:
        - captureFolder is the folder where the capture file will be saved
    '''
    communityList = session.ixload.test.activeTest.communityList
    captureFolder = captureFolder.replace("\\\\", "\\")
    connection = getConnection()

    for community in communityList:
        portList = community.network.portList
        for port in portList:
            captureName = "Capture_%s_%s.cap" % (community.objectID, port.id)
            captureFile = '/'.join([captureFolder, captureName])
            captureUrl = '/'.join([port.getUrl(), 'restCaptureFile'])
            capturePayload = connection.httpRequest('GET', captureUrl, stream=True)
            log('Saving capture file %s...' % (captureFile))
            try:
                with open(captureFile, 'wb') as fileHandle:
                    for chunk in capturePayload.iter_content(chunk_size=1024):
                        fileHandle.write(chunk)
            except IOError as e:
                raise Exception('Saving capture failed. Could not open or create file, please check path and/or permissions. Received IO error: %s' % str(e))
            except Exception as e:
                raise Exception('Saving capture failed. Received the following error:\n %s' % str(e))
            else:
                log('Saving capture finished.')


def enableAnalyzerOnPorts(portList):
    for port in portList:
        port.enableCapture = True

def addChassisList(session, chassisList):
    '''
        This method is used to add one or more chassis to the chassis list.

        Args:
        - chassisList is the list of chassis that will be added to the chassis chain.
    '''

    for chassisName in chassisList:
        chassis = session.ixload.chassischain.chassisList.appendItem(chassisName)
        chassis.refreshConnection()

def assignPorts(session, portListPerCommunity):
    '''
        This method is used to assign ports from a connected chassis to the required NetTraffics.

        Args:
        - portListPerCommunity is the dictionary mapping NetTraffics to ports (format -> { community name : [ port list ] })
    '''

    communityList = session.ixload.test.activeTest.communityList
    communityNameList = [community.name for community in communityList]

    for communityName in portListPerCommunity:
        if communityName not in communityNameList:
            errorMsg = "Error while executing assignPorts operation. Invalid NetTraffic name: %s. This NetTraffic is not defined in the loaded rxf." % communityName
            raise Exception(errorMsg)

    for community in communityList:
        if portListPerCommunity.get(community.name):
            portListForCommunity = portListPerCommunity.get(community.name)
            for portTuple in portListForCommunity:
                chassisId, cardId, portId = portTuple
                serverPortList.appendItem(chassisId, cardId, portId)
        else:
            errorMsg = "Error while executing assignPorts operation. For community: %s you dont't have ports assigned." % community.name
            raise Exception(errorMsg)

def getItemByName(itemList, itemName):
    for item in itemList:
        if item.name == itemName:
            return item

def getActivityByName(session, communityName, activityName):
    communityList = session.ixload.test.activeTest.communityList
    community = getItemByName(communityList, communityName)
    if community is None:
        raise Exception('Community %s cannot be found.' % communityName)

    activity = getItemByName(communityList.activityList, activityName)
    if activity is None:
        raise Exception('Community %s does not have an activity named %s.' % (communityName, activityName))
    return activity

def addActivities(session, activityListPerCommunity):
    communityList = session.ixload.test.activeTest.communityList
    for communityName, activityList in iteritems(activityListPerCommunity):
        community = getItemByName(communityList, communityName)

        if community is None:
            raise Exception('Community %s cannot be found.' % communityName)

        for activityType in activityList:
            community.activityList.protocolAndType = activityType

def getSharedFolder():
    connection = getConnection()
    resourceUrl = "resources"
    resourceObj = connection.httpGet(resourceUrl)
    return resourceObj.sharedLocation

def collectGatewayDiagnostics(zipFilePath):
    connection = getConnection()
    collectGatewayDiagnosticsUrl = "logs/operations/collectDiagnostics"
    data = {"zipFileLocation": zipFilePath}
    reply = connection.httpPost(collectGatewayDiagnosticsUrl, data)
    if not reply.ok:
        raise Exception(reply.text)

def deleteAllLogs():
    connection = getConnection()
    deleteAllLogsUrl = "logs/operations/deleteAllLogs"
    data = {}
    reply = connection.httpPost(deleteAllLogsUrl, data)
    if not reply.ok:
        raise Exception(reply.text)
        
def deleteAllGatewayLogs():
    connection = getConnection()
    deleteIxLoadGatewayLogsUrl = "logs/operations/deleteIxLoadGatewayLogs"
    data = {}
    reply = connection.httpPost(deleteIxLoadGatewayLogsUrl, data)
    if not reply.ok:
        raise Exception(reply.text)

def getLatestTimestampValuesForStatList(statSourceObject, statList):
    '''
        This method is used to get the latest timestamp values for the statistics 
        from the stat list and from the stat source specified.

        Args:
        - statSourceObject is the stat source
        - statList is the list of statistics of interest
    '''
    timestampList = copy.copy(statSourceObject.values)
    sortedTimestamps = sorted([int(key) for key in timestampList.keys() if key != '_url_'])
    if len(sortedTimestamps) > 0:
        latestTimestamp = str(sortedTimestamps[-1])
        timestampObject = timestampList[latestTimestamp]
        timestampValues = {}
        for stat in statList:
            if stat in timestampObject:
                timestampValues[stat] = timestampObject[stat] 
            else:
                log("Stat '%s' not found on this stat source" % (stat, ))
        
        return {latestTimestamp: timestampValues}
    else:
        return {}

def getLatestTimestampValues(statSourceObject):
    '''
        This method is used to get the latest timestamp values for the statistics from the stat source specified.

        Args:
        - statSourceObject is the stat source
    '''
    timestampList = copy.copy(statSourceObject.values)
    sortedTimestamps = sorted([int(key) for key in timestampList.keys() if key != '_url_'])
    if len(sortedTimestamps) > 0:
        latestTimestamp = str(sortedTimestamps[-1])
        timestampValues = timestampList[latestTimestamp]
        return {latestTimestamp: timestampValues}
    else:
        return {}