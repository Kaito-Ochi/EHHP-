"""
Edge Hub マルチエージェントシステム
=====================================
CEO / 営業 / マーケティングの3エージェントが協調して
会社業務をサポートします。

使い方:
    python main.py

環境変数:
    ANTHROPIC_API_KEY  - Anthropic API キー（必須）
"""

import os
import sys
from agents import CEOAgent


EXAMPLES = [
    "IT企業向けの新卒採用支援サービスの提案書を作ってほしい",
    "就活生向けのSNSキャンペーンを企画して",
    "来月の合同説明会に向けて、営業資料とSNS告知文を両方準備して",
]


def print_banner():
    print("=" * 60)
    print("  Edge Hub マルチエージェントシステム")
    print("  CEO / 営業担当 / マーケティング担当")
    print("=" * 60)
    print()
    print("使用例:")
    for i, ex in enumerate(EXAMPLES, 1):
        print(f"  {i}. {ex}")
    print()
    print("終了するには 'quit' または 'exit' と入力してください。")
    print("-" * 60)


def main():
    if not os.environ.get("ANTHROPIC_API_KEY"):
        print("エラー: ANTHROPIC_API_KEY 環境変数が設定されていません。")
        print("  export ANTHROPIC_API_KEY='your-api-key'")
        sys.exit(1)

    print_banner()
    ceo = CEOAgent()

    while True:
        try:
            user_input = input("\nあなた: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nシステムを終了します。")
            break

        if not user_input:
            continue

        if user_input.lower() in ("quit", "exit", "終了"):
            print("システムを終了します。")
            break

        print("\n[処理中...]")
        result = ceo.run(user_input)
        print(f"\n{result}")
        print("\n" + "-" * 60)


if __name__ == "__main__":
    main()
