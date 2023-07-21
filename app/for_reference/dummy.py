all_posts = [
    {
        "id": 1,
        "title": "First Post",
        "content": "This is the content of the first post.",
        "published": True,
        "rating": 4
    },
    {
        "id": 2,
        "title": "Second Post",
        "content": "This is the content of the second post.",
        "published": False,
        "rating": 5
    },
    {
        "id": 3,
        "title": "Third Post",
        "content": "This is the content of the third post.",
        "published": True
    },

]


def search_post(post_id):
    for post in all_posts:
        if post["id"] == post_id:
            return post
    return None


def search_post_index(post_id):
    for index, post in enumerate(all_posts):
        if post["id"] == post_id:
            return index
    return None
