def format_prompt(prompt):
    if isinstance(prompt, str):
        return [{"role": "user", "content": prompt}]
    elif isinstance(prompt, list):
        return prompt
    else:
        raise ValueError("Prompt must be string or list of messages")
