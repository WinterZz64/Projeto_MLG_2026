extends Area2D
var pode_colher = "nao"
var perto_milho = "nao"
# Called when the node enters the scene tree for the first time.
func _ready() -> void:
	Dados.semente -=1
	$AnimatedSprite2D.frame = 0
	await get_tree().create_timer(2.0).timeout
	$AnimatedSprite2D.frame = 1
	await get_tree().create_timer(2.0).timeout
	$AnimatedSprite2D.frame = 2
	await get_tree().create_timer(2.0).timeout
	$AnimatedSprite2D.frame = 3
	pode_colher = "sim"
# Called every frame. 'delta' is the elapsed time since the previous frame.
func _process(delta: float) -> void:
	if Input.is_action_just_pressed("colher") and pode_colher == "sim" and perto_milho == "sim":
		Dados.milho +=1
		queue_free()

func _on_body_entered(body: Node2D) -> void:
	perto_milho = "sim"

func _on_body_exited(body: Node2D) -> void:
	perto_milho = "nao"
