extends CharacterBody2D

const speed = 600
var current_dir = "none"
var pode_vender = "nao"

func _ready():
	$AnimatedSprite2D.play("idle_front")

func _physics_process(delta: float) -> void:	
	player_movement(delta)
	
@warning_ignore("unused_parameter")
func player_movement(delta):
	
	if Input.is_action_pressed("ui_right"):
		current_dir = "right"
		play_anim(1)
		velocity.x = speed
		velocity.y = 0
	elif Input.is_action_pressed("ui_left"):
		current_dir = "left"
		play_anim(1)
		velocity.x = -speed
		velocity.y = 0
	elif Input.is_action_pressed("ui_down"):
		current_dir = "down"
		play_anim(1)
		velocity.y = speed
		velocity.x = 0
	elif Input.is_action_pressed("ui_up"):
		current_dir = "up"
		play_anim(1)
		velocity.y = -speed
		velocity.x = 0
	else:
		play_anim(0)
		velocity.x = 0
		velocity.y = 0
		
	move_and_slide()

func play_anim(movement):
	var dir = current_dir
	var anim = $AnimatedSprite2D
	
	if dir == "right":
		anim.flip_h = true
		if movement == 1:
			anim.play("walk_side")
		elif movement == 0:
			anim.play("idle_side")
	if dir == "left":
		anim.flip_h = false
		if movement == 1:
			anim.play("walk_side")
		elif movement == 0:
			anim.play("idle_side")
			
	if dir == "up":
		anim.flip_h = false
		if movement == 1:
			anim.play("walk_back")
		elif movement == 0:
			anim.play("idle_back")
	if dir == "down":
		anim.flip_h = false
		if movement == 1:
			anim.play("walk_front")
		elif movement == 0:
			anim.play("idle_front")

	if Input.is_action_just_pressed("ui_accept") and Dados.milho >=1 and pode_vender=="sim":
		Dados.milho -=1 
		Dados.dinheiro += 5
		
func _on_sementes_body_entered(body: Node2D) -> void:
	Dados.semente +=1

func _on_gato_body_entered(body: Node2D) -> void:
	$"../dialogo_gato".show()
	$"../dialogo_gato".text = str("miau")
	#$"../dialogo_gato/AnimationPlayer"

func _on_gato_body_exited(body: Node2D) -> void:
	$"../dialogo_gato".hide()


func _on_npc_shop_body_entered(body: Node2D) -> void:
	pode_vender = "sim"
	
func _on_npc_shop_body_exited(body: Node2D) -> void:
	pode_vender = "nao"

func _on_ir_planatcao_body_entered(body: Node2D) -> void:
	get_tree().change_scene_to_file.bind("res://scenes/plantacao.tscn").call_deferred()

func _on_ir_inicio_body_entered(body: Node2D) -> void:
	get_tree().change_scene_to_file.bind("res://scenes/inicio.tscn").call_deferred()

func _on_ir_inimigo_body_entered(body: Node2D) -> void:
	get_tree().change_scene_to_file.bind("res://scenes/inimigo.tscn").call_deferred()

func _on_ir_planatcao_saida_body_entered(body: Node2D) -> void:
	get_tree().change_scene_to_file.bind("res://scenes/plantacao.tscn").call_deferred()
