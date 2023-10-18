from prism_ai.api_resources.api_resource import APIResource

class TextKnowledge(APIResource):

    '''
    Knowledge Object to be created from a text
    '''

    @classmethod
    def create(
        cls,
        **params,
    ):
            
        '''
        Create a new Knowledge Object from text
        '''

        name = params.pop("name", None)
        kb_id = params.pop("knowledge_base_id", None)
        text = params.pop("text", None)

        if None in [name, kb_id, text]:
            
            cls._no_params_message(
                
                endpoint="TextKnowledge",
                req_pars=[
                    "name",
                    "knowledge_base_id",
                    "text",
                ],
            )
            return None
        
        else: 
            return cls._post(
                endpoint_url=f"users/knowledge_base/{kb_id}/knowledge_from_text/",
                name=name,
                text=text,
                **params,
            )
