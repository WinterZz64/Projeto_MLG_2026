extends Node2D
var plantar_milho = preload("res://scripts/milho.gd")


func _ready() -> void:
	pass

# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	if Input.is_action_just_pressed(" plantar_milho") and Dados.semente >=1:
		var instance = plantar_milho.instantiate()
		instance.position = $player2.position
		add_child(instance)
