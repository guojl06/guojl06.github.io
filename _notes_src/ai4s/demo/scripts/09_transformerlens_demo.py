import torch


def main():
    from transformer_lens import HookedTransformer
    device = "mps" if torch.backends.mps.is_available() else ("cuda" if torch.cuda.is_available() else "cpu")
    model = HookedTransformer.from_pretrained("gpt2-small", device=device)
    prompt = "The Eiffel Tower is located in"
    tokens = model.to_tokens(prompt)
    logits, cache = model.run_with_cache(tokens)
    print("logits:", logits.shape)
    print("resid_pre layer 5:", cache["blocks.5.hook_resid_pre"].shape)
    print("attn pattern layer 0:", cache["blocks.0.attn.hook_pattern"].shape)

if __name__ == "__main__":
    main()
