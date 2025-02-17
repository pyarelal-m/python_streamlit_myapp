import streamlit as st
from PIL import Image
# import tweepy
import os

# Twitter API Authentication
def authenticate():
    api_key = "A6ezRueARyFYjqbfcqsaKBmfE"
    api_secret = "uU4NZNACFHkarRdZE768ylVbwP8nvXz7OTQvsTgBZzbtlChNg5"
    # access_token = "AAAAAAAAAAAAAAAAAAAAAMDczAAAAAAA2mER0CvQWf%2BaWHEK%2Fm9NtM6vNHU%3Dr9tYeUglllZN84gIEkFgqQHHNPSm0ZtKsF0JR4w4uxcdbQjCQx"
    access_token = "3257961960-dg3DmY8E3kgAFlAmbO1QTdX3OgVcY492R06jUdv"
    access_secret = "40jy4hOA6sfFO4L0PqoRRM6RE08bWyuXAVEiA90ZWQwQc"

    bearer_token = "AAAAAAAAAAAAAAAAAAAAAD3MzAEAAAAAgVLehYDgHybNeSchd%2FptAFyVCvU%3D5ZRgmituQuT6zIEnW3ttDu7mVQXGnsw4smFn2kOQb7Q84gryLy"

    auth = tweepy.OAuthHandler(api_key, api_secret)
    auth.set_access_token(access_token, access_secret)
    return tweepy.API(auth)

    # auth = tweepy.OAuth1UserHandler(api_key, api_secret)
    # auth.set_access_token(access_token, access_secret)
    
    # api = tweepy.API(auth, wait_on_rate_limit=True, retry_count=3)
    # return api

def post_to_twitter(api, text, image_paths):
    # media_ids = [api.media_upload(img).media_id_string for img in image_paths]
    # api.update_status(status=text, media_ids=media_ids)
    # return "Posted successfully!"

    # Generate shareable Twitter link
    twitter_card_url = "https://pyarelal-m-python-streamlit-myapp-app-z4zgby.streamlit.app/images"
    share_url = f"https://twitter.com/intent/tweet?text={text}&url={twitter_card_url}"
    st.markdown(f"[**Share on X (Twitter)**]({share_url})", unsafe_allow_html=True)
    
    st.success("Your image is ready to be shared!")
    
    st.write("### To display the image correctly on X, add these meta tags on your website:")
    st.markdown(f'''
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="My Awesome Image">
    <meta name="twitter:description" content="{text}">
    

    ''',  unsafe_allow_html=True)

    # print(image_paths)
    for path in image_paths:
        st.markdown(f'''
        <meta name="twitter:image" content="{twitter_card_url}/{path}">
        ''',  unsafe_allow_html=True)

    st.markdown(f'''
    <a href="https://twitter.com/intent/tweet?text=Check+out+this+awesome+image!&url={twitter_card_url}/{image_paths[0]}" 
   target="_blank" class="btn btn-primary">
   Share on X
</a>
    ''',  unsafe_allow_html=True)

def resize_image(image, sizes):
    resized_images = {}
    for size in sizes:
        resized_images[size] = image.resize(size, Image.LANCZOS)
    return resized_images

def main():
    st.title("Image Resizer and Twitter Poster")

    # File uploader
    uploaded_file = st.file_uploader("Upload an image", type=["png", "jpg", "jpeg"])
    sizes = [(300, 250), (728, 90), (160, 600), (300, 600)]
    
    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)
        resized_images = resize_image(image, sizes)

        st.write("### Resized Images:")
        saved_images = []
        for size, img in resized_images.items():
            img_path = f"images/resized_{size[0]}x{size[1]}.png"
            img.save(img_path)
            saved_images.append(img_path)
            st.image(img, caption=f"Size: {size[0]}x{size[1]}", use_column_width=True)
            st.download_button(label=f"Download {size[0]}x{size[1]}", data=open(img_path, "rb").read(), file_name=img_path, mime="image/png")

        # Draft Twitter Post
        st.write("### Twitter Post:")
        tweet_text = st.text_area("Enter your tweet:", value="Here are my resized images! #TwitterPost", height=100)

        # Post to Twitter
        if st.button("Post to Twitter"):
            api = authenticate()
            response = post_to_twitter(api, tweet_text, saved_images)

            print(response)
            st.success(response)

if __name__ == "__main__":
    main()

