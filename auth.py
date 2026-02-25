from db import conectar
import hashlib

def hash_senha(senha):
    return hashlib.sha256(senha.encode()).hexdigest()

def registrar_usuario(username, senha):
    conn = conectar()
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO usuarios (username, senha) VALUES (?, ?)",
            (username, hash_senha(senha))
        )
        conn.commit()
        conn.close()
        return True
    except:
        conn.close()
        return False

def autenticar(username, senha):
    conn = conectar()
    cursor = conn.cursor()

    cursor.execute(
        "SELECT * FROM usuarios WHERE username = ? AND senha = ?",
        (username, hash_senha(senha))
    )

    user = cursor.fetchone()
    conn.close()

    return user is not None