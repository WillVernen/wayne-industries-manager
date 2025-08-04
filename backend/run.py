# backend/run.py
"""
Este é o script principal para executar a aplicação Flask.
Ele importa a função 'create_app' da nossa pasta 'app' e a executa.
"""

from app import create_app

# Cria a aplicação chamando nossa fábrica.
app = create_app()

if __name__ == '__main__':
    # Executa o servidor de desenvolvimento do Flask.
    # debug=True: ativa o modo de depuração, que reinicia o servidor
    #             automaticamente a cada alteração no código e mostra
    #             erros detalhados no navegador.
    # host='0.0.0.0': torna o servidor acessível por outros dispositivos na mesma rede.
    app.run(host='0.0.0.0', port=5000, debug=True)
