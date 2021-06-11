//Load Player Files from Directory

var player_path = working_directory + "\Player Files"
player_list = ds_list_create()

//Validate Directory
if directory_exists(player_path)
{
	show_debug_message("Directory Exists")
	
}
else
{
	directory_create(player_path)
	show_debug_message("Creating directory...")
}

//Load names
name_loader = instance_create_depth(0, 0, 0, obj_NameLoader)

show_debug_message("Arriveth back in playerloader")

//Load players
if file_find_first(player_path + "/*.json", 0) == ""
{
	show_debug_message("No players exist, creating some...")
	for (i = 0; i < 10; i++)
	{
		new_player = {
			hp: irandom(50) + 50,
			name: name_loader.get_name(i)
		}
		player_file = file_text_open_write(player_path + "/Player" + string(i) + ".json")
		file_text_write_string(player_file, json_stringify(new_player))
		file_text_close(player_file)
	}
}
else
{
	show_debug_message("Now loading players")
	player_file_name = file_find_first(player_path + "/*.json", 0)
	show_debug_message("Player file name: " + player_file_name)
	while player_file_name != ""
	{
		player_file = file_text_open_read(player_path + "/" + player_file_name)
		player_string = file_text_read_string(player_file)
		show_debug_message("Player String: " + player_string)
		ds_list_add(player_list, json_parse(player_string))
		file_text_close(player_file)
		player_file_name = file_find_next()
	}
}