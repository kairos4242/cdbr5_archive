/// @description Insert description here


//Singleton(kinda)
if instance_number(obj_Receiver) > 1 instance_destroy()
else
{
	global.receiver = id
}

//all the methods for every action one can take will go here

method(target, function receiver_move(target, x_change, y_change) {
	target.x += x_change
	target_y += y_change
})