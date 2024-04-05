import vertexai
import os

from vertexai.preview.generative_models import(
    Content,
    FunctionDeclaration,
    GenerationConfig,
    GenerativeModel,
    Part,
    Tool
    )
PROJECT_ID=os.environ.get("opti-364416")
LOCATION=os.environ.get("us-central1")
vertexai.init(project=PROJECT_ID,location=LOCATION)
generation_config = {"temperature": 0.1, "max_output_tokens": 8000}
stream=True
## 
def LoadModels():
    text_model=GenerativeModel("gemini-pro")
    mm_mode=GenerativeModel("gemini-pro-vision")
    return text_model, mm_mode

def get_gemini_pro_text_response(model,prompt ):
    
        #txt_model,mm_model=LoadModels()
        responses=model.generate_content(
            prompt,generation_config=generation_config,stream=stream
        )
        
        final_respnse=[]
        for  response in responses:
            try: 
                final_respnse.append(response.text)
            except IndexError: 
                final_respnse.append(" ")
                continue
        return " " .join(final_respnse)

def get_gemini_pro_mm_response(model,prompt_list):
    
    responses = model.generate_content(
        prompt_list, generation_config=generation_config, stream=stream
    )
    final_response=[]
    for response in responses:
        try:
            final_response.append(response.text)
        except IndexError: 
            pass
            
    return " " .join(final_response)

    

    
    

            
            
        
        
        
        
    
    
