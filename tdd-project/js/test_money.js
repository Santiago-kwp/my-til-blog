const assert = require("assert"); // 이후 단언에 필요한 assert 패키지를 가져온다.

let fiver = new Dollar(5); // 'USD 5.' 를 나타내는 객체로 Dollar는 아직 존재하지 않는다.
let tenner = fiver.times(2); // 테스트 대상 메소드인 times로 아직 존재하지 않는다.
assert.strictEqual(tenner.amount, 10); // strictEqual 단언문으로 실제값과 예상값을 비교한다.
