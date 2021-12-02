// Async Networking Event
var nEvent = ds_map_find_value(async_load, "type");
switch (nEvent) {
    case network_type_connect:
        var socket = ds_map_find_value(async_load, "socket");
        var ip = ds_map_find_value(async_load, "ip");
        ds_list_add(socket_list, socket);
        show_debug_message("Client connected! "+ip);
    break;
    case network_type_disconnect:
        var socket = ds_map_find_value(async_load, "socket");
        var findSocket = ds_list_find_index(socket_list, socket);
        var ip = ds_map_find_value(async_load, "ip");
        if (findSocket >= 0) {
            ds_list_delete(socket_list, findSocket);
        }
        show_debug_message("Client disconnected! "+ip);
    break;
    case network_type_data:
        var buffer = ds_map_find_value(async_load, "buffer");
        var socket = ds_map_find_value(async_load,"id");
        var ip = ds_map_find_value(async_load, "ip");
        show_debug_message("Got packet from "+ip);
        buffer_seek(buffer, buffer_seek_start, 0);
        var msgid = buffer_read(buffer, buffer_u8);
        switch (msgid) {
            case 50:
                var data = buffer_read(buffer,buffer_u16);
                show_debug_message("Data: "+string(data));
				
				switch data {
					default: break;
					case 0: player_1.x += 25
					break;
					case 1: player_1.y -= 25
					break;
					case 2: player_1.x -= 25
					break;
					case 3: player_1.y += 25
					break;//set up like this cause 0 is right, 90 up, 180 left, 270 down
					case 65534:
					//this the agent's signal for no action, just a request for game state
					//happens when the agent first starts and needs an initial state
					break;
					case 65535:
					//this is the signal for a reset
					room_restart()
					break;
				}
				player_1.x = clamp(player_1.x,0, room_width)
				player_1.y = clamp(player_1.y, 0, room_height)
				
				buffer_seek(write_buffer, buffer_seek_start, 0)
				with player_1 {
					if place_meeting(x, y, other.rewards[0]) {
						show_debug_message("Sending off a success")
						with other {
							buffer_write(write_buffer, buffer_string, string("0,0\n"))
						}
					}
					else {
						show_debug_message("Sending off distance to reward")
						with other {
							var xdir = difference_sign_margin(rewards[0].x, player_1.x, player_1.sprite_height / 2)//1 if to the right, -1 if to the left
							var ydir = difference_sign_margin(player_1.y, rewards[0].y, player_1.sprite_height / 2)//1 if upward, -1 if downward
							show_debug_message("Xdir: " + string(xdir))
							show_debug_message("Ydir: " + string(ydir))
							buffer_write(write_buffer, buffer_string, string(xdir) + "," + string(ydir) + "\n")
							//show_debug_message("Buffer size: " + string(buffer_get_size(write_buffer)))
						}
					}
				}
				network_send_packet(socket, write_buffer, buffer_get_size(write_buffer))
            break;
        }
    break;
}