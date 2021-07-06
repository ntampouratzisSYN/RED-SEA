
# default: on 
# descr and ption: The rshd server is the server for the rcmd(3) routine and, \ 
#    consequently, for the rsh(1) program. The server provides \ 
#    remote execution facilities with authentication based on \ 
#    privileged port numbers from trusted hosts. 
service shell 
{ 
    disable = no 
    socket_type       = stream 
    wait          = no 
    user          = root 
    log_on_success     += USERID 
    log_on_failure     += USERID 
    server         = /usr/sbin/in.rshd 
} 
 
/etc/xinetd.d/rlogin 
 
# default: on 
# descr and ption: rlogind is the server for the rlogin(1) program. The server \ 
#    provides a remote login facility with authentication based on \ 
#    privileged port numbers from trusted hosts. 
service login 
{ 
    disable = no 
    socket_type       = stream 
    wait          = no 
    user          = root 
    log_on_success     += USERID 
    log_on_failure     += USERID 
    server         = /usr/sbin/in.rlogind 
} 
 
/etc/xinetd.d/rexec 
 
# default: off 
# descr and ption: Rexecd is the server for the rexec(3) routine. The server \ 
#    provides remote execution facilities with authentication based \ 
#    on user names and passwords. 
service exec 
{ 
    disable = no 
    socket_type       = stream 
    wait          = no 
    user          = root 
    log_on_success     += USERID 
    log_on_failure     += USERID 
    server         = /usr/sbin/in.rexecd 
} 
