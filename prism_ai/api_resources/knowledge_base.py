from prism_ai.api_resources.api_resource import APIResource
from prism_ai.api_resources.knowledge import Knowledge
import pathlib
import os

supported_file_types = [
    "pdf",
    "doc",
    "docx",
    "txt",
    "md",
    "odt",
    "gz"
]

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
        Add knowledge to an existing knowledge base
        '''

        _id = params.pop("id", None)

        if None in [_id]:

            raise ValueError("Knowledge Base ID not provided.")

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
                    Knowledge.create(
                        method="url",
                        name=nm,
                        url=k,
                        knowledge_base_id=_id,
                    )
                elif tp == "text":
                    Knowledge.create(
                        method="text",
                        name=nm,
                        text=k,
                        knowledge_base_id=_id,
                    )
                elif tp == "file":
                    Knowledge.create(
                        method="path",
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
        
        elif "base_dir" in params:

            dir_path = pathlib.Path(params.pop("base_dir"))
            dir_list = list(dir_path.rglob('*'))
            file_list = []
            supported_file_list = []
            to_process = []

            for elt in dir_list:

                if elt.is_dir():
                    print(f"Omitting directory {elt} ... Not a file.")
                    continue
                else:
                    file_list.append(elt)

            print("\n\n")
            for elt in file_list:
                
                if str(elt).split(".")[-1] not in supported_file_types:
                    print(f"Omitting file {elt} ... Unsupported file type.")
                    continue
                else:
                    supported_file_list.append(elt)
            print("\n\n")
            for elt in supported_file_list:
                if os.path.getsize(elt) > 1024 * 1024 * 1024 * 4:
                    print(f"Omitting file {elt} ... File size exceeds 4GB.")
                    continue
                else:
                    to_process.append(elt)

            to_process_size = sum([os.path.getsize(file) for file in to_process])
            info_instance = cls._get(endpoint_url="basic_user_info/", quiet=True)
            user_info = info_instance.json

            if user_info["max_storage"] != None:
                if to_process_size / (1024 * 1024) > user_info["max_storage"]:
                    raise ValueError(f"Attempted to upload {to_process_size / (1024 * 1024)} MB of data, but you have only {user_info['max_storage']} MB of storage available. \n\nPlease upgrade your plan, or attempt upload with fewer data.")
            else: 
                pass
            if user_info["tokens_remaining"] <= 0:
                raise ValueError("You have no tokens remaining. Please upgrade your plan to continue using prism.")
            
            for fl in to_process:
                file = pathlib.Path(fl)
                Knowledge.create(
                    method="filesystem",
                    name=file.name,
                    path=file,
                    knowledge_base_id=_id,
                )
            
            return cls._get(
                endpoint_url=f"users/knowledge_base/{_id}/",
                # **params,
            )

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

        else:

            instance = cls._post(
                endpoint_url=f"users/knowledge_base/",
                name=name,
                **params,
            )

            instance.add(id=instance.json['id'], **params)

            return instance

