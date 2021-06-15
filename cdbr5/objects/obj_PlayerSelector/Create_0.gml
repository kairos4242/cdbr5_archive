/// @description Insert description here
// You can write your code in this editor
method(id, function create(list) {
	player_list = list
	round_list = ds_list_create()
	ds_list_copy(round_list, player_list)
})

method(id, function get_player() {
	return ds_list_pop_refills(round_list, player_list, true)
})