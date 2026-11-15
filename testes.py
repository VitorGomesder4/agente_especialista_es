from gerar_base_mecanica import gerar_base_mecanica as gerar_base

dados = gerar_base()

print(dados["temperatura_motor"][0], dados["nivel_oleo"][0], dados["estado_veiculo"][0])