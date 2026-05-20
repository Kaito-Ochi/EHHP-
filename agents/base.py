import anthropic
from typing import Optional


class BaseAgent:
    MODEL = "claude-opus-4-7"

    def __init__(self, name: str, role: str, system_prompt: str):
        self.name = name
        self.role = role
        self.system_prompt = system_prompt
        self.client = anthropic.Anthropic()

    def run(self, task: str, context: Optional[str] = None) -> str:
        user_message = task
        if context:
            user_message = f"【背景情報】\n{context}\n\n【依頼】\n{task}"

        response = self.client.messages.create(
            model=self.MODEL,
            max_tokens=2048,
            system=self.system_prompt,
            messages=[{"role": "user", "content": user_message}],
        )
        return response.content[0].text

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.name!r}, role={self.role!r})"
