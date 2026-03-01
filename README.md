script de automação para a ferramenta x64dbg
com interface grafica em html com layout simples
para alteração do dev/sec

intuito do script e trazer informação
organização e a comunicação automatizada
entre a arquitetura e os breakpoints

FEITA C++ COM INTEGRAÇÃO EM PYTHON


✔ Objetivo do sistema
✔ Arquitetura
✔ Comunicação com x64dbg
✔ Automação de breakpoints
✔ Coleta de registradores/memória
✔ Pipeline de análise
✔ Tecnologias
✔ Execução


Este projeto implementa uma camada de automação para o depurador x64dbg (xdbg64), permitindo a execução controlada de breakpoints, leitura de registradores e inspeção de memória através de uma API em Python integrada a um módulo nativo em C++

O script x64dbg.py injeta comandos no depurador através da API do plugin, capturando estados de execução e exportando os resultados via socket para o servidor
