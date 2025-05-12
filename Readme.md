# API REST avec Flask & Neo4j  

## 📌 Installation  

### 1️⃣ Create python virtual environment
```bash
python -m venv nosql
```

# On Windows
nosql\Scripts\activate

### 2️⃣ Installer les dépendances  
Dans ton terminal :  
```bash
pip install -r requirements.txt
```

### 3️⃣ Lancer Neo4j avec Docker  
```bash
docker run --name neo4j -d -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/password neo4j
```
👉 Neo4j sera disponible sur : [http://localhost:7474](http://localhost:7474)  
⚠️ Identifiants par défaut : `neo4j / password` (à remplacer si besoin)

### 4️⃣ Démarrer l'API Flask  
```bash
python app.py
```
👉 L'API sera accessible sur [http://127.0.0.1:5000](http://127.0.0.1:5000) 🚀  

---

### 🛑 Arrêter les serveurs  

#### 1️⃣ Arrêter Neo4j  
Dans ton terminal :  
```bash
docker stop neo4j
```

#### 2️⃣ Arrêter l'API Flask  
Si l'API Flask est en cours d'exécution dans le terminal, utilise `Ctrl + C` pour l'arrêter.

---

## 🔥 Tester les Routes  

### Routes pour les utilisateurs  

#### 1️⃣ Récupérer la liste des utilisateurs (GET /users)  

#### 📌 Méthode 1 : Tester avec Postman  
- **Méthode** : `GET`  
- **URL** : `http://127.0.0.1:5000/users`  

---

#### 2️⃣ Créer un utilisateur (POST /users)  

#### 📌 Méthode 1 : Tester avec Postman  
- **Méthode** : `POST`  
- **URL** : `http://127.0.0.1:5000/users`  
- **Body (JSON)** :  
```json
{
  "name": "Alice",
  "email": "alice@example.com"
}
```
- **Réponse attendue (201 Created)** :  
```json
{
  "message": "User created",
  "user": {
    "id": "1234-5678-abcd",
    "name": "Alice",
    "email": "alice@example.com",
    "created_at": "2025-03-31T12:00:00"
  }
}
```

#### 📌 Méthode 2 : Vérifier sur Neo4j  
1. Ouvre Neo4j sur [http://localhost:7474](http://localhost:7474)  
2. Connecte-toi avec `neo4j / password`  
3. Exécute cette requête Cypher :  
```cypher
MATCH (u:User) RETURN u;
```
👉 Tu devrais voir le nouvel utilisateur ajouté !

---

#### 3️⃣ Récupérer un utilisateur par son ID (GET /users/:id)  

#### 📌 Méthode 1 : Tester avec Postman  
- **Méthode** : `GET`  
- **URL** : `http://127.0.0.1:5000/users/<id>`  

#### 📌 Méthode 2 : Vérifier sur Neo4j  
1. Ouvre Neo4j sur [http://localhost:7474](http://localhost:7474)  
2. Connecte-toi avec `neo4j / password`  
3. Exécute cette requête Cypher :  
```cypher
MATCH (u:User {id: "<id>"}) RETURN u;
```
👉 Tu devrais voir l'utilisateur correspondant !

---

#### 4️⃣ Mettre à jour un utilisateur par son ID (PUT /users/:id)  

#### 📌 Méthode 1 : Tester avec Postman  
- **Méthode** : `PUT`  
- **URL** : `http://127.0.0.1:5000/users/<id>`  
- **Body (JSON)** :  
```json
{
  "name": "Alice Updated",
  "email": "alice.updated@example.com"
}
```
- **Réponse attendue (200 OK)** :  
```json
{
  "message": "User updated",
  "user": {
    "id": "1234-5678-abcd",
    "name": "Alice Updated",
    "email": "alice.updated@example.com",
    "updated_at": "2025-03-31T12:30:00"
  }
}
```

#### 📌 Méthode 2 : Vérifier sur Neo4j  
1. Ouvre Neo4j sur [http://localhost:7474](http://localhost:7474)  
2. Connecte-toi avec `neo4j / password`  
3. Exécute cette requête Cypher :  
```cypher
MATCH (u:User {id: "1234-5678-abcd"}) RETURN u;
```
👉 Tu devrais voir les informations mises à jour !

---

#### 5️⃣ Supprimer un utilisateur par son ID (DELETE /users/:id)  

#### 📌 Méthode 1 : Tester avec Postman  
- **Méthode** : `DELETE`  
- **URL** : `http://127.0.0.1:5000/users/<id>`  

#### 📌 Méthode 2 : Vérifier sur Neo4j  
1. Ouvre Neo4j sur [http://localhost:7474](http://localhost:7474)  
2. Connecte-toi avec `neo4j / password`  
3. Exécute cette requête Cypher :  
```cypher
MATCH (u:User {id: "<id>"}) RETURN u;
```
👉 L'utilisateur ne devrait plus exister !

---

#### 6️⃣ Récupérer la liste des amis d'un utilisateur (GET /users/:id/friends)  

#### 📌 Méthode 1 : Tester avec Postman  
- **Méthode** : `GET`  
- **URL** : `http://127.0.0.1:5000/users/<id>/friends`  

#### 📌 Méthode 2 : Vérifier sur Neo4j  
1. Ouvre Neo4j sur [http://localhost:7474](http://localhost:7474)  
2. Connecte-toi avec `neo4j / password`  
3. Exécute cette requête Cypher :  
```cypher
MATCH (u:User {id: "<id>"})-[:FRIENDS_WITH]->(f:User) RETURN f;
```

---

#### 7️⃣ Ajouter un ami (POST /users/:id/friends)  

#### 📌 Méthode 1 : Tester avec Postman  
- **Méthode** : `POST`  
- **URL** : `http://127.0.0.1:5000/users/<id>/friends`  
- **Body (JSON)** :  
```json
{
  "friend_id": "5ddd1b71-f0dc-4c40-9386-5b5cadace7ac"
}
```
- **Réponse attendue (201 Created)** :  
```json
{
  "message": "Friend added"
}
```

#### 📌 Méthode 2 : Vérifier sur Neo4j  
1. Ouvre Neo4j sur [http://localhost:7474](http://localhost:7474)  
2. Connecte-toi avec `neo4j / password`  
3. Exécute cette requête Cypher :  
```cypher
MATCH (u:User {id: "<id>"})-[:FRIENDS_WITH]->(f:User {id: "friend-id"}) RETURN f;
```
👉 Tu devrais voir l'ami ajouté !

---

#### 8️⃣ Supprimer un ami (DELETE /users/:id/friends/:friendId)  

#### 📌 Méthode 1 : Tester avec Postman  
- **Méthode** : `DELETE`  
- **URL** : `http://127.0.0.1:5000/users/<id>/friends/<friendId>`  

#### 📌 Méthode 2 : Vérifier sur Neo4j  
1. Ouvre Neo4j sur [http://localhost:7474](http://localhost:7474)  
2. Connecte-toi avec `neo4j / password`  
3. Exécute cette requête Cypher :  
```cypher
MATCH (u:User {id: "<id>"})-[r:FRIENDS_WITH]->(f:User {id: "<friendId>"}) DELETE r;
```
👉 La relation d'amitié devrait être supprimée !

---

#### 9️⃣ Vérifier si deux utilisateurs sont amis (GET /users/:id/friends/:friendId)  

#### 📌 Méthode 1 : Tester avec Postman  
- **Méthode** : `GET`  
- **URL** : `http://127.0.0.1:5000/users/<id>/friends/<friendId>`  

#### 📌 Méthode 2 : Vérifier sur Neo4j  
1. Ouvre Neo4j sur [http://localhost:7474](http://localhost:7474)  
2. Connecte-toi avec `neo4j / password`  
3. Exécute cette requête Cypher :  
```cypher
MATCH (u:User {id: "<id>"})-[:FRIENDS_WITH]-(f:User {id: "<friendId>"}) RETURN f;
```
👉 Si une relation existe, les utilisateurs sont amis !

---

#### 🔟 Récupérer les amis en commun (GET /users/:id/mutual-friends/:otherId)  

#### 📌 Méthode 1 : Tester avec Postman  
- **Méthode** : `GET`  
- **URL** : `http://127.0.0.1:5000/users/<id>/mutual-friends/<otherId>`  

#### 📌 Méthode 2 : Vérifier sur Neo4j  
1. Ouvre Neo4j sur [http://localhost:7474](http://localhost:7474)  
2. Connecte-toi avec `neo4j / password`  
3. Exécute cette requête Cypher :  
```cypher
MATCH (u:User {id: "<id>"})-[:FRIEND]->(m:User)<-[:FRIEND]-(o:User {id: "<otherId>"}) RETURN m;
```
👉 Tu devrais voir les amis en commun !

---

### Routes pour les posts  

#### 1️⃣ Récupérer tous les posts (GET /posts)  

#### 📌 Méthode 1 : Tester avec Postman  
- **Méthode** : `GET`  
- **URL** : `http://127.0.0.1:5000/posts`  

#### 📌 Méthode 2 : Vérifier sur Neo4j  
1. Ouvre Neo4j sur [http://localhost:7474](http://localhost:7474)  
2. Connecte-toi avec `neo4j / password`  
3. Exécute cette requête Cypher :  
```cypher
MATCH (p:Post) RETURN p;
```
👉 Tu devrais voir la liste de tous les posts !

---

#### 2️⃣ Récupérer un post par son ID (GET /posts/:id)  

#### 📌 Méthode 1 : Tester avec Postman  
- **Méthode** : `GET`  
- **URL** : `http://127.0.0.1:5000/posts/<id>`  

#### 📌 Méthode 2 : Vérifier sur Neo4j  
1. Ouvre Neo4j sur [http://localhost:7474](http://localhost:7474)  
2. Connecte-toi avec `neo4j / password`  
3. Exécute cette requête Cypher :  
```cypher
MATCH (p:Post {id: "<id>"}) RETURN p;
```
👉 Tu devrais voir le post correspondant !

---

#### 3️⃣ Récupérer les posts d'un utilisateur (GET /users/:id/posts)  

#### 📌 Méthode 1 : Tester avec Postman  
- **Méthode** : `GET`  
- **URL** : `http://127.0.0.1:5000/users/<id>/posts`  

#### 📌 Méthode 2 : Vérifier sur Neo4j  
1. Ouvre Neo4j sur [http://localhost:7474](http://localhost:7474)  
2. Connecte-toi avec `neo4j / password`  
3. Exécute cette requête Cypher :  
```cypher
MATCH (u:User {id: "<id>"})-[:CREATED]->(p:Post) RETURN p;
```
👉 Tu devrais voir les posts créés par l'utilisateur !

---

#### 4️⃣ Créer un post (POST /users/:id/posts)  

#### 📌 Méthode 1 : Tester avec Postman  
- **Méthode** : `POST`  
- **URL** : `http://127.0.0.1:5000/users/<id>/posts`  
- **Body (JSON)** :  
```json
{
  "title": "Mon premier post",
  "content": "Ceci est un test"
}
```
- **Réponse attendue (201 Created)** :  
```json
{
  "message": "Post created",
  "post": {
    "id": "abcd-efgh-ijkl",
    "title": "Mon premier post",
    "content": "Ceci est un test",
    "created_at": "2025-03-31T12:05:00"
  }
}
```

#### 📌 Méthode 2 : Vérifier sur Neo4j  
1. Ouvre Neo4j sur [http://localhost:7474](http://localhost:7474)  
2. Connecte-toi avec `neo4j / password`  
3. Exécute cette requête Cypher :  
```cypher
MATCH (u:User {id: "<id>"})-[:CREATED]->(p:Post {id: "abcd-efgh-ijkl"}) RETURN p;
```
👉 Tu devrais voir le post lié à son créateur !

---

#### 5️⃣ Mettre à jour un post (PUT /posts/:id)  

#### 📌 Méthode 1 : Tester avec Postman  
- **Méthode** : `PUT`  
- **URL** : `http://127.0.0.1:5000/posts/<id>`  
- **Body (JSON)** :  
```json
{
  "title": "Titre mis à jour",
  "content": "Contenu mis à jour"
}
```
- **Réponse attendue (200 OK)** :  
```json
{
  "message": "Post updated",
  "post": {
    "id": "abcd-efgh-ijkl",
    "title": "Titre mis à jour",
    "content": "Contenu mis à jour",
    "updated_at": "2025-03-31T12:30:00"
  }
}
```

#### 📌 Méthode 2 : Vérifier sur Neo4j  
1. Ouvre Neo4j sur [http://localhost:7474](http://localhost:7474)  
2. Connecte-toi avec `neo4j / password`  
3. Exécute cette requête Cypher :  
```cypher
MATCH (p:Post {id: "abcd-efgh-ijkl"}) RETURN p;
```
👉 Tu devrais voir les informations mises à jour !

---
#### 6️⃣ Supprimer un post (DELETE /users/:user_id/posts/:post_id)  

#### 📌 Méthode 1 : Tester avec Postman  
- **Méthode** : `DELETE`  
- **URL** : `http://127.0.0.1:5000/users/<user_id>/posts/<post_id>`  

#### 📌 Méthode 2 : Vérifier sur Neo4j  
1. Ouvre Neo4j sur [http://localhost:7474](http://localhost:7474)  
2. Connecte-toi avec `neo4j / password`  
3. Exécute cette requête Cypher :  
```cypher
MATCH (u:User {id: "<user_id>"})-[:CREATED]->(p:Post {id: "<post_id>"}) RETURN p;
```
👉 Le post ne devrait plus exister pour cet utilisateur !

---

#### 7️⃣ Ajouter un like à un post (POST /posts/:id/like)  

#### 📌 Méthode 1 : Tester avec Postman  
- **Méthode** : `POST`  
- **URL** : `http://127.0.0.1:5000/posts/<id>/like`  
- **Body (JSON)** :  
```json
{
  "user_id": "1234-5678-abcd"
}
```
- **Réponse attendue (201 Created)** :  
```json
{
  "message": "Like added"
}
```

#### 📌 Méthode 2 : Vérifier sur Neo4j  
1. Ouvre Neo4j sur [http://localhost:7474](http://localhost:7474)  
2. Connecte-toi avec `neo4j / password`  
3. Exécute cette requête Cypher :  
```cypher
MATCH (u:User {id: "1234-5678-abcd"})-[:LIKES]->(p:Post {id: "<id>"}) RETURN p;
```
👉 Tu devrais voir la relation de like ajoutée !

---

#### 8️⃣ Retirer un like d'un post (DELETE /posts/:id/like)  

#### 📌 Méthode 1 : Tester avec Postman  
- **Méthode** : `DELETE`  
- **URL** : `http://127.0.0.1:5000/posts/<id>/like`  
- **Body (JSON)** :  
```json
{
  "user_id": "1234-5678-abcd"
}
```
- **Réponse attendue (200 OK)** :  
```json
{
  "message": "Like removed"
}
```

#### 📌 Méthode 2 : Vérifier sur Neo4j  
1. Ouvre Neo4j sur [http://localhost:7474](http://localhost:7474)  
2. Connecte-toi avec `neo4j / password`  
3. Exécute cette requête Cypher :  
```cypher
MATCH (u:User {id: "1234-5678-abcd"})-[r:LIKES]->(p:Post {id: "<id>"}) DELETE r;
```
👉 La relation de like devrait être supprimée !

---

#### 9️⃣ Get likes for a post (GET /posts/:id/likes)  

#### 📌 Method 1: Test with Postman  
- **Method**: `GET`  
- **URL**: `http://127.0.0.1:5000/posts/<id>/likes`  

#### 📌 Method 2: Verify on Neo4j  
1. Open Neo4j at [http://localhost:7474](http://localhost:7474).  
2. Log in with `neo4j / password`.  
3. Run this Cypher query:  
```cypher
MATCH (u:User)-[:LIKES]->(p:Post {id: "<id>"}) RETURN u;
```
👉 You should see the users who liked the post!

---

### Routes pour les commentaires  

#### 1️⃣ Récupérer les commentaires d'un post (GET /posts/:id/comments)  

#### 📌 Méthode 1 : Tester avec Postman  
- **Méthode** : `GET`  
- **URL** : `http://127.0.0.1:5000/posts/<id>/comments`  

#### 📌 Méthode 2 : Vérifier sur Neo4j  
1. Ouvre Neo4j sur [http://localhost:7474](http://localhost:7474)  
2. Connecte-toi avec `neo4j / password`  
3. Exécute cette requête Cypher :  
```cypher
MATCH (p:Post {id: "<id>"})-[:HAS_COMMENT]->(c:Comment) RETURN c;
```
👉 Tu devrais voir les commentaires liés au post !

---

#### 2️⃣ Ajouter un commentaire (POST /posts/:id/comments)  

#### 📌 Méthode 1 : Tester avec Postman  
- **Méthode** : `POST`  
- **URL** : `http://127.0.0.1:5000/posts/<id>/comments`  
- **Body (JSON)** :  
```json
{
  "user_id": "1234-5678-abcd",
  "content": "Super post !"
}
```
- **Réponse attendue (201 Created)** :  
```json
{
  "message": "Comment added",
  "comment": {
    "id": "wxyz-1234",
    "content": "Super post !",
    "created_at": "2025-03-31T12:10:00"
  }
}
```

#### 📌 Méthode 2 : Vérifier sur Neo4j  
1. Ouvre Neo4j sur [http://localhost:7474](http://localhost:7474)  
2. Connecte-toi avec `neo4j / password`  
3. Exécute cette requête Cypher :  
```cypher
MATCH (u:User {id: "1234-5678-abcd"})-[:CREATED]->(c:Comment {id: "wxyz-1234"})<-[:HAS_COMMENT]-(p:Post {id: "<id>"}) RETURN c;
```
👉 Tu devrais voir le commentaire lié à l'utilisateur et au post !

---

#### 3️⃣ Supprimer un commentaire (DELETE /posts/:postId/comments/:commentId)  

#### 📌 Méthode 1 : Tester avec Postman  
- **Méthode** : `DELETE`  
- **URL** : `http://127.0.0.1:5000/posts/<postId>/comments/<commentId>`  

#### 📌 Méthode 2 : Vérifier sur Neo4j  
1. Ouvre Neo4j sur [http://localhost:7474](http://localhost:7474)  
2. Connecte-toi avec `neo4j / password`  
3. Exécute cette requête Cypher :  
```cypher
MATCH (p:Post {id: "<postId>"})-[r:HAS_COMMENT]->(c:Comment {id: "<commentId>"}) DELETE r, c;
```
👉 Le commentaire et sa relation avec le post devraient être supprimés !

---

#### 4️⃣ Récupérer tous les commentaires (GET /comments)  

#### 📌 Méthode 1 : Tester avec Postman  
- **Méthode** : `GET`  
- **URL** : `http://127.0.0.1:5000/comments`  

#### 📌 Méthode 2 : Vérifier sur Neo4j  
1. Ouvre Neo4j sur [http://localhost:7474](http://localhost:7474)  
2. Connecte-toi avec `neo4j / password`  
3. Exécute cette requête Cypher :  
```cypher
MATCH (c:Comment) RETURN c;
```
👉 Tu devrais voir tous les commentaires !

---

#### 5️⃣ Récupérer un commentaire par son ID (GET /comments/:id)  

#### 📌 Méthode 1 : Tester avec Postman  
- **Méthode** : `GET`  
- **URL** : `http://127.0.0.1:5000/comments/<id>`  

#### 📌 Méthode 2 : Vérifier sur Neo4j  
1. Ouvre Neo4j sur [http://localhost:7474](http://localhost:7474)  
2. Connecte-toi avec `neo4j / password`  
3. Exécute cette requête Cypher :  
```cypher
MATCH (c:Comment {id: "<id>"}) RETURN c;
```
👉 Tu devrais voir le commentaire correspondant !

---

#### 6️⃣ Mettre à jour un commentaire (PUT /comments/:id)  

#### 📌 Méthode 1 : Tester avec Postman  
- **Méthode** : `PUT`  
- **URL** : `http://127.0.0.1:5000/comments/<id>`  
- **Body (JSON)** :  
```json
{
  "content": "Commentaire mis à jour"
}
```
- **Réponse attendue (200 OK)** :  
```json
{
  "message": "Comment updated",
  "comment": {
    "id": "wxyz-1234",
    "content": "Commentaire mis à jour",
    "updated_at": "2025-03-31T12:30:00"
  }
}
```

#### 📌 Méthode 2 : Vérifier sur Neo4j  
1. Ouvre Neo4j sur [http://localhost:7474](http://localhost:7474)  
2. Connecte-toi avec `neo4j / password`  
3. Exécute cette requête Cypher :  
```cypher
MATCH (c:Comment {id: "wxyz-1234"}) RETURN c;
```
👉 Tu devrais voir les informations mises à jour !

---

#### 7️⃣ Supprimer un commentaire (DELETE /comments/:id)  

#### 📌 Méthode 1 : Tester avec Postman  
- **Méthode** : `DELETE`  
- **URL** : `http://127.0.0.1:5000/comments/<id>`  

#### 📌 Méthode 2 : Vérifier sur Neo4j  
1. Ouvre Neo4j sur [http://localhost:7474](http://localhost:7474)  
2. Connecte-toi avec `neo4j / password`  
3. Exécute cette requête Cypher :  
```cypher
MATCH (c:Comment {id: "<id>"}) DELETE c;
```
👉 Le commentaire devrait être supprimé !

---

#### 8️⃣ Ajouter un like à un commentaire (POST /comments/:id/like)  

#### 📌 Méthode 1 : Tester avec Postman  
- **Méthode** : `POST`  
- **URL** : `http://127.0.0.1:5000/comments/<id>/like`  
- **Body (JSON)** :  
```json
{
  "user_id": "1234-5678-abcd"
}
```
- **Réponse attendue (201 Created)** :  
```json
{
  "message": "Like added"
}
```

#### 📌 Méthode 2 : Vérifier sur Neo4j  
1. Ouvre Neo4j sur [http://localhost:7474](http://localhost:7474)  
2. Connecte-toi avec `neo4j / password`  
3. Exécute cette requête Cypher :  
```cypher
MATCH (u:User {id: "1234-5678-abcd"})-[:LIKES]->(c:Comment {id: "<id>"}) RETURN c;
```
👉 Tu devrais voir la relation de like ajoutée !

---

#### 9️⃣ Retirer un like d'un commentaire (DELETE /comments/:id/like)  

#### 📌 Méthode 1 : Tester avec Postman  
- **Méthode** : `DELETE`  
- **URL** : `http://127.0.0.1:5000/comments/<id>/like`  
- **Body (JSON)** :  
```json
{
  "user_id": "1234-5678-abcd"
}
```
- **Réponse attendue (200 OK)** :  
```json
{
  "message": "Like removed"
}
```

#### 📌 Méthode 2 : Vérifier sur Neo4j  
1. Ouvre Neo4j sur [http://localhost:7474](http://localhost:7474)  
2. Connecte-toi avec `neo4j / password`  
3. Exécute cette requête Cypher :  
```cypher
MATCH (u:User {id: "1234-5678-abcd"})-[r:LIKES]->(c:Comment {id: "<id>"}) DELETE r;
```
👉 La relation de like devrait être supprimée !

---

#### 🔟 Récupérer les likes d'un commentaire (GET /comments/:id/likes)  

#### 📌 Méthode 1 : Tester avec Postman  
- **Méthode** : `GET`  
- **URL** : `http://127.0.0.1:5000/comments/<id>/likes`  

#### 📌 Méthode 2 : Vérifier sur Neo4j  
1. Ouvre Neo4j sur [http://localhost:7474](http://localhost:7474).  
2. Connecte-toi avec `neo4j / password`.  
3. Exécute cette requête Cypher :  
```cypher
MATCH (u:User)-[:LIKES]->(c:Comment {id: "<id>"}) RETURN u;
```
👉 Tu devrais voir les utilisateurs qui ont liké le commentaire !

#### 📌 Method 1: Test with Postman  
- **Method**: `GET`  
- **URL**: `http://127.0.0.1:5000/comments/<id>/likes`  

#### 📌 Method 2: Verify on Neo4j  
1. Open Neo4j at [http://localhost:7474](http://localhost:7474).  
2. Log in with `neo4j / password`.  
3. Run this Cypher query:  
```cypher
MATCH (u:User)-[:LIKES]->(c:Comment {id: "<id>"}) RETURN u;
```
👉 You should see the users who liked the comment!

---

## 🛠️ Comment tester les routes avec Postman  

1. **Installer Postman**  
   Télécharge et installe Postman depuis [https://www.postman.com/downloads/](https://www.postman.com/downloads/).

2. **Créer une nouvelle requête**  
   - Ouvre Postman et clique sur "New" > "Request".
   - Choisis la méthode HTTP (par exemple, `POST`).
   - Saisis l'URL de l'API (par exemple, `http://127.0.0.1:5000/users`).

3. **Configurer le corps de la requête**  
   - Va dans l'onglet "Body".
   - Sélectionne "raw" et choisis "JSON" dans le menu déroulant.
   - Ajoute le contenu JSON requis (par exemple, pour créer un utilisateur :  
     ```json
     {
       "name": "Alice",
       "email": "alice@example.com"
     }
     ```

4. **Envoyer la requête**  
   - Clique sur "Send".
   - Vérifie la réponse dans l'onglet "Response".

5. **Vérifier dans Neo4j**  
   - Connecte-toi à l'interface Neo4j sur [http://localhost:7474](http://localhost:7474).
   - Exécute la requête Cypher correspondante pour vérifier les données (par exemple, `MATCH (u:User) RETURN u;`).

---

## ✅ Résumé des Tests  

| Action                  | Méthode | URL                              | Vérification sur Neo4j          |
|-------------------------|---------|----------------------------------|---------------------------------|
| Récupérer la liste des utilisateurs | GET    | `/users`                        | `MATCH (u:User) RETURN u;`     |
| Créer un utilisateur    | POST    | `/users`                        | `MATCH (u:User) RETURN u;`     |
| Récupérer un utilisateur par son ID | GET    | `/users/<id>`                   | `MATCH (u:User {id: "<id>"}) RETURN u;` |
| Mettre à jour un utilisateur par son ID | PUT    | `/users/<id>`                   | `MATCH (u:User {id: "1234-5678-abcd"}) RETURN u;` |
| Supprimer un utilisateur par son ID | DELETE  | `/users/<id>`                   | `MATCH (u:User {id: "<id>"}) RETURN u;` |
| Récupérer la liste des amis d'un utilisateur | GET    | `/users/<id>/friends`           | `MATCH (u:User {id: "<id>"})-[:FRIEND]->(f:User) RETURN f;` |
| Ajouter un ami          | POST    | `/users/<id>/friends`            | `MATCH (u:User {id: "<id>"})-[:FRIENDS_WITH]->(f:User {id: "friend-id"}) RETURN f;` |
| Supprimer un ami        | DELETE  | `/users/<id>/friends/<friendId>` | `MATCH (u:User {id: "<id>"})-[r:FRIENDS_WITH]->(f:User {id: "<friendId>"}) DELETE r;` |
| Vérifier si deux utilisateurs sont amis | GET    | `/users/<id>/friends/<friendId>` | `MATCH (u:User {id: "<id>"})-[:FRIEND]-(f:User {id: "<friendId>"}) RETURN f;` |
| Récupérer les amis en commun | GET    | `/users/<id>/mutual-friends/<otherId>` | `MATCH (u:User {id: "<id>"})-[:FRIEND]->(m:User)<-[:FRIEND]-(o:User {id: "<otherId>"}) RETURN m;` |
| Créer un post           | POST    | `/users/<user_id>/posts`         | `MATCH (p:Post) RETURN p;`     |
| Ajouter un commentaire  | POST    | `/posts/<post_id>/comments`      | `MATCH (c:Comment) RETURN c;`  |
| Supprimer un utilisateur| DELETE  | `/users/<user_id>`               | `MATCH (u:User {id: "1234-5678-abcd"}) RETURN u;` |
| Supprimer un post       | DELETE  | `/posts/<post_id>`               | `MATCH (p:Post {id: "abcd-efgh-ijkl"}) RETURN p;` |
| Supprimer un commentaire| DELETE  | `/comments/<comment_id>`         | `MATCH (c:Comment {id: "wxyz-1234"}) RETURN c;` |