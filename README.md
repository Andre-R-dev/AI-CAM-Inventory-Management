# AI-CAM-Inventory-Management

Programas necessários para a utilização do Kinect V2:\
Instalar Kinect SDK 2.0, Kinect Runtime 2.2 e Kinect ToolKit 1.8.\
Para alimentar o Kinect é necessário uma porta USB 3.0.\

# Ficheiros que necessitam de estar na pasta de execução do programa
- Inventario_2021\
- quadrado_vazio (imagem default)\

# Iteração com o programa
## Alterar a câmera
O programa vai sempre tentar conetar-se a uma das câmeras disponíveis. Caso queira alterar a câmera deve ser inserido um valor inteiro, normalmente 0 ou 1 (depende do número de câmeras conectadas). De seguida deve pressionar o botão "Carregar Câmera". 

## Carregar o Modelo TensorFlow
Quando o programa está a correr e não queremos usar só a procura por texto, é necessário carregar o modelo de IA. Para tal, deve ser colocado o diretório da pasta que contem o modelo TensorFlow criado no software LOBE e pressionar o botão "Carregar Modelo".

## Deteção do objeto via câmera
Depois do modelo carregado, para detetar o objeto com recurso à câmera do computador basta pressionar o botão "Deteção de objeto".

## A Procura Manual não requer qualquer um dos passos anteriormente descritos

## As imagens vêm diretamente de um diretório no Excel. Este diretório pode ser alterado diretamente.
