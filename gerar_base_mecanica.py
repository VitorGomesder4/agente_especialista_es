from random import randint

def gerar_base_mecanica(tamanho=100):
    #Tratando no caso de vir um valor pequeno ou muito grande
    if tamanho < 10 or tamanho > 100000:
        tamanho = 100


    data = {"temperatura_motor": [], "nivel_oleo": [], "estado_veiculo": []}

    for i in range(4):
        for j in range(tamanho):
            match i:
                #Caso normal
                case 0:
                    new_temperatura = randint(60, 84)
                    new_nivel_oleo = randint(40, 100)
                    new_estado = "Normal"

                    data["temperatura_motor"].append(new_temperatura)
                    data["nivel_oleo"].append(new_nivel_oleo)
                    data["estado_veiculo"].append(new_estado)

                case 1:
                    #Sorteando entre todas combinações possiveis para pontuação de atenção == 1
                    x = randint(0, 2)

                    if x == 0:
                        new_temperatura = randint(60, 84)
                        new_nivel_oleo = randint(20, 39)
                    elif x == 1:
                        new_temperatura = randint(0, 59)
                        new_nivel_oleo = randint(40, 100)
                    else:
                        new_temperatura = randint(85, 99)
                        new_nivel_oleo = randint(40, 100)

                    new_estado = "Atenção"

                    data["temperatura_motor"].append(new_temperatura)
                    data["nivel_oleo"].append(new_nivel_oleo)
                    data["estado_veiculo"].append(new_estado)

                case 2:
                    #Sorteando entre todas combinações possiveis para pontuação de atenção == 2
                    x = randint(0, 3)

                    if x == 0:
                        new_temperatura = randint(100, 120)
                        new_nivel_oleo = randint(40, 100)
                    elif x == 1:
                        new_temperatura = randint(0, 59)
                        new_nivel_oleo = randint(20, 39)
                    elif x == 2:
                        new_temperatura = randint(85, 99)
                        new_nivel_oleo = randint(20, 39)
                    else:
                        new_temperatura = randint(60, 84)
                        new_nivel_oleo = randint(0, 19)

                    new_estado = "Problema"

                    data["temperatura_motor"].append(new_temperatura)
                    data["nivel_oleo"].append(new_nivel_oleo)
                    data["estado_veiculo"].append(new_estado)

                case 3:
                    #Sorteando entre todas combinações possiveis para pontuação de atenção > 2
                    x = randint(0, 3)

                    if x == 0:
                        new_temperatura = randint(100, 120)
                        new_nivel_oleo = randint(20, 39)

                    elif x == 1:
                        new_temperatura = randint(100, 120)
                        new_nivel_oleo = randint(0, 19)

                    elif x == 2:
                        new_temperatura = randint(0, 59)
                        new_nivel_oleo = randint(0, 19)

                    else:
                        new_temperatura = randint(85, 99)
                        new_nivel_oleo = randint(0, 19)

                    new_estado = "Problema crítico"

                    data["temperatura_motor"].append(new_temperatura)
                    data["nivel_oleo"].append(new_nivel_oleo)
                    data["estado_veiculo"].append(new_estado)

    return(data)