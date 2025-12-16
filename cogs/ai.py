from typing import Sequence
import discord
from discord.ext import commands
from discord import app_commands
import torch
from torch._higher_order_ops import wrap_activation_checkpoint
import torch.nn as nn


class Brain(nn.Module):
    def __init__(self, embed_dim=16, num_classes=3, max_vocab=1000) -> None:
        super().__init__()
        self.vocab = {"<pad>": 0, "<unk>": 1}

        self.max_vocab = max_vocab
        self.embed_dim = embed_dim
        self.embedding = nn.Embedding(max_vocab, embed_dim)
        self.fc = nn.Linear(embed_dim, num_classes)

        self.vocab_frozen = True

    def tokenize(self, text: str):
        words = text.lower().split()
        ids = []

        for word in words:
            ids.append(self.vocab.get(word, self.vocab["<unk>"]))
        return ids

    def forward(self, token_idx):
        x = self.embedding(token_idx)
        x = x.mean(dim=1)
        return self.fc(x)

    def predict(self, text: str):
        token_idx = self.tokenize(text)

        if not token_idx:
            return None

        tensor = torch.tensor([token_idx])
        with torch.no_grad():
            logits = self.forward(tensor)

            return torch.argmax(logits, dim=1).item()

    def save(self, path):
        torch.save({"state": self.state_dict(), "vocab": self.vocab}, path)

    def load(self, path):
        data = torch.load(path, map_location="cpu")
        self.load_state_dict(data["state"])
        self.vocab = data["vocab"]

    def train_model(self, data, class_to_idx, epoch=100, lr=0.01):
        optimizer = torch.optim.Adam(self.parameters(), lr=lr)
        criterion = nn.CrossEntropyLoss()
        self.train()

        x = []
        y = []
        for sentence, word in data:
            token_idx = self.tokenize(sentence)
            if token_idx:
                x.append(token_idx)
                y.append(class_to_idx[word])

        max_len = max(len(sequence) for sequence in x)
        x_padded = [
            sequence + [self.vocab["<pad>"]] * (max_len - len(sequence))
            for sequence in x
        ]
        x_tensor = torch.tensor(x_padded, dtype=torch.long)
        y_tensor = torch.tensor(y, dtype=torch.long)

        for epoch in range(epoch):
            optimizer.zero_grad()
            outputs = self.forward(x_tensor)
            loss = criterion(outputs, y_tensor)
            loss.backward()
            optimizer.step()

        self.eval()


class AI(commands.Cog):
    def __init__(self, bot) -> None:
        self.bot = bot
        self.brain = Brain(num_classes=3)
        self.brain.eval()
        self.data = [
            ("hello", "greeting"),
            ("hi there", "greeting"),
            ("hey", "greeting"),
            ("how are you", "question"),
            ("what is this", "question"),
            ("why did that happen", "question"),
            ("I like turtles", "other"),
            ("it is raining today", "other"),
            ("I like cats :3", "other"),
        ]

        self.class_to_idx = {"greeting": 0, "question": 1, "other": 2}

        for sentence, _ in self.data:
            for word in sentence.lower().split():
                if (
                    word not in self.brain.vocab
                    and len(self.brain.vocab) < self.brain.max_vocab
                ):
                    self.brain.vocab[word] = len(self.brain.vocab)

        self.brain.train_model(self.data, self.class_to_idx, epoch=500, lr=0.05)
        self.brain.eval()

    @app_commands.command(name="ai_test", description="i need to test an ai rq")
    async def ai(self, interaction: discord.Interaction, text: str):
        result = self.brain.predict(text)

        if result is None:
            await interaction.response.send_message("Silence found, thought aborted")
            return

        intent = self.data[result]

        if intent == "greeting":
            await interaction.response.send_message("Heya. Pattern recognized")
        elif intent == "question":
            await interaction.response.send_message("Query detected. Noted")
        else:
            await interaction.response.send_message("Interesting, noted")


async def setup(bot):
    await bot.add_cog(AI(bot))
