import praw
import requests

reddit_oath = {
    'client_id': 'pIxpnAoiGfwE-g',
    'client_secret': 'Ueccpv4dJegXUYbmAIdwxevxjDs',
    'user_agent': 'wallpapers'
}

wallpapers = praw.Reddit(**reddit_oath).subreddit('wallpapers')

top10 = wallpapers.top(limit=10)

for idx, img_sub in enumerate(top10):
    img_sub.url.split('.')[-1]
    file_ext = img_sub.url.split('.')[-1]
    with open(f'tmp/tmp{idx}.{file_ext}', 'wb') as tmp:
        r = requests.get(img_sub.url, stream=True)
        if r.ok:
            tmp.write(r.content)
    file_ext = img_sub.thumbnail.split('.')[-1]
    with open(f'tmp/tmp{idx}_.{file_ext}', 'wb') as tmp:
        r = requests.get(img_sub.thumbnail, stream=True)
        if r.ok:
            tmp.write(r.content)