from agents.orchestrator import run_orchestrator

if __name__ == "__main__":
    request = "피보나치 수열 알고리즘을 조사하고, Python으로 10번째 항을 계산해줘"

    print("=" * 50)
    print(f"요청: {request}")
    print("=" * 50)

    result = run_orchestrator(request)

    print("\n✅ 최종 결과:")
    print(result)