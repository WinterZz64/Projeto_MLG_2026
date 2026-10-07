extends Area2D
var semente = Dados.semente
var plantar = "nao"
var terra = "nao"
var ja_tem_planta = "nao"

func _ready() -> void:
	
	
	hide()
	
	

func _process(delta: float) -> void:
	$"../segurar_informacoes/seementes_tomate".text = str("sementes de tomate = ", Dados.semente)
	
	if terra == "sim" and ja_tem_planta == "nao":
		if Dados.semente >=1 and Input.is_action_just_pressed("plantar_tomate"):
			show()
			ja_tem_planta = "sim"
			Dados.semente -=1
			$AnimatedSprite2D.frame = 0
			await get_tree().create_timer(2.0).timeout
			$AnimatedSprite2D.frame = 1
			await get_tree().create_timer(2.0).timeout
			$AnimatedSprite2D.frame = 2
			await get_tree().create_timer(2.0).timeout
			$AnimatedSprite2D.frame = 3
			ja_tem_planta = "nao"
		
func _on_body_entered(body: Node2D) -> void:
	terra = "sim"

func _on_body_exited(body: Node2D) -> void:
	terra = "nao"
