/// @description Insert description here
// You can write your code in this editor

//Randomness


//Load Players
player_loader = instance_create_depth(0, 0, 0, obj_PlayerLoader)
player_list = ds_list_create()
ds_list_copy(player_list,player_loader.player_list)
instance_destroy(player_loader)

//Select Two Players
ds_list_shuffle(player_list)

player_selector = instance_create_depth(0, 0, 0, obj_PlayerSelector)
player_selector.create(player_list)//workaround because constructors only for objects atm


method(id, function start_fight() {
	player_1_struct = player_selector.get_player()
	player_2_struct = player_selector.get_player()

	player_1 = instance_create_depth((room_width / 2) - 150, room_height / 2, 0, obj_Player)
	player_2 = instance_create_depth((room_width / 2) + 150, room_height / 2, 0, obj_Player)
	player_1.create(player_1_struct)
	player_2.create(player_2_struct)
})

method(id, function end_fight() {
	instance_destroy(player_1)
	instance_destroy(player_2)
	start_fight()
})

start_fight()