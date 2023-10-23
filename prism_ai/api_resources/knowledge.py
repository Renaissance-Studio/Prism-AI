from prism_ai.api_resources.api_resource import APIResource
import requests
from tqdm import tqdm
import os
import pathlib

supported_file_types = [
    "pdf",
    "doc",
    "docx",
    "txt",
    "md",
    "odt",
    "gz"
]

# def bytes_from_file(filename, chunksize=8192):
     
#     rbytes = bytearray()

#     with open(filename, "rb") as f:
#         while True:
#             chunk = f.read(chunksize)
#             if chunk:
#                 for b in chunk:
#                     rbytes.append(b)
#             else:
#                 break
    
#     return bytes(rbytes)

class Knowledge(APIResource):

    '''
    Knowledge Object to be created
    '''
    
    @classmethod
    def create(
        cls,
        **params,
    ):
            
        '''
        Create a new Knowledge Object from a url
        '''

        method = params.pop("method", None)
        name = params.pop("name", None)
        kb_id = params.pop("knowledge_base_id", None)
        text = params.pop("text", None)
        url = params.pop("url", None)
        path = params.pop("path", None)

        class FileWithProgress:
            def __init__(self, file, total_size):
                self.file = file
                self.total_size = total_size
                self.read_size = 0

            def read(self, chunk_size):
                data = self.file.read(chunk_size)
                self.read_size += len(data)
                progress_bar.update(len(data))
                return data


        if method == "text":
            if None in [name, kb_id, text]:
                
                cls._no_params_message(
                    
                    endpoint="Knowledge",
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

        elif method == "url":
            if None in [name, kb_id, url]:
                
                cls._no_params_message(
                    
                    endpoint="Knowledge",
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
            
        elif method == "filesystem":

            if None in [name, kb_id, path]:

                cls._no_params_message(

                    endpoint="Knowledge",
                    req_pars=[
                        "name",
                        "knowledge_base_id",
                        "path",
                    ],
                )
                return None
            
            else:
                try:
                    dir_path = pathlib.Path(path)
                except: 
                    raise ValueError("The path you provided is not valid.")

                if dir_path.is_dir(): # We're dealing with a directory.

                    print("You've provided a directory, to the Knowledge.create method.\n\nPlease use the KnowledgeBase.create method to create a KnowledgeBase from a directory, to create multiple knowledge objects from a directory.")
                    

                else: # We're dealing with a file. 

                    instance = cls(endpoint_url="upload/")
                    file_size = os.path.getsize(path)

                    info_instance = instance._get(endpoint_url="basic_user_info/", quiet=True)
                    user_info = info_instance.json

                    if user_info["max_storage"] != None:
                        if file_size / (1024 * 1024) > user_info["max_storage"]:
                            raise ValueError("You have exceeded your storage limit. Please upgrade your plan to continue using prism.")
                    else: 
                        pass
                    if user_info["tokens_remaining"] <= 0:
                        raise ValueError("You have no tokens remaining. Please upgrade your plan to continue using prism.")
                    if file_size > 4 * 1024 * 1024 * 1024:
                        raise ValueError("The file you provided is too large. The maximum file size is 4GB.")
                    if str(path).split(".")[-1] not in supported_file_types:
                        raise ValueError("The file you provided is not supported. \nSupported file types are: \n\n - pdf \n - doc \n - docx \n - txt \n - md \n - odt")

                    with open(path, 'rb') as file:
                        
                        print("Uploading file "+str(path)+" as "+str(name)+" ...")

                        file_like = FileWithProgress(file, file_size)

                        headers = {'Content-Type': 'application/octet-stream', 'Filename': name}
                        url = instance.api_url + "upload/"

                        with tqdm(total=file_size, unit='B', unit_scale=True, dynamic_ncols=True) as progress_bar:
                            response = requests.post(url, data=file_like, headers=headers)

                    return {"ASDF":"FUCK"}

