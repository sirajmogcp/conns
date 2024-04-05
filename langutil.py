from langchain_google_vertexai import VertexAI
from langchain_core.messages import HumanMessage
from langchain_google_vertexai import ChatVertexAI

txt_model=VertexAI(model_name="gemini-pro")
mm_model=ChatVertexAI(model_name="gemini-pro-vision")
#mm_model=VertexAI("gemini-pro-vision")
stream=True

def get_lang_txt_response(txt_model,prompt):
    response=txt_model.invoke(prompt)
    return response

def get_lang_mm_response(prompt,image):
    
    image_message={
        "type":"image_url", 
        "image_url":{"url": image}
        }
    
    text_message={
        "type": "text",
        "text": prompt
    }
    message=HumanMessage(content=[text_message,image_message])
    response=mm_model([message])
    return response
    
