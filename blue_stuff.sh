#!/usr/bin/expect -f

set controller  "5C:F3:70:89:E1:0E"
# 5C:F3:70:89:E1:0E
set device "F0:2F:74:63:3A:12"
set timeout 60

spawn bluetoothctl
expect "Agent registered"
send -- "list\r"
expect "$controller"
send -- "select $controller\r"
send -- "exit\r"
expect eof
