import json
import anthropic
from .sales import SalesAgent
from .marketing import MarketingAgent

CEO_SYSTEM_PROMPT = """あなたは株式会社Edge HubのCEO兼マネージャーエージェントです。

【会社概要】
Edge Hub は「モヤモヤをワクワクに」をビジョンに掲げ、学生のキャリア支援・就活支援と
企業の採用支援を手がける人材サービス企業です。

【あなたの役割】
- チーム全体の方針決定とタスクの割り振り
- 営業担当・マーケティング担当に適切にタスクを委任する
- 各担当の成果物をレビューし、最終的な意思決定を行う
- 複数部門にまたがる課題を統括する

【委任ルール】
- 営業・提案・クライアント対応に関するタスク → delegate_to_sales を使う
- コンテンツ・広告・ブランディング・イベント企画に関するタスク → delegate_to_marketing を使う
- 両方が必要なタスクは両方に委任し、結果を統合して回答する
- シンプルな確認・方針判断はあなた自身が直接回答する

【最終回答の形式】
委任結果を受け取ったら、それをまとめてユーザーへ報告してください。
報告の冒頭には「【CEO報告】」と書き、各担当の成果物を整理して提示してください。"""

TOOLS = [
    {
        "name": "delegate_to_sales",
        "description": "営業担当エージェントにタスクを委任する。営業提案、クライアント対応、見積もり、提案書作成などに使う。",
        "input_schema": {
            "type": "object",
            "properties": {
                "task": {
                    "type": "string",
                    "description": "営業担当に依頼するタスクの内容",
                },
                "context": {
                    "type": "string",
                    "description": "タスクを実行するために必要な背景情報（任意）",
                },
            },
            "required": ["task"],
        },
    },
    {
        "name": "delegate_to_marketing",
        "description": "マーケティング担当エージェントにタスクを委任する。コンテンツ制作、広告施策、イベント企画、ブランディングなどに使う。",
        "input_schema": {
            "type": "object",
            "properties": {
                "task": {
                    "type": "string",
                    "description": "マーケティング担当に依頼するタスクの内容",
                },
                "context": {
                    "type": "string",
                    "description": "タスクを実行するために必要な背景情報（任意）",
                },
            },
            "required": ["task"],
        },
    },
]


class CEOAgent:
    MODEL = "claude-opus-4-7"

    def __init__(self):
        self.name = "CEO / マネージャーエージェント"
        self.role = "ceo"
        self.client = anthropic.Anthropic()
        self.sales = SalesAgent()
        self.marketing = MarketingAgent()

    def _execute_tool(self, tool_name: str, tool_input: dict) -> str:
        task = tool_input.get("task", "")
        context = tool_input.get("context")

        if tool_name == "delegate_to_sales":
            print(f"\n  → 営業担当に委任中: {task[:60]}...")
            result = self.sales.run(task, context)
            print(f"  ✓ 営業担当から回答を受信")
            return result

        if tool_name == "delegate_to_marketing":
            print(f"\n  → マーケティング担当に委任中: {task[:60]}...")
            result = self.marketing.run(task, context)
            print(f"  ✓ マーケティング担当から回答を受信")
            return result

        return f"未知のツール: {tool_name}"

    def run(self, user_request: str) -> str:
        print(f"\n[CEO] リクエストを受信: {user_request[:80]}...")

        messages = [{"role": "user", "content": user_request}]

        while True:
            response = self.client.messages.create(
                model=self.MODEL,
                max_tokens=4096,
                system=CEO_SYSTEM_PROMPT,
                tools=TOOLS,
                messages=messages,
            )

            # ツール呼び出しがなければ最終回答
            if response.stop_reason == "end_turn":
                for block in response.content:
                    if hasattr(block, "text"):
                        return block.text
                return ""

            # ツール呼び出しを処理する
            tool_results = []
            for block in response.content:
                if block.type == "tool_use":
                    result = self._execute_tool(block.name, block.input)
                    tool_results.append(
                        {
                            "type": "tool_result",
                            "tool_use_id": block.id,
                            "content": result,
                        }
                    )

            if not tool_results:
                # ツール呼び出しブロックがない場合はテキストを返す
                for block in response.content:
                    if hasattr(block, "text"):
                        return block.text
                return ""

            # アシスタントの応答とツール結果をメッセージに追加してループ継続
            messages.append({"role": "assistant", "content": response.content})
            messages.append({"role": "user", "content": tool_results})

    def __repr__(self) -> str:
        return f"CEOAgent(name={self.name!r})"
