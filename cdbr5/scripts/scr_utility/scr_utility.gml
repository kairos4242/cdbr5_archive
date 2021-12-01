// Script assets have changed for v2.3.0 see
// https://help.yoyogames.com/hc/en-us/articles/360005277377 for more information
function pop_two_values(list){
	if ds_list_size(list) < 2 throw "Not enough values in list to pop two!"
	else {
		return [ds_list_pop(list), ds_list_pop(list)]
	}
}

function ds_list_pop(list) {
	//returns the first value and removes it from the list
	var value_temp = ds_list_find_value(list, 0)
	if is_undefined(value_temp) throw "Cannot pop from a list of size 0!"
	else {
		ds_list_delete(list, 0)
		return value_temp
	}
}

function ds_list_pop_refills(list, refill_list, random) {
	//pops from a list, if list is empty then refills it with values from refill list
	//if random is true, list is shuffled upon refill
	if ds_list_size(list) == 0
	{
		ds_list_copy(list, refill_list)
		if random == true ds_list_shuffle(list)
	}
	return ds_list_pop(list)
}

function difference_sign_margin(x1, x2, margin) {
	//returns the sign of x1 - x2, but if the difference is within the margin returns 0
	var diff = x1 - x2
	if abs(diff) < margin {
		return 0
	}
	else {
		return sign(diff)
	}
}