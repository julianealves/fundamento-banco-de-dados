
def set_visao() -> str:
    return f"""
    CREATE OR REPLACE VIEW livros_loja AS
    SELECT Titulo, fk_Categoria_Nome_Categoria AS Categoria, fk_Editora_Nome AS Editora, Usuario.Nome AS Autor, Data_publicacao
    FROM Livro 
    INNER JOIN Escreve ON Escreve.fk_Livro_ASIN = Livro.ASIN 
    INNER JOIN Usuario ON Escreve.fk_Autor_fk_Usuario_CPF = Usuario.CPF
    LEFT JOIN Assunto ON Assunto.fk_Livro_ASIN = Livro.ASIN;
    """


def get_visao() -> str:
    return f"SELECT * FROM livros_loja;"


def get_autor_categoria(autor: str, categoria: str) -> str:
    return f"""
    SELECT * FROM livros_loja
    WHERE Categoria = '{categoria}' AND Autor = '{autor}';
    """


def set_visao_editora_que_vendeu_mais_livros(data_inicial: str, data_final: str) -> str:
    return f"""
    CREATE OR REPLACE VIEW editoras_beetwen_periodo AS (
    SELECT Editora, COUNT(DISTINCT Titulo) AS Livros_vendidos
    FROM livros_loja
    WHERE Data_publicacao >= '{data_inicial}'::date AND Data_publicacao <= '{data_final}'::date
    GROUP BY Editora
    ORDER BY COUNT(DISTINCT Titulo) DESC
    );
    """


def get_editora_que_mais_vendeu_livros() -> str:
    return f"""
    SELECT Editora AS editora_com_mais_livros_entre_periodo, Livros_vendidos
    FROM editoras_beetwen_periodo
    WHERE Livros_vendidos = (SELECT MAX(Livros_vendidos) FROM editoras_beetwen_periodo);
    """


def get_livros_nao_comprados() -> str:
    return f"""
    SELECT Titulo AS Livros_nao_comprados FROM Livro
    WHERE NOT EXISTS(SELECT * FROM Compra
    WHERE Asin = Compra.fk_Livro_ASIN);
    """


def get_gasto_usuarios() -> str:
    return f"""
    SELECT Nome, SUM(total) AS Total
    FROM Compra
    INNER JOIN usuario ON fk_Leitor_fk_Usuario_CPF = usuario.CPF
    GROUP BY Nome
    ORDER BY SUM(total) DESC;
    """


def set_visao_livro_mais_vendido() -> str:
    return f"""
    CREATE OR REPLACE VIEW Venda_livros AS (
    SELECT Titulo, COUNT(Titulo) AS Vendas
    FROM Compra INNER JOIN Livro ON fk_Livro_ASIN=Livro.Asin
    GROUP BY Titulo
    ORDER BY COUNT(Titulo) DESC
    );
    """


def get_livro_mais_vendido() -> str:
    return f"SELECT Titulo, Vendas FROM Venda_livros WHERE Vendas = (SELECT MAX(Vendas) FROM Venda_livros);"


def set_visao_acesso_usuarios_e_dispositivos() -> str:
    return f"""
    CREATE OR REPLACE VIEW Acessos_app AS (
    SELECT Nome, COUNT(Data) AS total_acessos 
    FROM Utiliza 
    INNER JOIN Usuario ON Utiliza.fk_Leitor_fk_Usuario_CPF = Usuario.CPF
    GROUP BY Nome
    HAVING COUNT(DISTINCT Data) > 2);
    """


def get_acesso_usuarios_e_dispositivos() -> str:
    return f"""
    SELECT Nome, fK_Dispositivo_Tipo, COUNT(Data)
    FROM Utiliza 
    INNER JOIN Usuario ON Utiliza.fk_Leitor_fk_Usuario_CPF = Usuario.CPF
    WHERE Nome in (SELECT Nome FROM Acessos_app)
    GROUP BY Nome, fK_Dispositivo_Tipo;
    """


def get_porcentagem_de_leitura(leitor: str) -> str:
    return f"""
    SELECT Nome, Titulo, Porcentagem_Leitura
    FROM Le
    INNER JOIN Usuario ON Le.fk_Leitor_fk_Usuario_CPF = Usuario.CPF
    INNER JOIN Livro ON Livro.ASIN = Le.fk_Livro_ASIN
    WHERE Nome  = '{leitor}';
    """


def get_autores_com_mesma_agencia_bancaria() -> str:
    return f"""
    SELECT Nome, fk_Numero_Agencia
    FROM Usuario
    INNER JOIN Autor ON Autor.fk_Usuario_CPF = CPF
    WHERE fk_Numero_Agencia in (SELECT fk_Numero_Agencia
    FROM (
    SELECT fk_Numero_Agencia, COUNT(DISTINCT fk_Usuario_CPF) AS Qtd_autores
    FROM Autor as t1
    GROUP BY fk_Numero_Agencia
    ) as t2 WHERE Qtd_autores > 1
    );
    """


def get_leitores_e_planos() -> str:
    return f"""
    SELECT Nome, fk_Plano_Tipo
    FROM Leitor
    INNER JOIN Usuario ON Usuario.CPF = Leitor.fk_Usuario_CPF;
    """


def get_uso_dispositivos() -> str:
    return f"""
    SELECT fK_Dispositivo_Tipo, COUNT(*) AS Total_uso
    FROM Utiliza
    GROUP BY fK_Dispositivo_Tipo
    ORDER BY Total_uso DESC;
    """
