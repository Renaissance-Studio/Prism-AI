from prism_ai.api_resources.api_resource import APIResource
from prism_ai.api_resources.url_knowledge import UrlKnowledge
from prism_ai.api_resources.text_knowledge import TextKnowledge
from prism_ai.api_resources.file_knowledge import FileKnowledge


class KnowledgeBase(APIResource):

    '''
    Knowledge Base Object to be created from a url
    '''


    @classmethod
    def add(
        cls, 
        **params,
    ):
        '''
        Create a new Knowledge Base Object 
        '''

        _id = params.pop("id", None)

        if None in [_id]:
            
            cls._no_params_message(
                
                endpoint="KnowledgeBase",
                req_pars=[
                    "id",
                ],
            )
            return None

        if "knowledges" in params:
            
            MULTI = True

            knowledges = params.pop("knowledges")

            if "types" in params: 
                types = params.pop("types")
            else:
                types = cls.infer_types(knowledges)

            if "names" in params: 
                names = params.pop("names")

            else: 
                names = ["Knowledge " + str(i) for i in range(len(knowledges))]

            for tp, k, nm in zip(types, knowledges, names):

                if tp == "url":
                    UrlKnowledge.create(
                        name=nm,
                        url=k,
                        knowledge_base_id=_id,
                    )
                elif tp == "text":
                    TextKnowledge.create(
                        name=nm,
                        text=k,
                        knowledge_base_id=_id,
                    )
                elif tp == "file":
                    FileKnowledge.create(
                        name=nm,
                        file=k,
                        knowledge_base_id=_id,
                    )
                else:
                    raise ValueError(f"Type {tp} not recognized.")

            return cls._get(
                endpoint_url=f"users/knowledge_base/{_id}/",
                # **params,
            )
        else:

            MULTI = False
            return 

    @classmethod
    def infer_types(
        cls,
        knowledges,
    ):
        '''
        Infer the types of the knowledges
        '''

        types = []

        for knowledge in knowledges:

            types.append("url")

        return types

    @classmethod
    def create(
        cls,
        **params,
    ):
            
        '''
        Create a new Knowledge Base Object 
        '''

        name = params.pop("name", None)

        if None in [name]:
            
            cls._no_params_message(
                
                endpoint="KnowledgeBase",
                req_pars=[
                    "name",
                ],
            )
            return None

        if "knowledges" in params:
            
            MULTI = True

            kb = cls._post(
                endpoint_url=f"users/knowledge_base/",
                name=name,
                **params,
            )
            print(kb.json)
            kb_id = int(kb.json['id'])

            knowledges = params.pop("knowledges")

            if "types" in params: 
                types = params.pop("types")
            else:
                types = cls.infer_types(knowledges)

            if "names" in params: 
                names = params.pop("names")

            else: 
                names = ["Knowledge " + str(i) for i in range(len(knowledges))]

            for tp, k, nm in zip(types, knowledges, names):

                if tp == "url":
                    UrlKnowledge.create(
                        name=nm,
                        url=k,
                        knowledge_base_id=kb_id,
                    )
                elif tp == "text":
                    TextKnowledge.create(
                        name=nm,
                        text=k,
                        knowledge_base_id=kb_id,
                    )
                elif tp == "file":
                    FileKnowledge.create(
                        name=nm,
                        file=k,
                        knowledge_base_id=kb_id,
                    )
                else:
                    raise ValueError(f"Type {tp} not recognized.")

            return cls._get(
                endpoint_url=f"users/knowledge_base/{kb_id}/",
                # **params,
            )
        else:

            MULTI = False
            return cls._post(
                endpoint_url=f"users/knowledge_base/",
                name=name,
                **params,
            )

