import sys
sys.path.append('../')
from processingNetwork.ProcessingNetwork import ProcessingNetwork
from processingNetwork.ProcessingNode import ProcessingNode

class DataLake(ProcessingNode):
    def do_input(self,feature,settings):
        ''' 
            *** Do any standard data lake prep here that should be global across all queries!
        '''
        assert 'qtype' in feature and not feature['qtype'] == None
        if feature['qtype'] == 'do_insert':
            ''' 
             ** Do any standard insert prep here that should be global across all insert queries!
            '''
            assert 'key' in feature and not feature['key'] == None #Standard unique key value to insert with 
            assert 'meta' in feature and not  feature['meta'] == None #Standard searchable meta value in json
            assert 'data' in feature and not  feature['data'] == None #Standard data value in any type
            # Note to developers: These asserts ensure no matter what, data lakes always have keys, meta and data values across all service providers.
            # This is good, because as the data pipelines grow, they will have a standard cross platform nomenclature by virtue of the fact tha they are
            # 'DataLakes'.  It would be ill advised to edit these fields past Phase 1 of the project, as plugins and other systems will grow to expect these fields.
            for k in feature:
                assert k in ['key','meta','data','qtype']
            return self.do_insert(feature,settings)
        
        if feature['qtype'] == 'do_find':
            ''' 
             ** Do any standard insert prep here that should be global across all insert queries!
            '''
            f = feature.copy()
            del(f['qtype'])
            return self.do_find(f,settings)
        
        if feature['qtype'] == 'do_delete':
            ''' 
             ** Do any standard insert prep here that should be global across all insert queries!
            '''
            f = feature.copy()
            del(f['qtype'])
            return self.do_find(f,settings)
        raise Exception ("the qtype supplied is not understood by the Generic data lake!")