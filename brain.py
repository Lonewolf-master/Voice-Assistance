from transformers import pipeline
import torch

class JarvisBrain:
    """
    JarvisBrain uses a local LLM to process transcribed text, 
    refine the meaning, and generate intelligent responses.
    """
    
    def __init__(self, model_name="TinyLlama/TinyLlama-1.1B-Chat-v1.0"):
        """
        Initializes the AI brain with a lightweight local model.
        """
        print(f"Loading AI Brain ({model_name})...")
        device = 0 if torch.cuda.is_available() else -1
        self.generator = pipeline(
            "text-generation", 
            model=model_name, 
            torch_dtype=torch.float16 if device == 0 else torch.float32,
            device=device
        )
        
    def think(self, user_input):
        """
        Processes user input and returns a response.
        - user_input: The transcribed text from STT.
        """
        prompt = f"""<|system|>
You are Jarvis, a helpful and concise voice assistant. Respond briefly to the user's request.</s>
<|user|>
{user_input}</s>
<|assistant|>
"""
        
        try:
            outputs = self.generator(
                prompt, 
                max_new_tokens=50, 
                do_sample=True, 
                temperature=0.7, 
                top_k=50, 
                top_p=0.95
            )
            response = outputs[0]["generated_text"].split("<|assistant|>")[-1].strip()
            return response
        except Exception as e:
            return f"I encountered an error while thinking: {str(e)}"

if __name__ == "__main__":
    # Quick test
    brain = JarvisBrain()
    print(brain.think("Hello Jarvis, how are you today?"))
