import torch; torch.manual_seed(0)
import torch.nn as nn
import torch.nn.functional as F
import torch.utils
import torch.distributions
import torchvision
import numpy as np
from tqdm import tqdm
import matplotlib.pyplot as plt

from autoencoder_torch import Decoder


if torch.cuda.is_available():
    device = 'cuda'
elif torch.backends.mps.is_available():
    device = 'mps'
else:
    device = 'cpu'

print(f'Using device: {device}')

class VariationalEncoder(nn.Module):
    def __init__(self, latent_dims):
        super(VariationalEncoder, self).__init__()
        self.linear1 = nn.Linear(784, 512)
        self.linear2 = nn.Linear(512, latent_dims)
        self.linear3 = nn.Linear(512, latent_dims)

        self.N = torch.distributions.Normal(0, 1)
        self.N.loc = self.N.loc.to(device)
        self.N.scale = self.N.scale.to(device)
        self.kl = 0

    def forward(self, x):
        x = torch.flatten(x, start_dim=1)
        x = F.relu(self.linear1(x))
        mu =  self.linear2(x)
        sigma = torch.exp(self.linear3(x))
        z = mu + sigma*self.N.sample(mu.shape)
        self.kl = (sigma**2 + mu**2 - torch.log(sigma) - 1/2).sum()
        return z

class VariationalAutoencoder(nn.Module):
    def __init__(self, latent_dims):
        super(VariationalAutoencoder, self).__init__()
        self.encoder = VariationalEncoder(latent_dims)
        self.decoder = Decoder(latent_dims)

    def forward(self, x):
        z = self.encoder(x)
        return self.decoder(z)

def train(autoencoder, data, epochs=20):
    opt = torch.optim.Adam(autoencoder.parameters())
    for epoch in tqdm(range(epochs)):
        for x, y in data:
            x = x.to(device) # GPU
            opt.zero_grad()
            x_hat = autoencoder(x)
            loss = ((x - x_hat)**2).sum() + autoencoder.encoder.kl
            loss.backward()
            opt.step()
    return autoencoder

if __name__ == "__main__":

    latent_dims = 2
    vae = VariationalAutoencoder(latent_dims).to(device) # GPU

    data = torch.utils.data.DataLoader(
            torchvision.datasets.MNIST('./data',
                transform=torchvision.transforms.ToTensor(),
                download=True),
            batch_size=128,
            shuffle=True)

    vae = train(vae, data)

    num_batches=100
    fig, ax = plt.subplots()
    for i, (x, y) in enumerate(data):
        z = vae.encoder(x.to(device))
        z = z.to('cpu').detach().numpy()
        ax.scatter(z[:, 0], z[:, 1], c=y, cmap='tab10')
        if i > num_batches:
            colorbar = plt.colorbar(ax.collections[0], ax=ax)
            break

    fig.tight_layout()

    plt.show()

    #fig.savefig('../../assets/figures/07-summary/vae_latent_space.svg')