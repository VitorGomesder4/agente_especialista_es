import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree
from sklearn.metrics import accuracy_score, confusion_matrix, ConfusionMatrixDisplay
from gerar_base_mecanica import gerar_base_mecanica as gerar_base

"""
logica/problema escolhido:
    Agente especialista mecanico

ENTRADAS X1 e X2 serão = temperatura do motor e nível do oleo

    X1:
        0-59 C: Motor frio                          Adicionara 1 pontos de atençao
        60-84 C: Motor temperatura normal           Adicionara 0 pontos de atençao
        85-99 C: Motor Temperatura elevada          Adicionara 1 ponto de atençao
        100-120 C: Motor Superaquecido              Adicionara 2 ponto de atençao

    X2:
        0-19% Nível Óleo: Muito baixo               Adicionara 2 ponto de atençao
        20%-39% Nível Óleo: Baixo                   Adicionara 1 ponto de atençao
        40%-100% Nível Óleo: Normal                 Adicionara 0 ponto de atençao

ROTULO y como estado final podera ser : Normal, Atenção, Problema e Problema critico:
    Ira ser usado para definir qual ação deve ser tomada/avisada


    A criação da base e seu estado final sera definido no contexto:

        RECOMENDAÇÕES:

            se Pontuação_de_atenção == 0 entao "Normal":
                Ação = "Veiculo Normal"

            se Pontuação_de_atenção == 1 entao "Atenção":
                Ação = "Atenção ao veículo cheque o nível do óleo e considere levar a um mecanico"

            se Pontuação_de_atenção == 2 entao "Problema":
                Ação = "O veículo possui um provavel problema, leve a um mecanico"

            se 2 < Pontuação_de_atenção entao "Problema critico":
                Ação = "O veículo possui um possivel problema critico leve a um mecanico"



"""

#Criação da base com a minha lógica
tamanho = 100000
data = gerar_base(tamanho=tamanho)

dados = pd.DataFrame(data=data)


X = dados[["temperatura_motor", "nivel_oleo"]]
y = dados["estado_veiculo"]


"""
print(dados["estado_veiculo"].value_counts())
    estado_veiculo
    Normal              10
    Atenção             10
    Problema            10
    Problema crítico    10
    Name: count, dtype: int64
"""


X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.25, random_state=42, stratify=y)

modelo_tree = DecisionTreeClassifier(max_depth=10, random_state=42)

modelo_tree.fit(X=X_treino, y=y_treino)

predict = modelo_tree.predict(X_teste)

print(f"Acurracy: {accuracy_score(y_teste, predict):.1%}")


classes = ["Normal", "Atenção", "Problema", "Problema crítico"]

matriz = confusion_matrix(y_teste, predict, labels=classes)

print(pd.DataFrame(matriz, index=classes, columns=classes))

"""
ConfusionMatrixDisplay(matriz, display_labels=classes).plot(cmap="Blues", colorbar=False)
plt.title(f"Confusion Matrix de base tamanho de entrada: {tamanho}")
plt.show()


plt.figure(figsize=(18, 15))
plot_tree(modelo_tree, feature_names=list(X.columns),
          class_names=list(modelo_tree.classes_), filled=True)
plt.show()
"""


novos_casos = [
    {"temperatura_motor": 60, "nivel_oleo": 40},     #Deve ser "normal"
    {"temperatura_motor": 40, "nivel_oleo": 50},     #Deve ser "Atenção"
    {"temperatura_motor": 120, "nivel_oleo": 1}]     #Deve ser "Problema crítico"

novos_casos = pd.DataFrame(novos_casos)

must_resultados = ["Normal", "Atenção", "Problema crítico"]

novos_casos_predict = modelo_tree.predict(novos_casos)

print(f"Previsões: {novos_casos_predict} == Must_Resultados: {must_resultados}")

print(f"Acurracy dos novos casos: {accuracy_score(must_resultados, novos_casos_predict):.1%}")


# Definição da Base de Conhecimento do sistema especialista
regras = [
    {
        "id": "R1",
        "estado": "Normal",
        "acao": "Veículo em condições normais de funcionamento."
    },
    {
        "id": "R2",
        "estado": "Atenção",
        "acao": "Recomenda-se verificar as condições do motor e realizar manutenção preventiva."
    },
    {
        "id": "R3",
        "estado": "Problema",
        "acao": "Recomenda-se realizar uma inspeção mecânica para identificar possíveis falhas."
    },
    {
        "id": "R4",
        "estado": "Problema crítico",
        "acao": "Interromper o uso do veículo e procurar assistência mecânica imediatamente."
    }
]


# Motor de Inferência
def aplicar_regras(estado):
    for regra in regras:

        # Verifica se existe uma regra correspondente ao estado previsto
        if regra["estado"] == estado:
            return {
                "estado_previsto": estado,
                "regra": regra["id"],
                "recomendacao": regra["acao"],
                "explicacao": (
                    f"O sistema classificou o veículo como: {estado}."
                )
            }

    raise ValueError("Nenhuma regra compatível com o estado previsto.")


# Integração do modelo de Machine Learning com o Sistema Especialista
def diagnosticar_veiculo(temperatura, nivel_oleo):

    # Validação dos dados de entrada
    if not 0 <= temperatura <= 120:
        raise ValueError("Temperatura deve estar entre 0 e 120 C.")

    if not 0 <= nivel_oleo <= 100:
        raise ValueError("Nível de óleo deve estar entre 0 e 100%.")

    # Criação do DataFrame para alimentar o modelo
    novo_caso = pd.DataFrame([{
        "temperatura_motor": temperatura,
        "nivel_oleo": nivel_oleo
    }])

    # 1. Classificação pelo modelo de Machine Learning
    estado = modelo_tree.predict(novo_caso)[0]

    # 2. Inferência utilizando a base de conhecimento
    resultado = aplicar_regras(estado)

    # 3. Verificação se os dados estão dentro dos intervalos de treinamento
    fora = any(
        not X_treino[c].min() <= novo_caso[c].iloc[0] <= X_treino[c].max()
        for c in X.columns
    )

    # Adição de um aviso sobre o resultado
    resultado["aviso"] = (
        "Entrada fora dos intervalos observados no treinamento."
        if fora else "Diagnóstico didático; recomenda-se avaliação mecânica."
    )

    return resultado


# Definição das variáveis de entrada para uma consulta simulada
temperatura = 60
nivel_oleo = 40

# Execução da consulta chamando a função integradora do sistema
resultado = diagnosticar_veiculo(temperatura, nivel_oleo)

# Exibição detalhada de cada atributo retornado pelo motor de inferência
for campo, valor in resultado.items():
    print(f"{campo}: {valor}")