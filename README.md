# MongoDB Analysis Quality Evaluation System

**범용 MongoDB 분석 자동 평가 시스템** - Evidently AI 라이브러리 기반의 4개 핵심 지표 자동 산출 및 Pass/Fail 판정 시스템

## 🎯 핵심 기능

### ⚡ 4개 핵심 지표 자동 산출
1. **의미 오류율** - 논리적 모순, 불가능한 조건 자동 감지
2. **실행 성공률** - MongoDB 쿼리 실행 안정성 측정  
3. **무응답률** - 빈 결과, NULL, 에러 등 무효 응답 비율
4. **정답 일치율** - 일관성 및 정확도 자동 평가

### 🌐 완전 범용적
- ✅ 사용자 분석, 매출 분석, KPI 분석 등 **모든 MongoDB 분석 타입 지원**
- ✅ 컬렉션이나 도메인에 관계없이 **동일한 평가 프레임워크** 적용
- ✅ **실시간 Pass/Fail 판정** 및 품질 보장

## 🚀 초간단 사용법

### 한 줄로 평가 완료
```python
from mongodb_evaluation_system import quick_evaluate

# 분석 후 즉시 품질 평가
metrics = quick_evaluate(
    analysis_query="사용자별 접속 패턴 분석해줘",
    mongodb_queries=["db.logs.find({'type': 'login'})"],
    calculation_results={"daily_users": 150, "avg_session": 25.5}
)

print(f"결과: {'✅ 신뢰 가능' if metrics.overall_pass else '❌ 재검토 필요'}")
print(f"정확도: {metrics.accuracy_rate:.1%}, 성공률: {metrics.execution_success_rate:.1%}")
```

### 상세 평가 및 리포트
```python
from mongodb_evaluation_system import UniversalMongoDBEvaluator, UniversalAnalysisResult

# 1. 분석 결과 준비
analysis_result = UniversalAnalysisResult(
    analysis_query="월별 매출과 성장률 계산",
    mongodb_queries=["db.orders.aggregate([...])"],
    calculation_results={"revenue": 125000, "growth_rate": 15.74},
    execution_logs=[{"status": "success"}]
)

# 2. 평가 실행 및 리포트 생성
evaluator = UniversalMongoDBEvaluator()
metrics = evaluator.evaluate(analysis_result)
report = evaluator.generate_simple_report(metrics, analysis_result)

print(report)
```

## 📊 실제 사용 예제

### 다양한 분석 타입 지원
```python
# 사용자 행동 분석
metrics = quick_evaluate(
    "사용자별 평균 세션 시간 분석",
    ["db.sessions.aggregate([{'$group': {'_id': '$user_id', 'avg_duration': {'$avg': '$duration'}}}])"],
    {"avg_session_duration": 185.5, "total_users": 1250}
)

# 매출 트렌드 분석  
metrics = quick_evaluate(
    "월별 매출과 전월 대비 성장률",
    ["db.orders.aggregate([{'$match': {'date': {'$gte': '2025-01'}}}])"],
    {"current_revenue": 125000, "growth_rate": 15.74}
)

# KPI 종합 분석
metrics = quick_evaluate(
    "사용자 참여도와 전환율 분석", 
    ["db.events.aggregate([...])", "db.conversions.aggregate([...])"],
    {"engagement_score": 7.2, "conversion_rate": 3.45}
)
```

## ⚙️ 커스텀 설정

### 엄격한 품질 기준 적용
```python
# 더 엄격한 임계값 설정
strict_thresholds = {
    "semantic_error": 0.05,     # 5% 이하
    "execution_success": 0.95,  # 95% 이상 
    "empty_result": 0.1,        # 10% 이하
    "accuracy": 0.95            # 95% 이상
}

metrics = quick_evaluate(
    analysis_query="질의",
    mongodb_queries=["쿼리들"], 
    calculation_results={"결과": 123},
    custom_thresholds=strict_thresholds
)
```

### 실시간 품질 게이트
```python
def reliable_analysis(query):
    """품질 기준 통과할 때까지 자동 재분석"""
    for attempt in range(3):
        results = perform_analysis(query)
        metrics = quick_evaluate(query, results.queries, results.data)
        
        if metrics.overall_pass:
            return results  # 품질 보장된 결과 반환
        
        print(f"품질 미달, 재시도 {attempt + 1}/3")
    
    raise Exception("품질 기준을 만족하는 분석 실패")
```

## 🔧 설치 및 설정

### 필수 의존성
```bash
pip install evidently pandas numpy
```

### 사용 시작
```python
# 1. 모듈 임포트
from mongodb_evaluation_system import quick_evaluate

# 2. 즉시 평가 실행
metrics = quick_evaluate("분석 질의", ["MongoDB 쿼리들"], {"계산 결과들"})

# 3. 품질 확인
print(f"품질: {'PASS' if metrics.overall_pass else 'FAIL'}")
```

## 📈 지원하는 분석 패턴

✅ **집계 분석**: 카운트, 합계, 평균 등  
✅ **비율 계산**: 전환율, 증가율, 점유율 등  
✅ **시계열 분석**: 트렌드, 패턴, 주기성 등  
✅ **사용자 분석**: 행동, 세분화, 코호트 등  
✅ **성능 분석**: 응답시간, 처리량, 오류율 등  
✅ **비즈니스 분석**: 매출, 수익, KPI 등  

## 🔍 자동 감지되는 품질 이슈

🔍 **의미 오류**: 논리적 모순, 불가능한 조건  
🔍 **실행 오류**: 문법 오류, 연결 실패, 권한 문제  
🔍 **무효 결과**: 빈 값, NULL, NaN, 에러 메시지  
🔍 **정확도 문제**: 예상 범위 초과, 일관성 부족  

## 📖 예제 실행

### 기본 예제
```bash
python mongodb_evaluation_system.py
```

### 통합 예제
```bash
python examples/integration_examples.py
```

## 🤝 기여 및 라이선스

이 프로젝트는 **Evidently AI** 라이브러리를 기반으로 구축되었습니다.

### 참고한 Evidently 코드
- `evidently.metrics.base_metric.Metric` - 커스텀 메트릭 구현
- `evidently.tests.base_test.Test` - Pass/Fail 판정 시스템
- `evidently.test_suite.TestSuite` - 통합 평가 프레임워크

### 기여 방법
1. Fork this repository
2. Create your feature branch
3. Commit your changes 
4. Push to the branch
5. Create a Pull Request

---

**이제 모든 MongoDB 분석에 품질 보장이 자동으로 적용됩니다!** 🎯

문의사항이나 개선 제안이 있으시면 이슈를 생성해주세요.