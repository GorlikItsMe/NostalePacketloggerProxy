# Nostale Packetlogger / Proxy in Python

In login_proxy.py or world_proxy.py  just edit 
`INPUT_IP`, `INPUT_PORT` and `OUTPUT_IP`, `OUTPUT_PORT`
if you want modify packets edit `after_send_func_handler` or `after_recv_func_handler` functions

By default in login_proxy.py in after_recv_func_handler is function what modify NsTeST packet and change channel ip to 127.0.0.1:4010. Soo you dont need change  `INPUT_IP`, `INPUT_PORT` in world_proxy.py


#requirements
```
pip install noscrypto
```

thanks for https://github.com/morsisko/NosCrypto
