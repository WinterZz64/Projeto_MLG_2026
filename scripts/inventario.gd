extends Area2D
var mochila_aberta = "nao"

# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	$local_inventario.hide()

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	pass

func _input(event: InputEvent) -> void:
	if Input.is_action_just_pressed("inventario"):
		$local_inventario.show()
		mochila_aberta = "sim"
