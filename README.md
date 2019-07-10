# merge-haproxy-stats

Programa utilizado para fazer o merge das estatísticas que são geradas individualmente por processador utilizado (nbproc > 1).  
Gerando um unix socket similar ao gerado pelo haproxy, com as estatísticas unidas. Para que a monitoração do zabbix possa funcionar corretamente com o template.
