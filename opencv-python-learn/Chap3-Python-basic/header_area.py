import math

def calc_area(type, a, b=None, c=None):
    """
    다양한 도형의 넓이를 계산하는 함수

    Args:
        type: 도형 종류 ('rectangle', 'triangle', 'circle')
        a: 첫 번째 매개변수 (직사각형-가로, 삼각형-밑변, 원-반지름)
        b: 두 번째 매개변수 (직사각형-세로, 삼각형-높이)
        c: 세 번째 매개변수 (현재 미사용, 확장 가능)

    Returns:
        float: 계산된 넓이
    """
    if type == 'rectangle':
        if b is None:
            return "직사각형은 가로와 세로가 필요합니다."
        area = a * b
        msg = f"직사각형 넓이: {a} × {b} = {area}"
        return area, msg

    elif type == 'triangle':
        if b is None:
            return "삼각형은 밑변과 높이가 필요합니다."
        area = (a * b) / 2
        msg = f"삼각형 넓이: ({a} × {b}) / 2 = {area}"
        return area, msg

    elif type == 'circle':
        area = math.pi * (a ** 2)
        msg = f"원의 넓이: π × {a}² = {area:.2f}"
        return area, msg

    else:
        return f"지원하지 않는 도형 타입입니다: {type}"


# 사용 예시
print("=== 도형 넓이 계산 ===\n")

# 직사각형 넓이
rect_area = calc_area('rectangle', 5, 3)

# 삼각형 넓이
triangle_area = calc_area('triangle', 6, 4)

# 원의 넓이
circle_area = calc_area('circle', 7)

# 잘못된 타입
calc_area('pentagon', 5)

def say():
    print('넓이를 구해요')

def write(result, msg):
    print(msg, ' 넓이는', result, 'm^2 입니다.')

say()
