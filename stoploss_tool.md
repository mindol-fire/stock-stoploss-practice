# Stoploss Tool Spec

## 목적
종목 손절 알림(규칙 기반) 제공

## 입력 데이터
- 종목 가격: `entry_price`, `close`, `peak_price`
- 지수 값: `entry_index_ref`, `index_close`, `peak_index_ref`

## 공통 계산식
- 종목하락폭(`stock_down`) = `(기준가 - 현재가) / 기준가 * 100`
- 지수하락폭(`index_down`) = `(기준지수 - 현재지수) / 기준지수 * 100`
- 상대하락폭(`relative_down`) = `max(stock_down - index_down, 0)`

## 규칙
### A. 매수가 기준 손절선
- 기준가: `entry_price`
- 기준지수: `entry_index_ref`
- 손절 임계치(`threshold`): `10%`
- 손절선 가격: `entry_price * 0.90`

### B. 최고 종가 기준 트레일링 손절선
- 기준가: `peak_price` (`peak_close_since_entry`와 동일 의미)
- 기준지수: `peak_index_ref`
- 손절 임계치(`threshold`): `10%`
- 트레일링 손절선 가격: `peak_price * 0.90`

## 상태 판정 로직 (A/B 공통)
1. `stock_down < 10` 이면 `OK`
2. `stock_down >= 10` 이고 `relative_down >= 10` 이면 `HARD_STOP`
3. `stock_down >= 10` 이고 `relative_down < 10` 이면 `MARKET_DRIVEN_ALERT`
   - HARD_STOP으로 보지 않지만 알림은 제공

## 출력 포맷
A/B 각각 아래 컬럼으로 표를 출력:
- `stock_down`
- `index_down`
- `relative_down`
- `threshold`
- `status`

예시 출력(형식):

| rule | stock_down | index_down | relative_down | threshold | status |
|---|---:|---:|---:|---:|---|
| A | 12.30% | 3.10% | 9.20% | 10.00% | MARKET_DRIVEN_ALERT |
| B | 15.00% | 2.00% | 13.00% | 10.00% | HARD_STOP |
