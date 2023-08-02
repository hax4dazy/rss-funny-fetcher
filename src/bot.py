import requests, json, xmltodict, time

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
    webhook = ""
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
        image_link.append(image)
        # author name
        author_name.append(xml['feed']['entry'][posts]['author']['name'])
        # author link
        author_link.append(xml['feed']['entry'][posts]['author']['uri'])
        # post link
        post_link.append(xml['feed']['entry'][posts]['link']['@href'])
        # post title
        post_title.append(xml['feed']['entry'][posts]['title'])
        # post time
        post_time.append(xml['feed']['entry'][posts]['published'])
        # post id
        post_id.append(xml['feed']['entry'][posts]['id'])

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
                mark_post_as_sent(g[i])
    time.sleep(600)
