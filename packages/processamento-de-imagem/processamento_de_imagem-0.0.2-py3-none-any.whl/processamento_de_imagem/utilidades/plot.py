import matplotlib.pyplot as plt

def plot_imagem(imagem):
    plt.figure(figsize=(12, 4))
    plt.imshow(imagem, cmap='gray')
    plt.axis('off')
    plt.show()

def plot_resultado(*args):
    imagens = len(args)
    fig, axis = plt.subplots(nrows=1, ncols = imagens, figsize=(12, 4))
    nomes = ['imagem {}'.format(i) for i in range(1, imagens)]
    nomes.append('Resultado')
    for ax, nome, imagem in zip(axis, nomes, args):
        ax.set_title(nome)
        ax.imshow(imagem, cmap='gray')
        ax.axis('off')
    fig.tight_layout()
    plt.show()

def plot_histograma(imagem):
    fig, axis = plt.subplots(nrows=1, ncols = 3, figsize=(12, 4), sharex=True, sharey=True)
    color_lst = ['vermelho', 'verde', 'azul']
    for index, (ax, color) in enumerate(zip(axis, color_lst)):
        ax.set_title('{} histograma'.format(color.title()))
        ax.hist(imagem[:, :, index].ravel(), bins = 256, color = color, alpha = 0.8)
    fig.tight_layout()
    plt.show()