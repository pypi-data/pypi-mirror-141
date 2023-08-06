from skimage.io import imread, imsave

def ler_imagem(caminho, cinza = False):
    imagem = imread(caminho, as_gray = cinza)
    return imagem

def salvar_imagem(imagem, caminho):
    imsave(caminho, imagem) 