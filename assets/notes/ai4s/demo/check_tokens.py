from transformers import AutoTokenizer
tok = AutoTokenizer.from_pretrained('Qwen/Qwen3.5-4B', trust_remote_code=True, local_files_only=True, cache_dir='./hf_cache')
tags = ['<think>', '</think>', '</think>
', '
', '

']
for tag in tags:
    ids = tok.encode(tag, add_special_tokens=False)
    print(f'{repr(tag)}: {ids}')
# also check the actual tokenizer vocab for think-related
print('---')
for tid in range(tok.vocab_size):
    txt = tok.decode([tid])
    if 'think' in txt.lower():
        print(f'token {tid}: {repr(txt)}')
        if tid > 250000:
            break
