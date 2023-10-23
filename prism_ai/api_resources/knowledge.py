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
    "odt"
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

                if path.is_dir(): # We're dealing with a directory.

                    dir_path = pathlib.Path(path)
                    dir_list = list(dir_path.rglob('*'))
                    file_list = []
                    supported_file_list = []

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

                else: # We're dealing with a file. 

                    file_size = os.path.getsize(path)

                    with open(path, 'rb') as file:

                        file_like = cls.FileWithProgress(file, file_size)

                        headers = {'Content-Type': 'application/octet-stream', 'Filename': name}
                        url = cls.api_url + "upload/"

                        with tqdm(total=file_size, unit='B', unit_scale=True, dynamic_ncols=True) as progress_bar:
                            response = requests.post(url, data=file_like, headers=headers)

                    return {"ASDF":"FUCK"}

