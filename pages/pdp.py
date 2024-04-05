import util
import streamlit as st
import soup
import urllib.parse
import base64
from io import BytesIO
from vertexai.preview.vision_models import Image, ImageGenerationModel
from itertools import cycle
st.set_page_config(layout="wide", page_title="Home", page_icon="🧞‍♂️")
st.image("pages/connslogo.png",width=200)
txt_model,mm_model =util.LoadModels()


pdp_url = st.text_input("Product Page URL")

if st.button("Get Product Info"):  
    Product_image,Product_description,Product_features, Product_specs = soup.get_product(pdp_url)
    #Product_description = soup.get_productdescription(pdp_url)
    #Product_features = soup.get_productfeatures(pdp_url)

    prod_desc = Product_description
    promptimg=util.Part.from_uri(Product_image,mime_type="image/jpeg")
    promptimg1="https://storage.googleapis.com/" + Product_image.split("gs://")[1]
    
    # Encode the query string portion of the URL

    # Reconstruct the encoded URL
    encoded_url = urllib.parse.quote(promptimg1, safe='/:') 
    st.image(encoded_url)
    prompttext=("""You are a seasoned product description writer working at conn's homeplus ,  
                             a US-based retailer that sells durable consumer goods and related services.
                             Analyze the provided product image, product description, and product features, 
                             and craft a compelling, engaging product description. 
                             Ensure your product description, feature and benefits are informative and persuasive, 
                             catering to potential buyers. Include the following sections: 
                             Prodcuct Overview (bold): 2 paragraphs, 
                             Key Feature and Benefits (bold): 5 bullet points, 
                             Product specifications: table,
                             Product Category : 1 word,
                             Product brand : 1 word, 
                             theme of image : 1 workd, 
                             and Call to Action : 1 sentence , 
                             and also list at least 10 SEO keywords. in english language""")
    
    adprompttext=("""You are a seasoned marketing copywriter working at conn's homeplus ,  
                             a US-based retailer that sells durable consumer goods and related services.
                             Analyze the provided product image, product description, and product features, 
                             and craft a compelling, engaging facebook ad copy. 
                             in english language""")
    twprompttext=("""You are a seasoned marketing copywriter working at conn's homeplus ,  
                            a US-based retailer that sells durable consumer goods and related services.
                            Analyze the provided product image, product description, and product features, 
                            and craft a compelling, twitter tweet with related emoji, don't offer any promotions. 
                            in english language""")
    
    finalpormpt=f"""" {prompttext}, for "product description: " {prod_desc}  "product features:" {Product_features}  "  "  and product specification:" {Product_specs} """
    prompt_list=[finalpormpt, "using image ", " product image:", promptimg]
    
    adprompt=f"""" {adprompttext}, for "product description: " {prod_desc}  "product features:" {Product_features}  "  "  and product specification:" {Product_specs} """
    prompt_list_ad=[adprompt, "using image ", " product image:", promptimg]
    
    twprompt=f"""" {twprompttext}, for "product description: " {prod_desc}  "product features:" {Product_features}  "  "  and product specification:" {Product_specs} """
    prompt_list_tw=[twprompt, "using image ", " product image:", promptimg]
    
    response=util.get_gemini_pro_mm_response(mm_model,prompt_list)
    
    adresponse=util.get_gemini_pro_mm_response(mm_model,prompt_list_ad)
    
    twresponse=util.get_gemini_pro_mm_response(mm_model,prompt_list_tw)

    tab1, tab2, tab3, tab4 =st.tabs(["Prompt","Original","Generated", "Marketing Content"])
    with tab1:
        st.header("Prompt")
        st.write("Instructions")
        st.write(prompttext)
        st.write("Product description")
        st.write(prod_desc)
        st.write("Product features")
        st.write(Product_features)
        st.write("Product specification")
        st.write(Product_specs)
        
        
        
    with tab2:
        st.header("Original")
        st.write("Product Description")
        st.write(Product_description)
        st.write("Features")
        st.write(Product_features)
        st.write("Specs")
        st.write(Product_specs)
        
    with tab3:  
        st.header("Generated")
        st.write(response)
    with tab4:  
        model = ImageGenerationModel.from_pretrained("imagegeneration@006")
        imageprompt=f""""you are a product photographer generate lifestyle image of digital ads for {response} in a large modern home  photo realistic image with  high resolution """

        st.header("Facebook Post")
        st.write(adresponse)
        
        st.header("Twitter Post")
        st.write(twresponse)
        st.header("Images")
        images1 = model.generate_images(
        prompt=imageprompt,
        # Optional:
        number_of_images=4,
        guidance_scale=2048,
        seed=1
        )

        filteredImages = images1 # your images here
        caption = [] # your caption here
        cols = cycle(st.columns(2,gap="medium")) # st.columns here since it is out of beta at the time I'm writing this
        
        for idx, filteredImage in enumerate(filteredImages):
         
            next(cols).image(filteredImage._image_bytes, width=250)
        
    
    
