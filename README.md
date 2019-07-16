# merge-haproxy-stats


### Descrição

Programa utilizado para fazer o merge das estatísticas que são geradas individualmente por processador utilizado (nbproc > 1).  
Gerando um unix socket similar ao gerado pelo haproxy, com as estatísticas unidas.

### Defaults


* Diretório dos sockets:  `/var/run/haproxy/`
* Nome do socket mesclado:  `/var/run/haproxy/info.sock`
* Sockets do haproxy:       `/var/run/haproxy/hastat-proc*.sock`

### Funcionamento

Para a execução o arquivo *merge_config.json* deve estar no mesmo diretório do arquivo *haproxy_sock_stats.py*

 - iniciar o programa: 
   - `nohup haproxy_sock_stats.py &`
 - Ver o csv mesclado: (a requisição e a resposta seguem o mesmo padrão dos sockets gerado pelo haproxy)
   - `echo "show stat" | socat /var/run/haproxy/info.sock stdio`