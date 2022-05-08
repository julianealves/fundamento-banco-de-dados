"""
Aplicativo de leitura
Juliane Alves e Gustavo Noll
"""
import getpass
import psycopg2
import queries


if __name__ == "__main__":
    senha = getpass.getpass(prompt="Senha database: ")

    try:
        con = psycopg2.connect(host="localhost", database="postgres", user="postgres", password=senha)
    except:
        print("Falha ao conectar com o database")
        exit(-1)

    cur = con.cursor()
    visao = queries.set_visao()
    cur.execute(visao)

    print("***** Bem-Vindo(a) ao Aplicativo de leitura! *****")
    sair = False
    while not sair:
        print("Menu: ")
        print("1 - Procurar por um autor em uma determinada categoria")
        print("2 - Editora(s) que vendeu mais livros em um determinado periodo")
        print("3 - Livros que nunca foram comprados")
        print("4 - Gasto total de todos os usuarios")
        print("5 - Livro(s) mais vendido")
        print("6 - Usuarios que acessaram o app mais de 2 vezes e quais dispositivos utilizados pelos mesmos")
        print("7 - Retornar a porcentagem de leitura de todos os livros de um determinado usuario")
        print("8 - Retornar autores que possuem a mesma agencia bancaria")
        print("9 - Retornar lista de leitores e seus respectivos planos")
        print("10 - Retornar uso dos dispositivos")
        print("11 - Sair")

        menu = int(input())

        if menu == 1:
            print("Nome do autor:")
            autor = input()
            print("Categoria:")
            categoria = input()
            cur.execute(queries.get_autor_categoria(autor=autor, categoria=categoria))
            con.commit()
            recset = cur.fetchall()
            for rec in recset:
                print(rec)
        elif menu == 2:
            print("Periodo inicial (formato: yyyy-mm-dd): ")
            data_inicial = input()
            print("Periodo final (formato: yyyy-mm-dd): ")
            data_final = input()
            visao = queries.set_visao_editora_que_vendeu_mais_livros(data_inicial=data_inicial, data_final=data_final)
            cur.execute(visao)
            resp = queries.get_editora_que_mais_vendeu_livros()
            cur.execute(resp)
            con.commit()
            recset = cur.fetchall()
            for rec in recset:
                print(rec)
        elif menu == 3:
            resp = queries.get_livros_nao_comprados()
            cur.execute(resp)
            con.commit()
            recset = cur.fetchall()
            for rec in recset:
                print(rec)
        elif menu == 4:
            resp = queries.get_gasto_usuarios()
            cur.execute(resp)
            con.commit()
            recset = cur.fetchall()
            for rec in recset:
                print(rec)
        elif menu == 5:
            visao = queries.set_visao_livro_mais_vendido()
            cur.execute(visao)
            resp = queries.get_livro_mais_vendido()
            cur.execute(resp)
            con.commit()
            recset = cur.fetchall()
            for rec in recset:
                print(rec)
        elif menu == 6:
            visao = queries.set_visao_acesso_usuarios_e_dispositivos()
            cur.execute(visao)
            resp = queries.get_acesso_usuarios_e_dispositivos()
            cur.execute(resp)
            con.commit()
            recset = cur.fetchall()
            for rec in recset:
                print(rec)
        elif menu == 7:
            print("Nome do leitor:")
            leitor = input()
            resp = queries.get_porcentagem_de_leitura(leitor=leitor)
            cur.execute(resp)
            con.commit()
            recset = cur.fetchall()
            for rec in recset:
                print(rec)
        elif menu == 8:
            resp = queries.get_autores_com_mesma_agencia_bancaria()
            cur.execute(resp)
            con.commit()
            recset = cur.fetchall()
            for rec in recset:
                print(rec)
        elif menu == 9:
            resp = queries.get_leitores_e_planos()
            cur.execute(resp)
            con.commit()
            recset = cur.fetchall()
            for rec in recset:
                print(rec)
        elif menu == 10:
            resp = queries.get_uso_dispositivos()
            cur.execute(resp)
            con.commit()
            recset = cur.fetchall()
            for rec in recset:
                print(rec)
        elif menu == 11:
            sair = True

    con.close()
