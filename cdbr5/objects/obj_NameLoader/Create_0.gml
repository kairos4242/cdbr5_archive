//Load Names from file

name_file = file_text_open_read(working_directory + "nounlist.txt")
name_list = ds_list_create()
while !file_text_eof(name_file) {
	curr_name = file_text_read_string(name_file)
	file_text_readln(name_file)//This should mean the resulting string avoids the newline
	ds_list_add(name_list, curr_name)
	show_debug_message("Adding name: " + curr_name)
}
file_text_close(name_file)
show_debug_message("shuffling name list...")
ds_list_shuffle(name_list)

method(id, function get_name(i) {
	return ds_list_find_value(name_list, i)
})
show_debug_message("Arriveth end of nameloader")