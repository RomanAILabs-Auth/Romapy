import time, os, sys
from llama_cpp import Llama

accelerate = speed_wrap()

MODEL_NAME = "dolphin-2.9-llama3-8b-Q4_K_M.gguf"
search_paths = [
    os.path.join(os.path.dirname(__file__), MODEL_NAME),
    os.path.expanduser(f"~/Downloads/{MODEL_NAME}"),
    os.path.expanduser(f"~/downloads/{MODEL_NAME}")
]
MODEL_PATH = next((p for p in search_paths if os.path.exists(p)), None)

if not MODEL_PATH:
    print(f"❌ Error: {MODEL_NAME} not found!")
    sys.exit(1)

print(f"🐬 Loading Turbo Model: {MODEL_PATH}")
llm = Llama(model_path=MODEL_PATH, n_ctx=2048, n_threads=8, n_batch=512, n_ubatch=512, verbose=False)

@accelerate
def clean_token(text):
    return text.strip() + " "

def chat():
    print("\n--- RomaPy Chat (2.07s Latency Mode) ---")
    while True:
        query = input("\nYou: ")
        if query.lower() in ['exit', 'quit']: break
        prompt = f"<|im_start|>system\nYou are Dolphin.<|im_end|>\n<|im_start|>user\n{query}<|im_end|>\n<|im_start|>assistant\n"
        start = time.time()
        stream = llm(prompt, max_tokens=512, stop=["<|im_end|>"], stream=True)
        print("AI: ", end="")
        first = True
        for output in stream:
            if first:
                print(f"🚀 [Latency: {time.time()-start:.2f}s] ", end="")
                first = False
            print(clean_token(output['choices'][0]['text']), end="", flush=True)
        print()

if __name__ == "__main__":
    chat()
