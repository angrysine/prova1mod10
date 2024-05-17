from fastapi import FastAPI
import sqlite3
from pydantic import BaseModel
import uvicorn

class Pedido(BaseModel):
    username : str
    email : str
    description : str

app = FastAPI()

@app.post("/novo")
def createPedido(pedido: Pedido):
    con = sqlite3.connect("sqlite.db")
    cur = con.cursor()
    cur.execute("select max(id) as id from pedidos")
    id =cur.fetchone()[0]
    if not id:
        id =0
    cur.execute("insert into pedidos (username,email,description) values (?,?,?)",(pedido.username,pedido.email,pedido.description,))
    con.commit()
    
    return {"status": id+1}

@app.get("/pedidos")
def getAllPedidos():
   
    con = sqlite3.connect("sqlite.db")
    cur = con.cursor()
    
    response = cur.execute("select * from pedidos")
    pedidos = response.fetchall()
    return pedidos

@app.get("/pedidos/{id}")
def getPedidoById(id: int):
    con = sqlite3.connect("sqlite.db")
    cur = con.cursor()
    resposta = cur.execute("select * from pedidos where id =?",(str(id)))
    pedido =resposta.fetchone()

    if not pedido:
        return "pedido not found"
    return pedido

@app.put("/pedidos/{id}")
def updatePedido(id :int,pedido:Pedido):
    con = sqlite3.connect("sqlite.db")
    cur = con.cursor()
    cur.execute("update pedidos set username = ?,email = ?, description =? where id =?",(pedido.username,pedido.email,pedido.description,id))
    con.commit()
    return "pedido atualizado com sucesso"

@app.delete("/pedidos/{id}")
def deletePedido(id:int):
    con = sqlite3.connect("sqlite.db")
    cur = con.cursor()
    cur.execute("delete from pedidos where id =?",(str(id)))
    con.commit()
    return "pedido deletado com sucesso"
if __name__ == "__main__":
    uvicorn.run(app,port=5000)
    

