import json

class Tokenizer:
    def __init__(self, vocab):
        self.vocab = vocab
        with open(vocab, 'r', encoding='utf-8') as f:
            self.vocab = json.load(f)
            self.reverse_vocab = {v: k for k, v in self.vocab.items()}

    def encode(self, text): # text'i token ID'lerine dönüştür
        tokens = []
        
        # Bütün kelimeleri boşluklardan ayır ve her kelimeyi alt kelimelere böl
        for word in text.split():
            i = 0

            # Kelimeyi alt kelimelere böl
            while i < len(word):
                match = None

                for j in range(len(word), i, -1): # Kelimenin sonundan başlayarak alt kelimeleri kontrol et
                    subword = word[i:j]
                    if subword in self.vocab: # Eğer alt kelime sözlükte varsa token olarak ekle
                        match = subword
                        tokens.append(self.vocab[match])
                        i = j # İndeksi alt kelimenin sonuna taşı
                        break

                # Eğer eşleşme bulunamazsa bilinmeyen token ekle ve ilerle
                if not match:
                    tokens.append(self.vocab.get("<unk>"))
                    i += 1

            # Kelimeler arasına boşluk token'ı ekle
            tokens.append(self.vocab[" "])

        # Son boşluk token'ını kaldır
        return tokens[:-1]

    def decode(self, token_ids): # token ID'lerini tekrar metne dönüştür
        text = ""

        for token_id in token_ids:
            text += self.reverse_vocab[token_id]

        return text