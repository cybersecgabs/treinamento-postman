from fastapi import FastAPI, Response, HTTPException
import json

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Bem Vindo ao desafio! Sinta-se a vontade a pedir ajuda caso necessite!"}

@app.get("/users")
async def read_users():
    with open("users.json") as f:
        users = json.load(f)["users"]
        users = json.dumps(users, indent=4, ensure_ascii=False)
    return Response(content=users, media_type='application/json')

@app.post("/createuser")
async def create_user(user: dict):
    with open("users.json") as f:
        data = json.load(f)
    
    if "users" not in data:
        data["users"] = []

    if "id" not in user:
        user["id"] = len(data["users"]) + 1
    
    if "nome" not in user:
        raise HTTPException(status_code=400, detail="Nome do usuário é obrigatório")

    if any(u["email"] == user["email"] for u in data["users"]):
        raise HTTPException(status_code=400, detail="Email já registrado")

    data["users"].append(user)
    
    with open("users.json", "w") as f:
        json.dump(data, f, indent=4)

    return {"message": "Usuário criado com sucesso", "user": user}

@app.delete("/deleteuser/{user_id}")
async def delete_user(user_id: int):
    with open("users.json") as f:
        data = json.load(f)

    if "users" not in data:
        raise HTTPException(status_code=404, detail="No users found")

    for user in data["users"]:
        if user["id"] == user_id:
            data["users"].remove(user)
            with open("users.json", "w") as f:
                json.dump(data, f, indent=4)
            return {"message": f"Usuário com o id {user_id} deletado com sucesso!"}

    raise HTTPException(status_code=404, detail=f"Usuário com o id {user_id} não encontrado")

@app.delete("/deleteallusers")
async def delete_all_users():
    with open("users.json") as f:
        data = json.load(f)

    if "users" not in data:
        raise HTTPException(status_code=404, detail="Nenhum usuáriuo encontrado")

    data["users"] = []
    with open("users.json", "w") as f:
        json.dump(data, f, indent=4)
        
    return {"message": "Todos usuários deletados"}

@app.put("/updateuser/{user_id}")
async def update_user(user_id: int, usuario: dict):
    with open("users.json") as f:
        data = json.load(f)

    if "users" not in data:
        raise HTTPException(status_code=404, detail="Nenhum usuário encontrado")

    for user in data["users"]:
        if user["id"] == user_id:
            user["nome"] = usuario["nome"]
            user["email"] = usuario["email"]
            with open("users.json", "w") as f:
                json.dump(data, f, indent=4)
            return {"mensagem": f"Usuário com id {user_id} atualizado com sucesso"}

    raise HTTPException(status_code=404, detail=f"Usuário com id {user_id} não encontrado")