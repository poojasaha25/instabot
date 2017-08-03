import requests,urllib
from textblob import TextBlob
from termcolor import colored
from textblob.sentiments import NaiveBayesAnalyzer
import matplotlib.pyplot as plt


BASE_URL = 'https://api.instagram.com/v1/'
APP_ACCESS_TOKEN = '1781606623.579bc1e.11870c626ee747789624b39241f043c5'

Hashtag_list = []


#Fumction to get your own info

def self_info():
    request_url = (BASE_URL+"users/self/?access_token=%s")%(APP_ACCESS_TOKEN)
    print 'GET request url: %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'User does not exist!'
    else:
        print 'Status code other than 200 received!'


#function to get id of a user by username

def get_user_id(insta_username):
    request_url = (BASE_URL + 'users/search?q=%s&access_token=%s') % (insta_username, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            return user_info['data'][0]['id']
        else:
            return None
    else:
        print 'Status code other than 200 received!'
        exit()


#Function to get the information about user by username

def get_user_info(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist!'
        exit()
    request_url = (BASE_URL + 'users/%s?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_info = requests.get(request_url).json()

    if user_info['meta']['code'] == 200:
        if len(user_info['data']):
            print 'Username: %s' % (user_info['data']['username'])
            print 'No. of followers: %s' % (user_info['data']['counts']['followed_by'])
            print 'No. of people you are following: %s' % (user_info['data']['counts']['follows'])
            print 'No. of posts: %s' % (user_info['data']['counts']['media'])
        else:
            print 'There is no data for this user!'
    else:
        print 'Status code other than 200 received!'


#Function to get your recent post

def get_own_post():
    request_url = (BASE_URL + 'users/self/media/recent/?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url,image_name)
            print 'your image has been downloaded'
            caption = own_media['data'][0]['caption']['text']
            print 'Caption is : %s' % (caption)
        else:
            print 'Post does not exit!!'
    else:
        print 'Status code other than 200 recieved!!!'


#function to get the recent post of a user by username

def get_user_post(insta_username):
    user_id = get_user_id(insta_username)
    if user_id == None:
        print 'User does not exist...Please enter a valid username!!!'
        exit()
    request_url = (BASE_URL+'users/%s/media/recent/?access_token=%s') % (user_id,APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            caption = user_media['data'][0]['caption']['text']
            print 'Caption is : %s' % (caption)
            image_name = user_media['data'][0]['id'] + '.jpeg'
            image_url = user_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url,image_name)
            print 'Image is downloaded'
        else:
            print 'Post does not exist'
    else:
        print 'Status code other than 200 recieved'


#Function to get the ID of the recent post of a user by username

def get_post_id(insta_username):
    request_url = (BASE_URL + 'users/self/media/liked?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()

    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'your image has been downloaded'
            caption = own_media['data'][0]['caption']['text']
            print 'Caption is : %s' % (caption)
        else:
            print 'Post does not exit!!'
    else:
        print 'Status code other than 200 recieved!!!'


#Function to like post of a user

def like_a_post(insta_username):
    media_id = get_post_id(insta_username)

    request_url = (BASE_URL + 'media/%s/likes') % (media_id)
    payload = {"access_token": APP_ACCESS_TOKEN}
    print 'POST request url : %s' % (request_url)

    post_a_like = requests.post(request_url, payload).json()
    if post_a_like['meta']['code'] == 200:
        print 'Like was successful!'
    else:
        print 'Your like was unsuccessful. Try again!'

#Function to make a comment on the recent post of the user

def post_a_comment(insta_username):
    media_id = get_post_id(insta_username)
    comment_text = raw_input('Enter comment:')
    payload = {'access_token': APP_ACCESS_TOKEN, 'text' : comment_text}
    request_url = (BASE_URL + 'media/%s/comments') % (media_id)
    print 'POST request url : %s' % (request_url)

    make_comment = requests.get(request_url,payload).json()

    if make_comment['meta']['code'] == 200:
        print 'Successfully added a new comment'
    else:
        print 'Unable to add comment....Try again!!!'


#function to delete negative comments

def delete_negative_comments(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/comments/?access_token=%s') % (media_id,APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    comment_info = requests.get(request_url).json()

    if comment_info['meta']['code'] ==200:
        if len(comment_info['data']):
            for x in range(0,len(comment_info['data'])):
                comment_id = comment_info['data'][x]['id']
                comment_text = comment_info['data'][x]['text']
                blob = TextBlob(comment_text, analyzer=NaiveBayesAnalyzer())
                if (blob.sentiment.p_neg > blob.sentiments.p_pos):
                    print 'Negative comment : %s' % (comment_text)
                    delete_url = (BASE_URL + 'media/%s/comments/%s/?access_token=%s') % (media_id,comment_id,APP_ACCESS_TOKEN)
                    print 'DELETE request url : %s' % (delete_url)
                    delete_info = requests.delete(delete_url)

                    if delete_info['meta']['code'] == 200:
                        print 'Negative comment successfully deleted'
                    else:
                        print 'Unable to delete comment'
                else:
                    print 'No negative comment'
        else:
            print 'There are no existing comments on the post'
    else:
        print 'Status code other than 200 recieved'


#Function to get the list of hashtags of all the posts of a user

def hashtag_analysis(insta_username):
    user_id = get_user_id(insta_username)

    if user_id == None:
        print 'User does not exist'

    request_url = (BASE_URL + 'users/%s/media/recent/?access_token=%s') % (user_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):

            for x in range(0,len(user_media['data'])):
                for hashtags in user_media['data'][x]['tags']:
                    Hashtag_list.append(hashtags)

            tags = " ".join(Hashtag_list)
            menu = True
            while menu:
                choice = raw_input('Enter you choice for Hashtag analysis')
                print 'Enter your choice: '
                print '1.Hashtag analysis through wordcloud\n'
                print '2.Hashtag analysis through piechart\n'
                if choice == '1':
                    wordcloud(tags)
                elif choice == '2':
                    pie_chart()
                else:
                    menu = False
        else:
            print 'No recent posts of the user'

    else:
        print 'Status code other than 200 recieved'

#Function to download image of a user

def download_user_image(insta_username):
    media_id = get_post_id(insta_username)
    request_url = (BASE_URL + 'media/%s/?access_token=%s') % (media_id, APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    user_media = requests.get(request_url).json()

    if user_media['meta']['code'] == 200:
        if len(user_media['data']):
            if user_media['data']['type'] == "image":
                image_name = user_media['data']['id'] + '.jpeg'
                image_url = user_media['data']['images']['standard_resolution']['url']
                urllib.urlretrieve(image_url, image_name)     #using urllib library for downloading the image
                print 'Your image has been downloaded!'
            else:
                print 'The post is not an image'
    else:
        print 'Status code other than 200 received!'


#Function to get the recent post liked by the user

def recently_liked_media():
    request_url = (BASE_URL + 'users/self/media/liked?access_token=%s') % (APP_ACCESS_TOKEN)
    print 'GET request url : %s' % (request_url)
    own_media = requests.get(request_url).json()
    print own_media

    if own_media['meta']['code'] == 200:
        if len(own_media['data']):
            liked_media_id = own_media['data'][0]['id']
            print liked_media_id

            image_name = own_media['data'][0]['id'] + '.jpeg'
            image_url = own_media['data'][0]['images']['standard_resolution']['url']
            urllib.urlretrieve(image_url, image_name)
            print 'Recently liked media is downloaded successfully'
        else:
            print 'Post does not exit!!'
    else:
        print 'Status code other than 200 recieved!!!'


#Function to create pie chart

def pie_chart():
    max_hashtag = max(Hashtag_list)
    min_hashtag = min(Hashtag_list)

    x = Hashtag_list.count(max_hashtag)
    y = Hashtag_list.count(min_hashtag)

    total = len(Hashtag_list)
    a = float(x) * 100 / total
    b = float(y) * 100 / total

    labels = max_hashtag, min_hashtag
    sizes = [a, b]
    colors = ['red', 'lightskyblue']
    explode = (0.2, 0)  # explode the 1st slice

    plt.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
            shadow=True, startangle=140)
    plt.axis('equal')
    plt.title('Hashtag Analysis')
    plt.show()




#Function to start instabot

def start_bot():
    while True:
        print '\n'
        print colored('Hey! Welcome to instaBot!','blue')
        print colored('What do you wanna do???', 'cyan')
        print 'Here are your options:'
        print '1.Get your own details\n'
        print '2.Get details of a user by username\n'
        print '3.Get your own recent post\n'
        print '4.Get recent post of a user by username'
        print '5.Like the recent post of a user'
        print '6.Make a comment on the recent post of a user'
        print '7.Delete the negative comments on the post'
        print '8.Hashtag analysis using wordcloud and piechart'
        print '9.Get the recent post liked by the user'
        print '10.Download image of a user'
        print '11.exit'

        choice = raw_input("Enter your choice: ")
        if choice == '1':
            self_info()
        elif choice == '2':
            insta_username = raw_input("Enter the username of the user: ")
            get_user_info(insta_username)
        elif choice == '3':
            get_own_post()
        elif choice == '4':
            insta_username = raw_input("Enter the name of the user: ")
            get_user_post(insta_username)
        elif choice == '5':
            insta_username = raw_input("Enter the name of the user: ")
            like_a_post(insta_username)
        elif choice == '6':
            insta_username = raw_input("Enter the name of the user: ")
            post_a_comment(insta_username)
        elif choice == '7':
            insta_username = raw_input("Enter the username of the user: ")
            delete_negative_comments(insta_username)
        elif choice == '8':
            insta_username = raw_input("Enter the username of the user: ")
            hashtag_analysis(insta_username)
        elif choice == '9':
            recently_liked_media()
        elif choice == '10':
            insta_username = raw_input("Enter the username of the user")
            download_user_image(insta_username)
        elif choice == '11':
            exit()
        else:
            print "You have not entered a correct choice"

start_bot()