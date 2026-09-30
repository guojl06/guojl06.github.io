import argparse
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1]))

import pandas as pd
import torch
from tqdm import tqdm
from src.config_utils import file_prefix, load_config, output_paths
from src.experiment_utils import require_single_token
from src.hook_utils import get_final_norm
from src.model_utils import load_causal_lm
from src.prompt_utils import prompt_suite_from_config, row_tags_json, row_variables_json, validate_prompt_rows


def parse_args():
    p=argparse.ArgumentParser(); p.add_argument("--config",default="configs/pythia_70m.json"); p.add_argument("--prompt-suite",default=None); p.add_argument("--cache-dir",default=None); p.add_argument("--max-examples",type=int,default=None); p.add_argument("--skip-invalid",action="store_true"); p.add_argument("--top-k",type=int,default=5); p.add_argument("--out",default=None); return p.parse_args()


def main():
    args=parse_args(); cfg=load_config(args.config)
    model, tokenizer, device, _=load_causal_lm(cfg,args.cache_dir)
    rows_in=prompt_suite_from_config(cfg,args.prompt_suite,args.max_examples)
    errors=validate_prompt_rows(rows_in, tokenizer=tokenizer, max_prompt_tokens=cfg.get("experiments",{}).get("global_defaults",{}).get("max_prompt_tokens"))
    if errors and not args.skip_invalid: raise ValueError("Prompt validation failed. Use validation script or pass --skip-invalid.")
    bad_ids={e.get("prompt_id") for e in errors}; norm=get_final_norm(model); rows_out=[]
    for row in tqdm(rows_in, desc="prompts"):
        if args.skip_invalid and row.get("prompt_id") in bad_ids: continue
        if row.get("task") == "activation_patching": continue
        target_id=require_single_token(tokenizer,row["target_text"])
        inputs=tokenizer(row["prompt"],return_tensors="pt").to(device)
        with torch.no_grad(): out=model(**inputs,use_cache=False,output_hidden_states=True,return_dict=True)
        for layer_idx,h in enumerate(out.hidden_states):
            final_h=h[:,-1,:]
            if norm is not None: final_h=norm(final_h)
            logits_lens=model.lm_head(final_h)
            values,ids=torch.topk(logits_lens[0],k=args.top_k)
            rows_out.append({"model_id":cfg["model_id"],"prompt_id":row.get("prompt_id"),"task":row.get("task"),"condition":row.get("condition"),"layer_index_including_embedding":layer_idx,"target_text":row.get("target_text"),"target_logit":logits_lens[0,target_id].item(),"top_tokens":repr([tokenizer.decode([i.item()]) for i in ids]),"top_values":repr([round(v.item(),4) for v in values]),"variables_json":row_variables_json(row),"tags_json":row_tags_json(row)})
    paths=output_paths(cfg); paths["results"].mkdir(parents=True,exist_ok=True)
    out_path=Path(args.out) if args.out else paths["results"] / f"{file_prefix(cfg)}_batch_logit_lens.csv"
    pd.DataFrame(rows_out).to_csv(out_path,index=False); print("saved:",out_path)

if __name__ == "__main__": main()
