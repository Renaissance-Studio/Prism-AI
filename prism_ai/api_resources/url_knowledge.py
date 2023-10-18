from prism_ai.api_resources.api_resource import APIResource

class UrlKnowledge(APIResource):

    '''
    Knowledge Object to be created from a url
    '''

    @classmethod
    def create(
        cls,
        **params,
    ):
            
        '''
        Create a new Knowledge Object from a url
        '''

        name = params.pop("name", None)
        kb_id = params.pop("knowledge_base_id", None)
        url = params.pop("url", None)

        if None in [name, kb_id, url]:
            
            cls._no_params_message(
                
                endpoint="UrlKnowledge",
                req_pars=[
                    "name",
                    "knowledge_base_id",
                    "url",
                ],
            )
            return None
        
        else: 
            return cls._post(
                endpoint_url=f"users/knowledge_base/{kb_id}/knowledge_from_url/",
                name=name,
                url=url,
                **params,
            )
