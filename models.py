from py2neo import Node, Relationship
from config import graph
import uuid
from datetime import datetime

def create_user(name, email):
    user_id = str(uuid.uuid4())
    user = Node("User", id=user_id, name=name, email=email, created_at=str(datetime.utcnow()))
    graph.create(user)
    return user

def create_post(user_id, title, content):
    user = graph.nodes.match("User", id=user_id).first()
    if not user:
        return None
    post_id = str(uuid.uuid4())
    post = Node("Post", id=post_id, title=title, content=content, created_at=str(datetime.utcnow()))
    rel = Relationship(user, "CREATED", post)
    graph.create(post | rel)
    return post

def create_comment(user_id, post_id, content):
    user = graph.nodes.match("User", id=user_id).first()
    post = graph.nodes.match("Post", id=post_id).first()
    if not user or not post:
        return None
    comment_id = str(uuid.uuid4())
    comment = Node("Comment", id=comment_id, content=content, created_at=str(datetime.utcnow()))
    rel1 = Relationship(user, "CREATED", comment)
    rel2 = Relationship(post, "HAS_COMMENT", comment)
    graph.create(comment | rel1 | rel2)
    return comment

def get_all_users():
    users = []
    for user in graph.nodes.match("User"):
        users.append({
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "created_at": user["created_at"]
        })
    return users

def get_all_posts():
    posts = []
    for post in graph.nodes.match("Post"):
        posts.append({
            "id": post["id"],
            "title": post["title"],
            "content": post["content"],
            "created_at": post["created_at"]
        })
    return posts

def get_all_comments():
    comments = []
    for comment in graph.nodes.match("Comment"):
        comments.append({
            "id": comment["id"],
            "content": comment["content"],
            "created_at": comment["created_at"]
        })
    return comments

def create_friendship(user_id_1, user_id_2):
    user1 = graph.nodes.match("User", id=user_id_1).first()
    user2 = graph.nodes.match("User", id=user_id_2).first()
    if not user1:
        return {"error": f"User with ID {user_id_1} not found"}
    if not user2:
        return {"error": f"User with ID {user_id_2} not found"}
    friendship = Relationship(user1, "FRIENDS_WITH", user2)
    graph.create(friendship)
    return friendship

def like_post(user_id, post_id):
    user = graph.nodes.match("User", id=user_id).first()
    post = graph.nodes.match("Post", id=post_id).first()
    like = Relationship(user, "LIKES", post)
    graph.create(like)
    return like

def like_comment(user_id, comment_id):
    user = graph.nodes.match("User", id=user_id).first()
    comment = graph.nodes.match("Comment", id=comment_id).first()
    if not user or not comment:
        return None
    like = Relationship(user, "LIKES", comment)
    graph.create(like)
    return like

def update_user(user_id, name=None, email=None):
    user = graph.nodes.match("User", id=user_id).first()
    if not user:
        return None
    if name:
        user["name"] = name
    if email:
        user["email"] = email
    graph.push(user)
    return user

def get_user_friends(user_id):
    user = graph.nodes.match("User", id=user_id).first()
    if not user:
        return None
    friends = []
    for rel in graph.match((user, None), r_type="FRIENDS_WITH"):
        friend = rel.end_node
        friends.append({
            "id": friend["id"],
            "name": friend["name"],
            "email": friend["email"],
            "created_at": friend["created_at"]
        })
    return friends

def get_post_likes(post_id):
    post = graph.nodes.match("Post", id=post_id).first()
    if not post:
        return None
    likes = []
    for rel in graph.match((None, post), r_type="LIKES"):
        likes.append({
            "user_id": rel.start_node["id"],
            "user_name": rel.start_node["name"]
        })
    return likes

def get_comment_likes(comment_id):
    comment = graph.nodes.match("Comment", id=comment_id).first()
    if not comment:
        return None
    likes = []
    for rel in graph.match((None, comment), r_type="LIKES"):
        likes.append({
            "user_id": rel.start_node["id"],
            "user_name": rel.start_node["name"]
        })
    return likes

def add_friend(user_id, friend_id):
    return create_friendship(user_id, friend_id)

def remove_friend(user_id, friend_id):
    user1 = graph.nodes.match("User", id=user_id).first()
    user2 = graph.nodes.match("User", id=friend_id).first()
    if not user1 or not user2:
        return None
    rel = graph.match((user1, user2), r_type="FRIENDS_WITH").first()
    if rel:
        graph.separate(rel)
        return True
    return False

def are_friends(user_id, friend_id):
    user1 = graph.nodes.match("User", id=user_id).first()
    user2 = graph.nodes.match("User", id=friend_id).first()
    if not user1 or not user2:
        return False
    rel = graph.match((user1, user2), r_type="FRIENDS_WITH").first()
    return rel is not None

def get_mutual_friends(user_id, other_id):
    user1 = graph.nodes.match("User", id=user_id).first()
    user2 = graph.nodes.match("User", id=other_id).first()
    if not user1 or not user2:
        return []
    query = """
    MATCH (u1:User {id: $user_id})-[:FRIENDS_WITH]-(mutual:User)-[:FRIENDS_WITH]-(u2:User {id: $other_id})
    RETURN mutual
    """
    result = graph.run(query, user_id=user_id, other_id=other_id)
    mutual_friends = []
    for record in result:
        mutual = record["mutual"]
        mutual_friends.append({
            "id": mutual["id"],
            "name": mutual["name"],
            "email": mutual["email"],
            "created_at": mutual["created_at"]
        })
    return mutual_friends

def update_post(post_id, title=None, content=None):
    post = graph.nodes.match("Post", id=post_id).first()
    if not post:
        return None
    if title:
        post["title"] = title
    if content:
        post["content"] = content
    graph.push(post)
    return post

def update_comment(comment_id, content=None):
    comment = graph.nodes.match("Comment", id=comment_id).first()
    if not comment:
        return None
    if content:
        comment["content"] = content
    graph.push(comment)
    return comment

def remove_like(user_id, target_id, target_label):
    user = graph.nodes.match("User", id=user_id).first()
    target = graph.nodes.match(target_label, id=target_id).first()
    
    if not user:
        return {"error": f"User with ID {user_id} not found"}
    if not target:
        return {"error": f"{target_label} with ID {target_id} not found"}
    
    rel = graph.match((user, target), r_type="LIKES").first()
    
    if rel:
        graph.separate(rel)
        return True
    
    return {"error": "Like not found"}