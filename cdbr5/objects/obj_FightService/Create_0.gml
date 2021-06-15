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

for (i = 0; i < 20; i++)
{
	//for testing purposes
	show_debug_message("Player selected: " + string(player_selector.get_player()))
}