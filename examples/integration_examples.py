"""
범용 MongoDB 분석 자동 평가 시스템 통합 예제
어떤 분석이든 즉시 품질 평가가 가능한 간단한 구현
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from mongodb_evaluation_system import quick_evaluate, UniversalMongoDBEvaluator, UniversalAnalysisResult
from datetime import datetime
from typing import Dict, List, Any

class AnalysisQualityChecker:
    """분석 품질 실시간 체커"""
    
    def __init__(self, strict_mode: bool = False):
        """
        Args:
            strict_mode: True면 더 엄격한 기준 적용
        """
        self.strict_thresholds = {
            "semantic_error": 0.05,
            "execution_success": 0.95,
            "empty_result": 0.1,
            "accuracy": 0.95
        } if strict_mode else None
    
    def check_analysis_quality(self, 
                             user_query: str,
                             mongodb_queries: List[str], 
                             results: Dict[str, Any],
                             execution_info: List[Dict] = None) -> Dict[str, Any]:
        """
        분석 품질 즉시 체크
        
        Returns:
            품질 체크 결과 (PASS/FAIL + 4개 지표)
        """
        
        # 빠른 평가 실행
        metrics = quick_evaluate(
            analysis_query=user_query,
            mongodb_queries=mongodb_queries,
            calculation_results=results,
            execution_logs=execution_info or [],
            custom_thresholds=self.strict_thresholds
        )
        
        return {
            "timestamp": datetime.now().isoformat(),
            "query": user_query,
            "quality_status": "PASS" if metrics.overall_pass else "FAIL",
            "confidence_level": "높음" if metrics.overall_pass else "낮음",
            "metrics": {
                "semantic_error_rate": f"{metrics.semantic_error_rate:.2%}",
                "execution_success_rate": f"{metrics.execution_success_rate:.2%}",
                "empty_result_rate": f"{metrics.empty_result_rate:.2%}",
                "accuracy_rate": f"{metrics.accuracy_rate:.2%}"
            },
            "analysis_results": results,
            "recommendation": self._get_recommendation(metrics)
        }
    
    def _get_recommendation(self, metrics) -> str:
        """품질 기반 권장사항"""
        if metrics.overall_pass:
            return "✅ 분석 결과를 신뢰하고 사용할 수 있습니다."
        
        issues = []
        if metrics.semantic_error_rate > (self.strict_thresholds or {}).get("semantic_error", 0.1):
            issues.append("쿼리 논리 검토")
        if metrics.execution_success_rate < (self.strict_thresholds or {}).get("execution_success", 0.8):
            issues.append("실행 환경 점검")
        if metrics.empty_result_rate > (self.strict_thresholds or {}).get("empty_result", 0.2):
            issues.append("데이터 존재 확인")
        if metrics.accuracy_rate < (self.strict_thresholds or {}).get("accuracy", 0.9):
            issues.append("계산 로직 검증")
        
        return f"⚠️ 재검토 필요: {', '.join(issues)}"


def demo_various_analysis_types():
    """다양한 분석 타입 데모"""
    
    checker = AnalysisQualityChecker()
    
    # 1. 사용자 행동 분석
    print("=== 사용자 행동 분석 ===")
    user_behavior_result = checker.check_analysis_quality(
        user_query="사용자별 평균 세션 시간과 페이지뷰 분석",
        mongodb_queries=[
            "db.sessions.aggregate([{'$group': {'_id': '$user_id', 'avg_duration': {'$avg': '$duration'}}}])",
            "db.pageviews.aggregate([{'$group': {'_id': '$user_id', 'total_views': {'$sum': 1}}}])"
        ],
        results={
            "avg_session_duration": 185.5,
            "total_users": 1250,
            "avg_pageviews_per_user": 8.3
        }
    )
    print_quality_result(user_behavior_result)
    
    # 2. 매출 분석
    print("\n=== 매출 트렌드 분석 ===")
    revenue_result = checker.check_analysis_quality(
        user_query="월별 매출과 전월 대비 성장률 계산",
        mongodb_queries=[
            "db.orders.aggregate([{'$match': {'date': {'$gte': '2025-01'}}}, {'$group': {'_id': {'$month': '$date'}, 'revenue': {'$sum': '$amount'}}}])"
        ],
        results={
            "current_month_revenue": 125000,
            "previous_month_revenue": 108000,
            "growth_rate": 15.74,
            "order_count": 890
        }
    )
    print_quality_result(revenue_result)
    
    # 3. 에러가 있는 분석 (의도적)
    print("\n=== 문제가 있는 분석 ===")
    error_result = checker.check_analysis_quality(
        user_query="활성 사용자 수 계산",
        mongodb_queries=[
            "db.users.find({'user_id': {'$ne': '$user_id'}})",  # 의미 오류
            "db.sessions.count({'invalid_field': true})"         # 실행 오류 가능성
        ],
        results={
            "active_users": -10,    # 논리적 불가능
            "error_result": None,   # 무응답
            "invalid_rate": 150     # 불가능한 비율
        },
        execution_info=[
            {"status": "error", "message": "Field not found"},
            {"status": "success"}
        ]
    )
    print_quality_result(error_result)
    
    # 4. 복합 지표 분석
    print("\n=== 복합 KPI 분석 ===")
    kpi_result = checker.check_analysis_quality(
        user_query="사용자 참여도와 전환율 종합 분석",
        mongodb_queries=[
            "db.events.aggregate([{'$group': {'_id': '$user_id', 'engagement_score': {'$avg': '$score'}}}])",
            "db.conversions.aggregate([{'$group': {'_id': null, 'conversion_rate': {'$avg': '$converted'}}}])"
        ],
        results={
            "avg_engagement_score": 7.2,
            "conversion_rate": 3.45,
            "total_conversions": 234,
            "funnel_dropoff_rate": 12.8
        }
    )
    print_quality_result(kpi_result)


def print_quality_result(result: Dict[str, Any]):
    """품질 결과 예쁘게 출력"""
    print(f"🔍 분석: {result['query']}")
    print(f"📊 상태: {result['quality_status']} ({result['confidence_level']} 신뢰도)")
    print(f"💡 권장: {result['recommendation']}")
    
    print("📈 품질 지표:")
    for metric, value in result['metrics'].items():
        print(f"  - {metric}: {value}")
    
    print("📋 분석 결과:")
    for key, value in result['analysis_results'].items():
        print(f"  - {key}: {value}")


def real_time_quality_gate_example():
    """실시간 품질 게이트 예제"""
    
    def analyze_with_quality_gate(query: str, max_attempts: int = 3):
        """품질 기준 통과할 때까지 재시도"""
        
        checker = AnalysisQualityChecker(strict_mode=True)
        
        for attempt in range(max_attempts):
            print(f"\n🔄 분석 시도 {attempt + 1}/{max_attempts}")
            
            # 실제로는 여기서 MongoDB 분석 수행
            # 시뮬레이션: 시도할수록 품질 개선
            simulated_results = simulate_analysis_attempt(query, attempt)
            
            # 품질 체크
            quality_result = checker.check_analysis_quality(
                user_query=query,
                mongodb_queries=simulated_results['queries'],
                results=simulated_results['results'],
                execution_info=simulated_results['execution_info']
            )
            
            print(f"품질 상태: {quality_result['quality_status']}")
            
            # 품질 기준 통과 시 성공
            if quality_result['quality_status'] == "PASS":
                print("✅ 품질 기준 통과! 분석 완료")
                return quality_result
            
            # 마지막 시도가 아니면 계속
            if attempt < max_attempts - 1:
                print("❌ 품질 기준 미달, 재분석 중...")
        
        print("🚨 품질 기준을 만족하지 못했습니다")
        return quality_result
    
    # 실시간 품질 게이트 테스트
    print("=== 실시간 품질 게이트 테스트 ===")
    final_result = analyze_with_quality_gate("고객 생애가치(LTV) 분석")
    print_quality_result(final_result)


def simulate_analysis_attempt(query: str, attempt: int) -> Dict[str, Any]:
    """분석 시도 시뮬레이션 (시도할수록 품질 개선)"""
    
    if attempt == 0:
        # 첫 번째 시도: 문제 많음
        return {
            'queries': ["db.users.find({'id': {'$ne': '$id'}})"],  # 의미 오류
            'results': {"ltv": -100},  # 논리적 불가능
            'execution_info': [{"status": "error"}]
        }
    elif attempt == 1:
        # 두 번째 시도: 일부 개선
        return {
            'queries': ["db.users.aggregate([{'$group': {'_id': null, 'avg_ltv': {'$avg': '$revenue'}}}])"],
            'results': {"ltv": None},  # 무응답
            'execution_info': [{"status": "success"}]
        }
    else:
        # 세 번째 시도: 정상
        return {
            'queries': [
                "db.users.aggregate([{'$group': {'_id': null, 'avg_ltv': {'$avg': '$lifetime_value'}}}])",
                "db.transactions.aggregate([{'$group': {'_id': '$user_id', 'total_spent': {'$sum': '$amount'}}}])"
            ],
            'results': {
                "average_ltv": 245.50,
                "median_ltv": 180.00,
                "total_customers": 5420
            },
            'execution_info': [
                {"status": "success", "execution_time": 0.15},
                {"status": "success", "execution_time": 0.23}
            ]
        }


def quick_start_example():
    """빠른 시작 예제"""
    print("=== 빠른 시작 예제 ===")
    print("한 줄로 품질 평가하기:\n")
    
    # 간단한 예제
    metrics = quick_evaluate(
        analysis_query="일일 활성 사용자 수 분석",
        mongodb_queries=["db.users.find({'last_active': {'$gte': 'today'}})"],
        calculation_results={"daily_active_users": 1847}
    )
    
    print(f"✨ 결과: {'✅ 신뢰할 수 있음' if metrics.overall_pass else '❌ 재검토 필요'}")
    print(f"📊 품질 점수:")
    print(f"   - 정확도: {metrics.accuracy_rate:.1%}")
    print(f"   - 실행 성공률: {metrics.execution_success_rate:.1%}")
    print(f"   - 의미 오류율: {metrics.semantic_error_rate:.1%}")
    print(f"   - 무응답률: {metrics.empty_result_rate:.1%}")


if __name__ == "__main__":
    print("🚀 범용 MongoDB 분석 품질 평가 시스템 데모\n")
    
    # 1. 빠른 시작 예제
    quick_start_example()
    
    print("\n" + "="*60 + "\n")
    
    # 2. 다양한 분석 타입 데모
    demo_various_analysis_types()
    
    print("\n" + "="*60 + "\n")
    
    # 3. 실시간 품질 게이트 데모
    real_time_quality_gate_example()
    
    print("\n✅ 데모 완료! 이제 모든 MongoDB 분석에 품질 평가를 적용할 수 있습니다.")
    print("\n🔧 사용법:")
    print("1. from mongodb_evaluation_system import quick_evaluate")
    print("2. metrics = quick_evaluate('질의', ['쿼리들'], {'결과들'})")
    print("3. print(f'품질: {\"PASS\" if metrics.overall_pass else \"FAIL\"}')")
