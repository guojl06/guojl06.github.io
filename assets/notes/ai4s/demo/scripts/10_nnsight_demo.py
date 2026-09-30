import argparse


def parse_args():
    p = argparse.ArgumentParser()
    p.add_argument("--model-id", default="EleutherAI/pythia-70m")
    return p.parse_args()


def main():
    args = parse_args()
    from nnsight import LanguageModel
    model = LanguageModel(args.model_id, device_map="auto")
    with model.trace("The capital of France is"):
        logits = model.output.logits.save()
    print("logits:", logits.value.shape)

if __name__ == "__main__":
    main()
