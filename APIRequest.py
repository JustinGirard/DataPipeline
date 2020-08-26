import sys
sys.path.append('../')
import importlib
import base64,json,pickle,urllib

class APIRequest():
    '''
    Processes a generic API request by looking for a registered System object, (mapped by directory name)
    '''
    def submit(feature,remote=None):
        if remote == None:
            import sys
            assert 'pipeline_id' in feature and not feature['pipeline_id'] == None 
            assert 'query_id' in feature and not feature['query_id'] == None
            sys.path.append('../'+feature['pipeline_id']+'/')
            pipeline_module = importlib.import_module(feature['pipeline_id']+".pipeline")
            importlib.reload(pipeline_module)

            System =  pipeline_module.System 
            pipeline_system = System()
            req_class = pipeline_system.get_request_class()
            req_instance =req_class() 
            result = req_instance.do_input(feature,{})
            return result
        else:
            assert 'pipeline_id' in feature and not feature['pipeline_id'] == None 
            assert 'query_id' in feature and not feature['query_id'] == None
            '''
            This is a remote request. We have to wrap up our post variable and unpack it on the other side
            '''
            import requests
            result = requests.post(remote, data = {'__packet':APIRequest.createPacket(feature)})
            try:
                return json.loads(result.text) 
            except:
                return result.text

    def submit_remote(request):
        '''
        This method should be invoked by a remote server. The server will get a request 
        (either though a websocket, a database, a buffer or some other method), 
        and will be supplied with a packet. 
        The remote side will unpack this request using extractPacket, and process
        the generic request.
        '''
        feature = APIRequest.extractPacket(request['__packet'])
        return json.dumps(APIRequest.submit(feature))
        
            
    def createPacket(obj):
        packet = base64.b64encode(pickle.dumps(obj))   
        try: #Support both the flask and non flask version
            packet = urllib.parse.quote(packet)     
        except:
            packet = urllib.quote(packet)  
        return packet

    def extractPacket(packet):
        try: #Support both the flask and non flask version
            packet = urllib.parse.unquote(packet)    
        except:
            packet = urllib.unquote(packet)    
        user_data_dev = base64.b64decode(packet)   
        data2 = pickle.loads(user_data_dev)
        return data2