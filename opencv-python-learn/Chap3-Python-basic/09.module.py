import header_area as mod   # header_area.py 파일을 모듈로 임포트
from header_area import write # header_area.py 파일내 write 함수만 임포트

mod.say()
area, msg = mod.calc_area('rectangle',2, 4)
write(area, msg)