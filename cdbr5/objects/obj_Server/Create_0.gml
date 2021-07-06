// Create Event
server = network_create_server_raw(network_socket_tcp, 8008, 10);
sBuffer = buffer_create(1024,buffer_fixed,1);
write_buffer = buffer_create(1024, buffer_fixed, 1)
socket_list = ds_list_create()

//game variables
rewards = []
player_1 = -1
player_2 = -1