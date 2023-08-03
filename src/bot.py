import requests, json, xmltodict, time, os

sent_posts = set()
concurrentposts = 8
storage = [
    {
        "url": "https://www.reddit.com/r/ecchi/hot.rss?sort=hot&limit=",
    },
    {
        "url": "https://www.reddit.com/r/hentai/hot.rss?sort=hot&limit=",
    },
    {
        "url": "https://www.reddit.com/r/awoo/new.rss?sort=hot&limit=",
    }
]


def sendWebook(img, post_link, post_title, time, author, author_link, subreddit):
    webhook = f"{os.environ['WEBHOOK']}"
    headers = {"Content-Type": "application/json"}
    data = {
        "username": "reddit-nsfw-bot",
        "embeds": [
            {
                "color": 16711823,
                "description": f"[Post Link]({post_link}) [{author}]({author_link}) in {subreddit}",
                "author": {
                    "name": post_title
                },
                "timestamp": time,
                "image": {"url": img},
                "footer": {
                    "text": "Discord Webhook Bot created by @hax4dayz",
                    "icon_url": "https://i.imgur.com/3b6BhDa.jpg"
                }
            }
        ]
    }
    requests.post(webhook, headers=headers, data=json.dumps(data))


def getXMLData(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    try:
        r = requests.get(url, headers=headers)
    except:
        return False
    xml = xmltodict.parse(r.text)
    return xml


def parseDict(xml):
    # image, user_tag, user_link, post_link, post_title, post_time, subreddit
    image_link = []
    author_name = []
    author_link = []
    post_link = []
    post_title = []
    post_time = []
    post_id = []

    for posts in range(concurrentposts):
        # this grabs the raw link from the converted dict
        # I know that this is really bad code. Could be done better
        content = xml['feed']['entry'][posts]['content']['#text']
        start_index_image = content.find('<span><a href="') + len('<span><a href="')
        end_index_image = content.find('">[link]</a>')
        image = content[start_index_image:end_index_image]
        try:
            image_link.append(image)
        except:
            image_link.append('https://cdn.discordapp.com/attachments/649724928542900264/1136450767771942942/resourceNotFound.png')
        # author name
        try:
            author_name.append(xml['feed']['entry'][posts]['author']['name'])
        except:
            author_name.append('Something went wrong')
        # author link
        try:
            author_link.append(xml['feed']['entry'][posts]['author']['uri'])
        except:
            author_link.append('google.com')
        # post link
        try:
            post_link.append(xml['feed']['entry'][posts]['link']['@href'])
        except:
            post_link.append('google.com')
        # post title
        try:
            post_title.append(xml['feed']['entry'][posts]['title'])
        except:
            post_title.append('Something went wrong')
        # post time
        try:
            post_time.append(xml['feed']['entry'][posts]['published'])  
        except:
            post_time.append('Something went wrong')
        # post id
        try:
            post_id.append(xml['feed']['entry'][posts]['id'])
        except:
            post_id.append('Something went wrong')

    # subreddit
    subreddit = xml['feed']['category']['@label']

    return image_link, author_name, author_link, post_link, post_title, post_time, post_id, subreddit


# Function to check if a post has already been sent
def is_post_sent(post_id):
    return post_id in sent_posts


# Function to mark a post as sent
def mark_post_as_sent(post_id):
    sent_posts.add(post_id)


while True:
    for subreddit in storage:
        xmlData = getXMLData(subreddit['url'] + str(concurrentposts))
        a, b, c, d, e, f, g, h = parseDict(xmlData)
        for i in range(concurrentposts):
            if is_post_sent(g[i]) == False:
                sendWebook(a[i], d[i], e[i], f[i], b[i], c[i], h)
                print(f'sent post:', g[i], 'from', h, 'subreddit')
                mark_post_as_sent(g[i])
    print('No more posts, waiting 10 minutes')
    time.sleep(600)
