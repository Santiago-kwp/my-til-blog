package main // 패키지를 선언한다.

import (
	"testing"
) // testing 패키지를 가져온 후 t.Errorf에 사용한다.

func TestMultiplication(t *testing.T) { // 테스트 메소드로, 반드시 *testing.T 인자 하나를 가지며 Test로 시작해야 한다.
	fiver := Dollar { // 'USD 5.' 달러를 나타내는 구조체로 아직 존재하지 않는다.
		amount: 5,
	}
	tenner := fiver.Times(2) // 테스트 대상 메소드인 Times로 아직 존재하지 않는다.
	if tenner.amount != 10 {
		t.Errorf("Expected 10, get: [%d]", tenner.amount)
	}
}
