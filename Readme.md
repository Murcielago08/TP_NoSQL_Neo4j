# API REST avec Flask & Neo4j  

## 📌 Installation  

### 1️⃣ Installer les dépendances  
Dans ton terminal :  
```bash
pip install -r requirements.txt
```

### 2️⃣ Lancer Neo4j avec Docker  
```bash
docker run --name neo4j -d -p 7474:7474 -p 7687:7687 -e NEO4J_AUTH=neo4j/password neo4j
```
👉 Neo4j sera disponible sur : [http://localhost:7474](http://localhost:7474)  
⚠️ Identifiants par défaut : `neo4j / password` (à remplacer si besoin)

### 3️⃣ Démarrer l'API Flask  
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

### 1️⃣ Créer un utilisateur (POST /users)  

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

### 2️⃣ Créer un post (POST /users/<user_id>/posts)  

#### 📌 Tester avec Postman  
- **Méthode** : `POST`  
- **URL** : `http://127.0.0.1:5000/users/1234-5678-abcd/posts`  
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

#### 📌 Vérifier sur Neo4j  
Exécute dans Neo4j :  
```cypher
MATCH (p:Post) RETURN p;
```
👉 Tu devrais voir le post créé !

---

### 3️⃣ Ajouter un commentaire (POST /posts/<post_id>/comments)  

#### 📌 Tester avec Postman  
- **Méthode** : `POST`  
- **URL** : `http://127.0.0.1:5000/posts/abcd-efgh-ijkl/comments`  
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

#### 📌 Vérifier sur Neo4j  
Exécute dans Neo4j :  
```cypher
MATCH (c:Comment) RETURN c;
```
👉 Tu devrais voir le commentaire !

---

### 4️⃣ Supprimer un utilisateur (DELETE /users/<user_id>)  

#### 📌 Tester avec Postman  
- **Méthode** : `DELETE`  
- **URL** : `http://127.0.0.1:5000/users/<user_id>`  
  👉 Remplace `<user_id>` par l'identifiant réel de l'utilisateur, par exemple :  
  `http://127.0.0.1:5000/users/b13ebbb0-e5ec-4cac-942a-5ad84c76a35c`
- **Réponse attendue (200 OK)** :  
```json
{
  "message": "User deleted"
}
```

#### 📌 Vérifier sur Neo4j  
Exécute dans Neo4j :  
```cypher
MATCH (u:User {id: "1234-5678-abcd"}) RETURN u;
```
👉 L'utilisateur ne devrait plus exister.

---

### 5️⃣ Supprimer un post (DELETE /posts/<post_id>)  

#### 📌 Tester avec Postman  
- **Méthode** : `DELETE`  
- **URL** : `http://127.0.0.1:5000/posts/abcd-efgh-ijkl`  
- **Réponse attendue (200 OK)** :  
```json
{
  "message": "Post deleted"
}
```

#### 📌 Vérifier sur Neo4j  
Exécute dans Neo4j :  
```cypher
MATCH (p:Post {id: "abcd-efgh-ijkl"}) RETURN p;
```
👉 Le post ne devrait plus exister.

---

### 6️⃣ Supprimer un commentaire (DELETE /comments/<comment_id>)  

#### 📌 Tester avec Postman  
- **Méthode** : `DELETE`  
- **URL** : `http://127.0.0.1:5000/comments/wxyz-1234`  
- **Réponse attendue (200 OK)** :  
```json
{
  "message": "Comment deleted"
}
```

#### 📌 Vérifier sur Neo4j  
Exécute dans Neo4j :  
```cypher
MATCH (c:Comment {id: "wxyz-1234"}) RETURN c;
```
👉 Le commentaire ne devrait plus exister.

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
| Créer un utilisateur    | POST    | `/users`                        | `MATCH (u:User) RETURN u;`     |
| Créer un post           | POST    | `/users/<user_id>/posts`         | `MATCH (p:Post) RETURN p;`     |
| Ajouter un commentaire  | POST    | `/posts/<post_id>/comments`      | `MATCH (c:Comment) RETURN c;`  |
| Supprimer un utilisateur| DELETE  | `/users/<user_id>`               | `MATCH (u:User {id: "<id>"}) RETURN u;` |
| Supprimer un post       | DELETE  | `/posts/<post_id>`               | `MATCH (p:Post {id: "<id>"}) RETURN p;` |
| Supprimer un commentaire| DELETE  | `/comments/<comment_id>`         | `MATCH (c:Comment {id: "<id>"}) RETURN c;` |