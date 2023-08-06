import numpy as np
from skimage.color import rgb2gray
from skimage.exposure import match_histograms
from skimage.metrics import structural_similarity

def procurar_diferenciacao(imagem1, imagem2):
    assert imagem1.shape == imagem2.shape, "Especifique 2 imagens com a mesma forma."
    cinza1 = rgb2gray(imagem1)
    cinza2 = rgb2gray(imagem2)
    (score, diferenca_imagem) = structural_similarity(cinza1, cinza2, full=True)
    print("Semelhança das imagens:", score)
    imagem = (diferenca_imagem-np.min(diferenca_imagem))/(np.max(diferenca_imagem)-np.min(diferenca_imagem))
    return imagem

def transferir_histograma(imagem1, imagem2):
    imagem = match_histograms(imagem1, imagem2, multichannel=True)
    return imagem