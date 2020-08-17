import sys
sys.path.append('../')
from processingNetwork.ProcessingNetwork import ProcessingNetwork
from processingNetwork.ProcessingNode import ProcessingNode
from  findclass.findclass import findclass
import json

class Request(ProcessingNode):
    '''
    A request is a mapping function that transforms a data request into resulting json data. It considers access permissions, and other issues pertaning to HTTP/HTTPS encoding. Queries supported:
    1) DataLake Queries - Get and dump data into a data lake
    2) Model Queries - 
    3) System Instrctions - Deploy, and access any hard coded queries
    3) Task Queries - Trigger and list scheduled tasks
    
    TODO: Add in a user management system.
    
    '''
    def get_json(self,obj):
        return json.loads(
        json.dumps(obj, default=lambda o: getattr(o, '__dict__', str(o)))
      )
    
    def get_registry(self):
        '''
            The registry maps functions from within different modules into the request system. This allows the kinds of requests to be augmented. Note that the registry is all text. This means that it can be stored in json, configured as version, will always be human readable, and can even be eventually be admistered within a database. 
        '''
        '''
        datalake_settings = {"GOOGLE_APPLICATION_CREDENTIALS":"creds.json", 
                            "GOOGLE_PROJECT_ID":'mwdatapipelineex',
                             "data_lake_id":'row',           
                             }
        
        registry = {
                'datalake_insert':{
                                'class':'MwDataLake', 
                                'query_id':'datalake_insert',
                                'method':'do_input', 
                                'arguments':{'qtype':'do_insert'},
                                'settings':datalake_settings
                                },
                'datalake_find':{
                                'class':'MwDataLake', 
                                'query_id':'datalake_find',
                                'method':'do_input', 
                                'arguments':{'qtype':'do_find'},
                                'settings':datalake_settings
                                }
                   }'''
        
        
        return {}
    
    def get_api_keys(self,request):
        '''
            List of allowed keys. This kind of system can be extended with permission levels and other ideas for the future. At a basic level certain keys should be manually entered. This basic level prevents most malicious access. Of course, these API keys can reside in a container or some special location, and could be looked up dynamically.
        
        '''
        return {}
    
    def access_log(self,feature,user):
        '''
        If needed, do something with the requested query. By default, we do nothing.
        '''
        pass
    
    def pipeline_globals(self):
        # MUST BE INCLUDED IN CHILD
        raise Exception("YOU MUST CHILD CLASS AND USE THIS METHOD")
        return globals()
    
    def do_input(self,feature,settings):
        '''
            Generic Query method that enforces basic permissions and structure around function look up. Can be extended in the future to generalize and enforce various API request standards across organizations.
        '''
        # We assert some basic requirements of a query, and then prepare a message for passing into the pipeline. After we convert the request to json, and if anything goes wrong we wrap up the error and send back a traceback. (That way a remote developer can understand what the heck is going on)
        # TODO IDEAS:
        # 1. you likely want the ability to trace queries, code profile queries, and have that return from an API
        try:
            
            allowed_keys = self.get_api_keys(feature)
            assert 'api_key' in feature and feature['api_key'] in allowed_keys
            assert 'query_id' in feature and type(feature['query_id']) == str
            assert 'query' in feature and type(feature['query']) == dict

            queries = self.get_registry()
            assert feature['query_id'] in queries.keys()
            
            self.access_log(feature,allowed_keys [feature['api_key'] ])
            
            ## Dynamic class load and invocation
            query_request = feature['query'].copy()
            query_def = queries[feature['query_id']].copy()
            query = query_def['arguments']
            query.update(query_request)
            #print("!!!!",query)
            qd = query_def 
            settings_in = qd['settings']
            
            ## Dynamic class load and invocation
            qtype = findclass(qd['class'],context=self.pipeline_globals())
            instance =qtype()
            func = getattr(instance,qd['method'],None)
            dat = self.get_json(func(query,settings_in))
            assert len(str(dat)) > 0
            return dat
        except:
            import traceback as tb
            return {'error':tb.format_exc()}   
        